# SPDX-FileCopyrightText: 2025-present Anton Popov <a.popov.fizteh@gmail.com>
#
# SPDX-License-Identifier: MIT
"""
Classes for communication with the Crossref API.

This module is part of the Artfinder package.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Any, Self, TypeVar, cast, Generator
import logging

import requests
from pandas import DataFrame

from artfinder.dataclasses import (
    CrossrefResource,
    CrossrefQueryField,
    DocumentType,
)
from artfinder.http_requests import AsyncHTTPRequest
from artfinder.crossref_helpers import build_cr_endpoint
from artfinder.article import CrossrefArticle, ArticleCollection
from artfinder.helpers import LinePrinter, MultiLinePrinter

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Endpoint(ABC):

    ROW_LIMIT = 100
    "Maximum articles to be retrieved in a single request."
    CONCURRENCY_LIMIT = 5

    def __init__(
        self,
        context: list[str] | None = None,
        request_params: dict[str, Any] | None = None,
        endpoint: str | None = None,
        email: str | None = None,
        **kwargs,
    ):
        self.printer = MultiLinePrinter(self.CONCURRENCY_LIMIT + 1)
        self.status_line = LinePrinter()
        ahttpr = AsyncHTTPRequest(email=email, concurrency_limit=self.CONCURRENCY_LIMIT)
        self.async_get = ahttpr.async_get
        self.get = ahttpr.get
        self.request_params = request_params or {}
        self.context = context
        self.endpoint = endpoint
        self.email = email
        """
        Context for the request. e.g. context=['types', 'journal-article'] and
        RESOURCE='works' will result in querying from 
        api.crossref.org/types/journal-article/works
        """

    @property
    @abstractmethod
    def RESOURCE(self) -> CrossrefResource:
        """
        This property should be implemented in the child class.
        """
        pass

    @property
    def request_params(self) -> dict[str, Any]:
        """
        This property retrieve the request parameters.
        """
        self._escaped_pagging()
        return self._request_params

    @request_params.setter
    def request_params(self, value: dict[str, Any]) -> None:
        """
        This property set the request parameters.
        """
        self._request_params = value

    def _escaped_pagging(self) -> None:
        """
        This method removes the offset and rows parameters from the
        request_params dictionary.
        This is used to build the url attribute.
        """

        # it contained "rows"...
        escape_pagging = ["offset"]

        for item in escape_pagging:
            self._request_params.pop(item, None)

    @property
    def version(self) -> str:
        """
        This attribute retrieve the API version.
        """
        result = self.get(
            url=self.request_url,
            params=self.request_params,
        )

        return result.get("message_version", "undefined")

    def count(self) -> int:
        """
        This method retrieve the total of records resulting from a given query.

        Note
        ----
        This method will send request to the Crossref API and should be chained the last.
        """
        request_params = dict(self.request_params)
        request_params["rows"] = 0

        result = self.get(
            url=self.request_url,
            params=request_params,
            print_progress=False,
        )

        num_found = int(result.get("message", {}).get("total-results"))
        self.status_line(f"Found {num_found} items.")

        return num_found

    @property
    def url(self):
        """
        This attribute retrieve the url that will be used as a HTTP request to
        the Crossref API.

        This attribute can be used compounded with query, filter,
        sort, order and facet methods.

        Examples:
            >>> from crossref.restful import Works
            >>> Works().query('zika').url
            'https://api.crossref.org/works?query=zika'
            >>> Works().query('zika').filter(prefix='10.1590').url
            'https://api.crossref.org/works?query=zika&filter=prefix%3A10.1590'
            >>> Works().query('zika').filter(prefix='10.1590').sort('published') \
                .order('desc').url
            'https://api.crossref.org/works?sort=published
            &order=desc&query=zika&filter=prefix%3A10.1590'
            >>> Works().query('zika').filter(prefix='10.1590').sort('published') \
                .order('desc').filter(has_abstract='true').query(author='Marli').url
            'https://api.crossref.org/works?sort=published
            &filter=prefix%3A10.1590%2Chas-abstract%3Atrue&query=zika&order=desc&query.author=Marli'
        """

        sorted_request_params = sorted([(k, v) for k, v in self.request_params.items()])
        req = requests.Request(
            "get", self.request_url, params=sorted_request_params
        ).prepare()

        return req.url

    @property
    def request_url(self) -> str:
        """Request endpoint for http request."""
        return build_cr_endpoint(
            resource=self.RESOURCE, endpoint=self.endpoint, context=self.context
        )

    def __iter__(self) -> Generator[dict[str, str], None, None]:

        if any(value in self.request_params for value in ["sample", "rows"]):
            if self.request_params.get("rows") is not None:
                self.status_line(
                    f"Fetching up to {self.request_params['rows']} items..."
                )
            result = self.get(
                url=self.request_url,
                params=self.request_params,
                print_progress=False,
            )
            if result is None:
                self.status_line("Found nothing.")
                return
            self.status_line(f"Fetched {len(result['message']['items'])} items.")
            for item in result["message"]["items"]:
                yield item

        else:
            request_params = dict(self.request_params)
            request_params["cursor"] = "*"
            request_params["rows"] = self.ROW_LIMIT
            items_obtained = 0
            self.status_line(f'Fetching up to {request_params["rows"]} items...')
            while True:
                result = self.get(
                    url=self.request_url,
                    params=request_params,
                    print_progress=False,
                )

                if result is None:
                    self.status_line("Found nothing.")
                    return

                if len(result["message"]["items"]) == 0:
                    if items_obtained == 0:
                        self.status_line("Empty result.")
                    else:
                        self.status_line(
                            f"Found {items_obtained} item{'s' if items_obtained > 1 else ''}."
                        )
                    return
                else:
                    increment = len(result["message"]["items"])
                    items_obtained += increment
                    self.status_line(
                        f"Found {items_obtained} item{'s' if items_obtained > 1 else ''}."
                         + f"{'Fetching more...' if increment == self.ROW_LIMIT else ''}"
                    )
                for item in result["message"]["items"]:
                    yield item

                request_params["cursor"] = result["message"]["next-cursor"]

    def init_params(self) -> set[str]:
        """Get list of parameters for initialization."""

        return set(("email", "request_params", "context", "endpoint"))

    def from_self(self, **kwargs) -> Self:
        """
        Create a new instance of the class.
        """

        params_list = self.init_params()
        params = dict()
        for param in params_list:
            if param in kwargs:
                params[param] = kwargs[param]
            else:
                params[param] = getattr(self, param)
        return self.__class__(**params)


class Crossref(Endpoint):
    """Wrap around the Crossref API."""

    @property
    def RESOURCE(self) -> CrossrefResource:
        """works endpoint."""
        return CrossrefResource.WORKS

    def get_df(self, max_results: int | None = None) -> DataFrame:
        """
        Build data frame query results.
        """

        if max_results is not None:
            self.request_params["rows"] = max_results
        return ArticleCollection(self).to_df()

    def query(self, **kwargs) -> Self:
        """
        This method can be chained with filter method.
        kwargs: CrossrefQueryField.
        """

        for field, value in kwargs.items():
            if field not in CrossrefQueryField:
                raise ValueError("Invalid query field name")
            self.request_params["query.%s" % field.replace("_", "-")] = value

        return self.from_self()

    def author(self, author: str | None) -> Self:
        """
        Search by author.
        """

        if author is not None and author != "":
            self.request_params["query." + CrossrefQueryField.AUTHOR] = author
        return self.from_self()

    def search(self, query: str | None) -> Self:
        """
        Bibliographic search.
        """

        if query is not None and query != "":
            self.request_params["query." + CrossrefQueryField.BIBLIOGRAPHIC] = query
        return self.from_self()

    def filter(self, **kwargs) -> Self:
        """
        Filter the results at server side.
        """

        filter_validator = CrossrefFilterValidator()
        for field, value in kwargs.items():
            # skip empty values
            if value is None or value == "":
                continue
            if isinstance(value, list):
                validated_values = [filter_validator(field, v) for v in value]
            else:
                validated_values = [filter_validator(field, value)]

            for i, v in enumerate(validated_values):
                if i == 0 and "filter" not in self.request_params:
                    self.request_params["filter"] = (
                        field.replace("_", "-") + ":" + str(v)
                    )
                else:
                    self.request_params["filter"] += (
                        "," + field.replace("_", "-") + ":" + str(v)
                    )

        return self.from_self()

    def article(self) -> Self:
        """
        Ensure that only articles will be searched.
        """
        return self.filter(
            type=[DocumentType.JOURNAL_ARTICLE, DocumentType.PROCEEDINGS_ARTICLE]
        )

    def doi(self, doi: str) -> DataFrame:
        """
        Search by DOI.
        """

        self.status_line(f"Fetching {doi}...")
        result = self.get(
            url=build_cr_endpoint(resource=self.RESOURCE, endpoint=doi),
        )
        if result is None:
            self.status_line("Found nothing.")
            return DataFrame(columns=CrossrefArticle.get_all_slots())

        self.status_line(f"Fethed {doi}")
        return CrossrefArticle(result["message"]).to_df()

    def get_dois(self, dois: list[str]) -> DataFrame:
        """
        Get all articles from a list of DOIs as dataframe.
        """

        # Get all articles from a list of DOIs
        urls = [build_cr_endpoint(resource=self.RESOURCE, endpoint=doi) for doi in dois]
        results = self.async_get(urls)
        return ArticleCollection(
            [
                CrossrefArticle(result["message"])
                for result in results.values()
                if result is not None
            ]
        ).to_df()

    def get_refs(
        self, df: DataFrame, concurrent_lim: int = 50
    ) -> tuple[DataFrame, list[str]]:
        """
        Get all references from articles in the DataFrame.
        """

        # Get all references from articles in the DataFrame
        raise NotImplementedError("This method is not implemented yet.")
        all_refs = []
        for article in df["references"]:
            if article is not None:
                all_refs.extend(article)
        all_refs = list(set(all_refs))
        print(f"Found {len(all_refs)} unique references.")
        return _execute_coro(self._get_with_limit, all_refs, rate_limit=concurrent_lim)


class CrossrefFilterValidator:
    """
    Validate filter values
    """

    # TODO: change it for using pydantic
    VALIDATORS = {
        "alternative_id": "dummy",
        "archive": "archive",
        "article_number": "dummy",
        "assertion": "dummy",
        "assertion_group": "dummy",
        "award.funder": "dummy",
        "award.number": "dummy",
        "category_name": "dummy",
        "clinical_trial-number": "dummy",
        "container_title": "dummy",
        "content_domain": "dummy",
        "directory": "directory",
        "doi": "dummy",
        "from_accepted_date": "is_date",
        "from_created_date": "is_date",
        "from_deposit_date": "is_date",
        "from_event_end_date": "is_date",
        "from_event_start_date": "is_date",
        "from_index_date": "is_date",
        "from_issued_date": "is_date",
        "from_online_pub_date": "is_date",
        "from_posted_date": "is_date",
        "from_print_pub_date": "is_date",
        "from_pub_date": "is_date",
        "from_update_date": "is_date",
        "full_text.application": "dummy",
        "full_text.type": "dummy",
        "full_text.version": "dummy",
        "funder": "dummy",
        "funder_doi_asserted_by": "dummy",
        "group_title": "dummy",
        "has_abstract": "is_bool",
        "has_affiliation": "is_bool",
        "has_archive": "is_bool",
        "has_assertion": "is_bool",
        "has_authenticated-orcid": "is_bool",
        "has_award": "is_bool",
        "has_clinical_trial_number": "is_bool",
        "has_content_domain": "is_bool",
        "has_domain_restriction": "is_bool",
        "has_event": "is_bool",
        "has_full_text": "is_bool",
        "has_funder": "is_bool",
        "has_funder_doi": "is_bool",
        "has_license": "is_bool",
        "has_orcid": "is_bool",
        "has_references": "is_bool",
        "has_relation": "is_bool",
        "has_update": "is_bool",
        "has_update_policy": "is_bool",
        "is-update": "is_bool",
        "isbn": "dummy",
        "issn": "dummy",
        "license.delay": "is_integer",
        "license.url": "dummy",
        "license.version": "dummy",
        "location": "dummy",
        "member": "is_integer",
        "orcid": "dummy",
        "prefix": "dummy",
        "relation.object": "dummy",
        "relation.object-type": "dummy",
        "relation.type": "dummy",
        "type": "correct_doc_type",
        "type_name": "dummy",
        "until_accepted_date": "is_date",
        "until_created_date": "is_date",
        "until_deposit_date": "is_date",
        "until_event_end_date": "is_date",
        "until_event_start_date": "is_date",
        "until_index_date": "is_date",
        "until_issued_date": "is_date",
        "until_online_pub_date": "is_date",
        "until_posted_date": "is_date",
        "until_print_pub_date": "is_date",
        "until_pub_date": "is_date",
        "until_update_date": "is_date",
        "update_type": "dummy",
        "updates": "dummy",
    }

    def __call__(self, filter: str, value: str) -> Any:
        # TODO: add some kind of similarity check, so that only the most
        # similar values are returned in error description
        if filter not in self.VALIDATORS:
            raise ValueError(
                f"Invalid filter: {filter}. Valid filters: {self.VALIDATORS.keys()}"
            )
        try:
            return getattr(self, self.VALIDATORS[filter])(value)
        except ValueError as exc:
            raise ValueError(
                f"Invalid value for filter {filter}: {exc.args[0]}"
            ) from exc

    @staticmethod
    def dummy(value: T) -> T:
        return value

    @staticmethod
    def is_date(value: str) -> date:
        """
        Validate date format.
        """
        try:
            return datetime.strptime(value, "%Y").date()
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m").date()
            except ValueError:
                try:
                    return datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError as exc:
                    raise ValueError(f"Invalid date {value}.")

    @staticmethod
    def is_integer(value: str | int) -> int:
        """
        Validate integer format.
        """
        try:
            value = int(value)
            if value >= 0:
                return value
            raise ValueError(f"Numerica value should be positive, but got: {value}")
        except ValueError:
            raise ValueError(f"Expected integer, but got: {value}")

    @staticmethod
    def is_bool(value: str | int) -> bool:

        true_vals = ["True", "true", "1"]
        false_vals = ["False", "false", "0"]

        if str(value) in true_vals:
            return True
        if str(value) in false_vals:
            return False
        raise ValueError(
            f"Expected boolean, but got: {value}. Expected values: {true_vals + false_vals}"
        )

    @staticmethod
    def correct_doc_type(value: str) -> str:
        """
        Validate document type.
        """
        if value in DocumentType:
            return value
        raise ValueError(
            f"Invalid document type {value}. Valid values are: {[doc.value for doc in DocumentType]}"
        )

    @staticmethod
    def archive(value: str) -> str:
        expected = ("Portico", "CLOCKSS", "DWT")

        if str(value) in expected:
            return value

        raise ValueError(f"Invalid archive {value}. Valid values are: {expected}")

    @staticmethod
    def directory(value: str) -> str:
        expected = "DOAJ"

        if str(value) in expected:
            return value

        msg = "Directory specified as {} but must be one of: {}".format(
            str(value), ", ".join(expected)
        )
        raise ValueError(
            msg,
        )

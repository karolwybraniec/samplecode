#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import numbers

from enum import Enum
from math import ceil

from CRS.Model.Entity.CollectedData import CollectedData
from CRS.Model.Entity.RequestParameter import RequestParameter
from CRS.Model.Enum.Endpoint import Endpoint
from CRS.Model.Enum.FilterType import FilterType
from CRS.Model.Enum.ObjectType import ObjectType
from CRS.Model.Enum.SortOrder import SortOrder
from Common.Helpers.AssertHelper.TestWrapper import TestWrapper
from Common.Helpers.AssertHelper.AssertHelper import AssertHelper
from Common.Models.Enum.Locale import Locale
from Common.Models.Report import Report, Service, Priority

from CRS.View.ExceptionMessage import ExceptionMessage as EM


class TestCRS:

    @Report.debug(Service.CRS, Priority.p5)
    def test_endpoint(self, data):
        """
        :type data: CollectedData
        """
        self.check_response_status_code(data.response.status_code, data.response.url)

        if data.response.status_code != 200:
            return

        self.__check_airline_code_existence_in_url(data.response.content, data.response.url)
        self.__check_data_types(data.response.content, data.response.url)
        self.__check_ratings_boundaries(data.response.content, data.response.url)

        if data.request_parameter.limit:
            self.__check_limit(data.response.content, data.response.url, data.request_parameter.limit)

        if data.request_parameter.limit and data.request_parameter.page:
            self.__check_pagination(data.response.content, data.response.url, data.request_parameter)

        if data.request_parameter.sorter.type_:
            self.__check_sorting(data.response.content, data.response.url, data.request_parameter.sorter.order)

        if data.request_parameter.filter_.type_:
            self.__check_filtering(data.response.content, data.response.url, data.request_parameter.filter_.value)

        if data.request_parameter.locale != Locale.pl_PL.value:
            self.__check_translated_review(data.response.content, data.response.url, data.request_parameter.locale)

    @Report.debug(Service.CRS, Priority.p5)
    def test_internal_reviews_endpoint(self, data):
        """
        :type data: CollectedData
        """
        self.check_response_status_code(data.response.status_code, data.response.url)

        if data.response.status_code != 200:
            return

        if data.endpoint != Endpoint.internal_reviews_endpoint_get:
            self.__check_data_types(data.response.content, data.response.url)
        else:
            self.__check_review_ids_correspondence(data.response.content, data.response.url)

        if data.request_parameter.filter_.type_:
            if data.request_parameter.filter_.type_ != FilterType.BOOKING_ID:
                self.__check_filtering(data.response.content, data.response.url, data.request_parameter.filter_.value)
            if data.request_parameter.filter_.type_ == FilterType.BOOKING_ID:
                self.__check_filtering_by_booking_id(
                    data.response.content, data.response.url, data.request_parameter.filter_.value)

        if data.request_parameter.sorter.type_:
            self.__check_sorting(data.response.content, data.response.url, data.request_parameter.sorter.order)

    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def test_response_with_exceeded_pagination(self, data, endpoint):
        """
        :type data: CollectedData
        :type endpoint: Endpoint
        """
        self.check_response_status_code(data.response.status_code, data.response.url)

        if data.response.status_code != 200:
            return

        response_element = "reviews_stats" if endpoint in [
            Endpoint.airports_stats_endpoint, Endpoint.airlines_stats_endpoint
        ] else "reviews"
        AssertHelper.assert_lists_equal(data.response.content.get(response_element), [],
                                        EM.UNEXPECTED_ERROR.format(url=data.response.url))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def check_response_status_code(status_code, url, expected_status_code=200):
        """
        :type status_code: int
        :type url: str
        :type expected_status_code: int
        """
        AssertHelper.assert_equal(status_code, expected_status_code, EM.INCORRECT_STATUS_CODE_EXCEPTION.format(url=url))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def test_helpful_counter(first_request_data, second_request_data, json_data, url):
        """
        :type first_request_data: CollectedData
        :type second_request_data: CollectedData
        :type json_data: dict
        :type url: str
        """
        AssertHelper.assert_less(
            first_request_data.response.content.get("helpful"), second_request_data.response.content.get("helpful"),
            EM.HELPFUL_COUNTER_MALFUNCTION
        )
        AssertHelper.assert_equal(first_request_data.response.content.get("id"), json_data.get("id"),
                                  EM.INCORRECT_FIELD_VALUE.format(field="id", url=url))
        AssertHelper.assert_equal(first_request_data.response.content.get("objectId"),
                                  json_data.get("objectId"),
                                  EM.INCORRECT_FIELD_VALUE.format(field="objectId", url=url))

    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def test_stats_endpoint(self, data, endpoint):
        """
        :type data: CollectedData
        :type endpoint: Endpoint
        """
        self.check_response_status_code(data.response.status_code, data.response.url)

        if data.response.status_code != 200:
            return

        object_type = ObjectType.airports if endpoint == Endpoint.airports_stats_endpoint else ObjectType.airlines
        AssertHelper.assert_equal(data.response.content.get("objectType"), object_type, EM.INCORRECT_FIELD_VALUE.format(
            field="objectType", url=data.response.url))
        AssertHelper.assert_equal(ceil(data.response.content.get("total") / data.response.content.get("limit")),
                                  data.response.content.get("totalPages"),
                                  EM.INCORRECT_FIELD_VALUE.format(field="totalPages", url=data.response.url))
        for stat in data.response.content.get("reviews_stats"):
            AssertHelper.assert_not_is_none(stat.get("objectId"),
                                            EM.INCORRECT_FIELD_VALUE.format(field="objectId", url=data.response.url))
            AssertHelper.assert_not_is_none(stat.get("objectType"),
                                            EM.INCORRECT_FIELD_VALUE.format(field="objectType", url=data.response.url))
            AssertHelper.assert_not_is_none(stat.get("objectName"),
                                            EM.INCORRECT_FIELD_VALUE.format(field="objectName", url=data.response.url))
            AssertHelper.assert_not_is_none(stat.get("total"),
                                            EM.INCORRECT_FIELD_VALUE.format(field="total", url=data.response.url))
            AssertHelper.assert_not_is_none(stat.get("rating"),
                                            EM.INCORRECT_FIELD_VALUE.format(field="rating", url=data.response.url))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __check_filtering(data, url, filter_value):
        """
        :type data: dict[str, str] | dict[str, int] | dict[str, list[str]]
        :type url: str
        :type filter_value: Enum
        """
        ratings = [item.get("rating") for item in data.get("reviews")]
        for rating in ratings:
            AssertHelper.assert_in(rating, filter_value.value, EM.FILTERING_MALFUNCTION.format(url=url))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __check_filtering_by_booking_id(data, url, filter_value):
        """
        :type data: dict
        :type url: str
        :type filter_value: str
        """
        AssertHelper.assert_greater_equal(
            len(data.get("reviews")), 1, EM.FILTERING_BY_BOOKING_ID_NOT_FOUND_EXCEPTION.format(booking_id=filter_value, url=url))
        for review in data.get("reviews"):
            AssertHelper.assert_equal(
                review.get("bookingId"),
                filter_value,
                EM.FILTERING_BY_BOOKING_ID_EXCEPTION.format(booking_id=filter_value, url=url, id=review.get("id")))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __check_sorting(data, url, sort_order):
        """
        :type data: dict
        :type url: str
        :type sort_order: SortOrder
        """
        ratings = [item.get("rating") for item in data.get("reviews")]
        if sort_order == SortOrder.ASCENDING:
            AssertHelper.assert_lists_equal(ratings, sorted(ratings), EM.ASCENDING_SORT_MALFUNCTION.format(url=url))
        elif sort_order == SortOrder.DESCENGING:
            AssertHelper.assert_lists_equal(ratings, sorted(ratings, reverse=True),
                                            EM.DESCENDING_SORT_MALFUNCTION.format(url=url))
        else:
            raise Exception(EM.SORT_MALFUNCTION.format(url=url))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __check_pagination(content, url, request_parameter):
        """
        :type content: dict
        :type url: str
        :type request_parameter: RequestParameter
        """
        AssertHelper.assert_equal(content.get("totalPages"), ceil(content.get("total") / int(request_parameter.limit)),
                                  EM.INCORRECT_FIELD_VALUE.format(url=url, field="totalPages"))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __check_limit(data, url, limit):
        """
        :type data: dict
        :type url: str
        :type limit: int
        """
        AssertHelper.assert_equal(
            data.get("limit"), int(limit), EM.INCORRECT_FIELD_VALUE.format(url=url, field="limit"))
        if data.get("total") > int(limit) and data.get("page") < data.get("totalPages"):
            AssertHelper.assert_equal(len(data.get("reviews")), int(limit), EM.LIMIT_MALFUNCTION.format(url=url))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __check_airline_code_existence_in_url(content, url):
        """
        :type content: dict
        :type url: str
        """
        AssertHelper.assert_in(
            content.get("objectId"), url, EM.MISSING_AIRLINE_CODE_IN_URL.format(url=url, code=content.get("objectId")))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __check_translated_review(content, url, locale):
        """
        :type content: dict
        :type url: str
        :type locale: str
        """
        for review in content.get("reviews"):
            AssertHelper.assert_in(
                review.get("translation").get("language").lower(), locale, EM.LANGUAGE_NOT_FOUND_IN_TRANSLATION.format(
                    url=url,
                    locale=locale
                ))
            AssertHelper.assert_not_is_none(
                review.get("translation").get("title"), EM.TITLE_NOT_FOUND_IN_TRANSLATION.format(
                    url=url,
                    locale=locale
                ))
            AssertHelper.assert_not_is_none(
                review.get("translation").get("content"), EM.CONTENT_NOT_FOUND_IN_TRANSLATION.format(
                    url=url,
                    locale=locale
                ))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    def __check_review_ids_correspondence(content, url):
        """
        :type content: dict
        :type url: str
        """
        AssertHelper.assert_in(
            str(content.get("id")), url, EM.INCORRECT_REVIEW_ID_EXCEPTION.format(url=url, review_id=content.get("id")))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __check_ratings_boundaries(data, url):
        """
        :type data: dict
        :type url: str
        """
        AssertHelper.assert_greater_equal(data.get("rating"), 1, EM.INCORRECT_RATING_VALUE_EXCEPTION.format(
            url=url, rating=data.get("rating")))
        AssertHelper.assert_less_equal(data.get("rating"), 10, EM.INCORRECT_RATING_VALUE_EXCEPTION.format(
            url=url, rating=data.get("rating")))
        for rating in data.get("categoryRatings"):
            AssertHelper.assert_greater_equal(rating.get("value"), 1, EM.INCORRECT_RATING_VALUE_EXCEPTION.format(
                url=url, rating=rating.get("value")))
            AssertHelper.assert_less_equal(rating.get("value"), 10, EM.INCORRECT_RATING_VALUE_EXCEPTION.format(
                url=url, rating=rating.get("value")))
        for review in data.get("reviews"):
            for rating in review.get("categoryRatings"):
                AssertHelper.assert_greater_equal(
                    rating.get("value"), 1, EM.INCORRECT_RATING_VALUE_EXCEPTION.format(
                        url=url, rating=rating.get("value")))
                AssertHelper.assert_less_equal(
                    rating.get("value"), 10, EM.INCORRECT_RATING_VALUE_EXCEPTION.format(
                        url=url, rating=rating.get("value")))

    @staticmethod
    @Report.debug(Service.CRS, Priority.p5)
    @TestWrapper.get_exceptions_collection
    def __assert_type(data, keys, url, value_type):
        for key in keys:
            if value_type != numbers.Number:
                AssertHelper.assert_equal(type(data.get(key)), value_type, EM.INCORRECT_DATA_TYPE.format(
                    url=url, field=key))
            else:
                AssertHelper.assert_true(isinstance(data.get(key), numbers.Number), EM.INCORRECT_DATA_TYPE.format(
                    url=url, field="value"))

    @classmethod
    @Report.debug(Service.CRS, Priority.p5)
    def __check_data_types(cls, content, url):
        """
        :type content: dict
        :type url: str
        """
        if content.get("objectType") == ObjectType.airlines:
            cls.__check_data_types_of_airlines_subjects(content, url)

    @classmethod
    def __check_data_types_of_airlines_subjects(cls, data, url):
        """
        :type data: dict
        :type url: str
        """
        for rating in data.get("categoryRatings"):
            cls.__assert_type(rating, ["name"], url, str)
            cls.__assert_type(rating, ["value"], url, numbers.Number)
        cls.__assert_type(data, ["objectType", "limit", "page", "total", "totalPages"], url, int)
        cls.__assert_type(data, ["categoryRatings", "reviews"], url, list)
        cls.__assert_type(data, ["objectId"], url, str)
        cls.__assert_type(data, ["rating"], url, numbers.Number)
        for review in data.get("reviews"):
            cls.__assert_type(review, ["id", "createdAt", "objectType"], url, int)
            cls.__assert_type(review, ["rating"], url, numbers.Number)
            cls.__assert_type(review, ["title", "content", "username", "language", "countryCode", "objectId"], url, str)
            for rating in review.get("categoryRatings"):
                cls.__assert_type(rating, ["name"], url, str)
                cls.__assert_type(rating, ["value"], url, numbers.Number)

#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os
import yaml
import random

from CRS.Model.Enum.APIVersion import APIVersion
from CRS.Model.Enum.FilterType import FilterType
from CRS.Model.Enum.SortType import SortType
from Common.Helpers.URLHelper import URLHelper
from Common.Settings.CRSSettings import CRSSettings
from Common.Models.Report import Report, Service, Priority

from CRS.Model.CRSModel import CRSModel
from CRS.Model.Enum.Endpoint import Endpoint

from CRS.Test.TestEndpoint.TestCRS import TestCRS


class CRSController:

    def __init__(self, settings):
        """
        :type settings: CRSSettings
        """
        self.__test = TestCRS()
        self.__config = self.get_config()
        self.__model = CRSModel(settings, self.__config)
        self.__settings = settings

    @staticmethod
    def get_config():
        """
        :rtype: dict
        """
        config_file_path = os.path.join(
            os.path.dirname(__file__), "Config", "CRSEndpointConfig.yml")
        endpoint_config = yaml.load(open(config_file_path))
        return endpoint_config

    # region Public API
    def handle_airline_endpoint(self):
        self.__handle_test_of_the_airline_endpoint_without_parameters()
        self.__handle_test_of_the_airline_endpoint_with_optional_parameters()
        self.__handle_test_of_the_airline_endpoint_with_sorting_by_rating()
        self.__handle_test_of_the_airline_endpoint_with_filtering_by_rating()
        self.__handle_test_of_the_airline_endpoint_with_wrong_airline_code()
        # Former API version tests (deprecated)
        self.__handle_test_of_the_airline_endpoint_without_parameters(api_version=APIVersion.PUBLIC_PREVIOUS)
        self.__handle_test_of_the_airline_endpoint_with_optional_parameters(api_version=APIVersion.PUBLIC_PREVIOUS)
        self.__handle_test_of_the_airline_endpoint_with_sorting_by_rating(api_version=APIVersion.PUBLIC_PREVIOUS)
        self.__handle_test_of_the_airline_endpoint_with_filtering_by_rating(api_version=APIVersion.PUBLIC_PREVIOUS)
        self.__handle_test_of_the_airline_endpoint_with_wrong_airline_code(api_version=APIVersion.PUBLIC_PREVIOUS)

    def handle_airport_endpoint(self):
        self.__handle_test_of_the_airport_endpoint_without_parameters()
        self.__handle_test_of_the_airport_endpoint_with_filtering_by_rating()
        self.__handle_test_of_the_airport_endpoint_with_sorting_by_rating()
        self.__handle_test_of_the_airport_endpoint_with_wrong_airport_code()
        # Former API version tests (deprecated)
        self.__handle_test_of_the_airport_endpoint_without_parameters(api_version=APIVersion.PUBLIC_PREVIOUS)
        self.__handle_test_of_the_airport_endpoint_with_filtering_by_rating(api_version=APIVersion.PUBLIC_PREVIOUS)
        self.__handle_test_of_the_airport_endpoint_with_sorting_by_rating(api_version=APIVersion.PUBLIC_PREVIOUS)
        self.__handle_test_of_the_airport_endpoint_with_wrong_airport_code(api_version=APIVersion.PUBLIC_PREVIOUS)

    def handle_helpful_endpoint(self):
        self.__handle_test_of_the_helpful_endpoint()

    def handle_airports_stats_endpoint(self):
        self.__handle_test_of_the_stats_endpoint(Endpoint.airports_stats_endpoint)
        self.__handle_test_of_the_stats_endpoint_with_pagination(Endpoint.airports_stats_endpoint)
        self.__handle_test_of_the_stats_endpoint_with_exceeded_pagination(Endpoint.airports_stats_endpoint)
        self.__handle_test_of_the_stats_endpoint_with_search(Endpoint.airports_stats_endpoint)

    def handle_airlines_stats_endpoint(self):
        self.__handle_test_of_the_stats_endpoint(Endpoint.airlines_stats_endpoint)
        self.__handle_test_of_the_stats_endpoint_with_pagination(Endpoint.airlines_stats_endpoint)
        self.__handle_test_of_the_stats_endpoint_with_exceeded_pagination(Endpoint.airlines_stats_endpoint)
        self.__handle_test_of_the_stats_endpoint_with_search(Endpoint.airlines_stats_endpoint)
    # endregion

    # region Internal API
    def handle_internal_review_endpoint(self):
        self.__handle_internal_endpoint_filtering_by_bookingid()
        self.__handle_test_of_the_internal_review_endpoint_for_post_request()
        self.__handle_test_of_the_internal_review_endpoint_for_list_of_reviews_with_filtering()
        self.__handle_test_of_the_internal_review_endpoint_for_list_of_reviews_with_sorting_by_rating()
        self.__handle_test_of_the_internal_review_endpoint_for_single_review()
        self.__handle_test_of_the_internal_review_endpoint_for_single_review_with_wrong_id()
        self.__handle_test_of_the_internal_review_endpoint_for_list_of_reviews_with_exceeded_pagination()

    def handle_internal_status_endpoint(self):
        self.__handle_test_of_the_internal_status_endpoint()
        self.__handle_test_of_the_internal_status_endpoint_with_wrong_credentials()
    # endregion

    # region AirportEndpoint
    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airport_endpoint_without_parameters(self, api_version=None):
        collected_data = self.__model.get_collected_data(Endpoint.airport_endpoint, api_version=api_version)
        self.__test.test_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airport_endpoint_with_filtering_by_rating(self, api_version=None):
        filter_ = self.__model.choose_filter()
        collected_data = self.__model.get_collected_data(Endpoint.airport_endpoint, api_version=api_version,
                                                         filter_=filter_)
        self.__test.test_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airport_endpoint_with_sorting_by_rating(self, api_version=None):
        sorter = self.__model.choose_sorter(type_=SortType.RATING)
        collected_data = self.__model.get_collected_data(Endpoint.airport_endpoint, api_version=api_version,
                                                         sorter=sorter)
        self.__test.test_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airport_endpoint_with_wrong_airport_code(self, api_version=None):
        collected_data = self.__model.get_collected_data(Endpoint.airport_endpoint, api_version=api_version,
                                                         airport_code="WRONG_CODE")
        self.__test.check_response_status_code(
            collected_data.response.status_code, collected_data.response.url, expected_status_code=404)
    # endregion

    # region InternalReviewEndpoint
    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_internal_review_endpoint_for_single_review(self):
        collected_data = self.__model.get_collected_data(Endpoint.internal_reviews_endpoint_get)
        self.__test.test_internal_reviews_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_internal_review_endpoint_for_single_review_with_wrong_id(self):
        """
        In case of wrong parameter `review_id` either not found or wrong (random string) app should return 404, not 5xx
        """
        collected_data = self.__model.get_collected_data(Endpoint.internal_reviews_endpoint_get, review_id=9999999)
        self.__test.check_response_status_code(
            collected_data.response.status_code, collected_data.response.url, expected_status_code=404)
        collected_data = self.__model.get_collected_data(Endpoint.internal_reviews_endpoint_get, review_id="wrong_id")
        self.__test.check_response_status_code(
            collected_data.response.status_code, collected_data.response.url, expected_status_code=404)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_internal_review_endpoint_for_list_of_reviews_with_sorting_by_rating(self):
        sorter = self.__model.choose_sorter(type_=SortType.RATING)
        collected_data = self.__model.get_collected_data(Endpoint.internal_reviews_endpoint_list, sorter=sorter)
        self.__test.test_internal_reviews_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_internal_review_endpoint_for_list_of_reviews_with_filtering(self):
        filter_ = self.__model.choose_filter()
        collected_data = self.__model.get_collected_data(Endpoint.internal_reviews_endpoint_list, filter_=filter_)
        self.__test.test_internal_reviews_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_internal_endpoint_filtering_by_bookingid(self):
        """
        Handles filtering internal reviews endpoint list by bookingId
        """
        filter_ = self.__model.choose_filter(
            type_=FilterType.BOOKING_ID, value=random.choice(self.__config.get("booking_id")))
        collected_data = self.__model.get_collected_data(Endpoint.internal_reviews_endpoint_list, filter_=filter_)
        self.__test.test_internal_reviews_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_internal_review_endpoint_for_list_of_reviews_with_exceeded_pagination(self):
        endpoint = Endpoint.internal_reviews_endpoint_list
        page = self.__model.choose_page(endpoint, 1, 999999)
        collected_data = self.__model.get_collected_data(endpoint, page=page)
        self.__test.test_response_with_exceeded_pagination(collected_data, endpoint)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_internal_review_endpoint_for_post_request(self, api_version=None):
        app_url = URLHelper.get_url(self.__config.get("app_url"), self.__settings.environment, self.__settings.branch)

        if URLHelper.is_pro_url(app_url):
            return  # Prevents tests on production

        # Code below shouldn't be called on production (until fake review in reviews will be provided).
        # POST affects on database
        collected_data = self.__model.get_collected_data(
            Endpoint.internal_reviews_endpoint, api_version=api_version, method="POST", is_auth_required=True)
        self.__test.check_response_status_code(collected_data.response.status_code,
                                               collected_data.response.url)

    # endregion

    # region InternalStatusEndpoint
    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_internal_status_endpoint(self):
        collected_data = self.__model.get_collected_data(Endpoint.internal_endpoint_status, is_auth_required=True)
        self.__test.check_response_status_code(collected_data.response.status_code, collected_data.response.url)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_internal_status_endpoint_with_wrong_credentials(self):
        collected_data = self.__model.get_collected_data(Endpoint.internal_endpoint_status)
        self.__test.check_response_status_code(
            collected_data.response.status_code, collected_data.response.url, expected_status_code=401)
    # endregion

    # region AirlineEndpoint
    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airline_endpoint_without_parameters(self, api_version=None):
        collected_data = self.__model.get_collected_data(Endpoint.airline_endpoint, api_version=api_version)
        self.__test.test_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airline_endpoint_with_optional_parameters(self, api_version=None):
        limit = self.__model.choose_limit()
        page = self.__model.choose_page(Endpoint.airline_endpoint, limit)
        collected_data = self.__model.get_collected_data(Endpoint.airline_endpoint, api_version=api_version,
                                                         limit=limit, page=page)
        self.__test.test_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airline_endpoint_with_sorting_by_rating(self, api_version=None):
        sorter = self.__model.choose_sorter(type_=SortType.RATING)
        limit = self.__model.choose_limit()
        page = self.__model.choose_page(Endpoint.airline_endpoint, limit)
        collected_data = self.__model.get_collected_data(
            Endpoint.airline_endpoint, api_version=api_version, sorter=sorter, limit=limit, page=page)
        self.__test.test_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airline_endpoint_with_filtering_by_rating(self, api_version=None):
        filter_ = self.__model.choose_filter()
        limit = self.__model.choose_limit()
        page = self.__model.choose_page(Endpoint.airline_endpoint, limit)
        collected_data = self.__model.get_collected_data(
            Endpoint.airline_endpoint, api_version=api_version, filter_=filter_, limit=limit, page=page)
        self.__test.test_endpoint(collected_data)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_airline_endpoint_with_wrong_airline_code(self, api_version=None):
        collected_data = self.__model.get_collected_data(Endpoint.airline_endpoint, api_version=api_version,
                                                         airline_code="WRONG_CODE")
        self.__test.check_response_status_code(
            collected_data.response.status_code, collected_data.response.url, expected_status_code=404)
    # endregion

    # region Helpful Counter
    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_helpful_endpoint(self, api_version=None):
        collected_data = self.__model.get_collected_data(Endpoint.helpful_endpoint, api_version=api_version)
        self.__test.check_response_status_code(
            collected_data.response.status_code, collected_data.response.url, expected_status_code=405
        )

        app_url = URLHelper.get_url(self.__config.get("app_url"), self.__settings.environment, self.__settings.branch)

        if URLHelper.is_pro_url(app_url):
            return  # Prevents tests on production

        # Code below shouldn't be called on production (until fake review in reviews will be provided).
        # PUT affects on database
        collected_data_for_method_put = self.__model.get_collected_data(
            Endpoint.helpful_endpoint, api_version=api_version, method="PUT")
        self.__test.check_response_status_code(collected_data_for_method_put.response.status_code,
                                               collected_data_for_method_put.response.url)
        next_collected_data_for_method_put = self.__model.get_collected_data(
            Endpoint.helpful_endpoint, api_version=api_version, method="PUT")
        self.__test.test_helpful_counter(collected_data_for_method_put, next_collected_data_for_method_put,
                                         self.__config.get("json_data"),
                                         collected_data_for_method_put.response.url)
    # endregion

    # region Airports&Airlines Stats Endpoint
    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_stats_endpoint(self, endpoint, api_version=None):
        """
        :type endpoint: Endpoint
        :type api_version: APIVersion | None
        """
        collected_data = self.__model.get_collected_data(endpoint, api_version=api_version)
        self.__test.test_stats_endpoint(collected_data, endpoint)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_stats_endpoint_with_pagination(self, endpoint, api_version=None):
        """
        :type endpoint: Endpoint
        :type api_version: APIVersion | None
        """
        limit = self.__model.choose_limit()
        page = self.__model.choose_page(endpoint, limit)
        collected_data = self.__model.get_collected_data(endpoint, api_version=api_version, page=page, limit=limit)
        self.__test.test_stats_endpoint(collected_data, endpoint)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_stats_endpoint_with_exceeded_pagination(self, endpoint, api_version=None):
        """
        :type endpoint: Endpoint
        :type api_version: APIVersion | None
        """
        collected_data = self.__model.get_collected_data(endpoint, api_version=api_version, page=9999999)
        self.__test.test_response_with_exceeded_pagination(collected_data, endpoint)

    @Report.debug(Service.CRS, Priority.p5)
    def __handle_test_of_the_stats_endpoint_with_search(self, endpoint, api_version=None):
        if endpoint == Endpoint.airports_stats_endpoint:
            filter_ = self.__model.choose_filter(
                type_=FilterType.AIRPORT_NAME,
                value="kra"
            )
        else:
            filter_ = self.__model.choose_filter(
                type_=FilterType.AIRLINE_NAME,
                value="air"
            )
        collected_data = self.__model.get_collected_data(endpoint, api_version=api_version, filter_=filter_)
        self.__test.test_stats_endpoint(collected_data, endpoint)
    # endregion

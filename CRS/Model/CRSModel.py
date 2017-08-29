#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import json
import random
import re
import uuid
from math import ceil
from urllib.parse import urljoin

import requests
from requests.exceptions import SSLError, RequestException

from CRS.Model.Entity.CollectedData import CollectedData
from CRS.Model.Entity.Filter import Filter
from CRS.Model.Entity.RequestParameter import RequestParameter
from CRS.Model.Entity.ResponseData import ResponseData
from CRS.Model.Entity.Sorter import Sorter
from CRS.Model.Enum.APIVersion import APIVersion
from CRS.Model.Enum.Endpoint import Endpoint
from CRS.Model.Enum.Filter.Rating import Rating
from CRS.Model.Enum.FilterType import FilterType
from CRS.Model.Enum.SortOrder import SortOrder
from CRS.Model.Enum.SortType import SortType
from CRS.View.ExceptionMessage import ExceptionMessage
from Common.Helpers.URLHelper import URLHelper
from Common.Models.Enum.Cookie.EskySrv import EskySrv
from Common.Models.Report import Report, Service, Priority
from Common.Settings.CRSSettings import CRSSettings


class CRSModel:

    def __init__(self, settings, config):
        """
        :type settings: CRSSettings
        :type config: dict
        """
        self.__settings = settings
        self.__config = config

        self.__filter = Filter()
        self.__sorter = Sorter()

    @Report.debug(Service.CRS, Priority.p5)
    def get_collected_data(self, endpoint, api_version=None, method="GET", filter_=None, sorter=None, limit=None,
                           page=None, is_auth_required=False, review_id=None, airport_code=None, airline_code=None):
        """
        Gets response data alongside with used parameters and additional data stored in proper entities
        :type endpoint: Endpoint
        :type api_version: APIVersion
        :type method: str
        :type filter_: Filter | None
        :type sorter: Sorter | None
        :type limit: int | None
        :type page: int | None
        :type is_auth_required: bool
        :type review_id: int | str | None
        :type airport_code: str | None
        :type airline_code: str | None
        :rtype: CollectedData
        """
        request_parameter = RequestParameter(
            locale=self.__settings.locale,
            limit=str(limit) if limit else "",
            page=str(page) if page else "",
            filter_=self.__filter if not filter_ else filter_,
            sorter=self.__sorter if not sorter else sorter,
            review_id=review_id,
            airport_code=airport_code,
            airline_code=airline_code
        )

        return CollectedData(
            response=self.__get_response(
                endpoint, api_version=api_version, method=method, request_parameter=request_parameter,
                is_auth_required=is_auth_required),
            endpoint=endpoint,
            request_parameter=request_parameter
        )

    @Report.debug(Service.CRS, Priority.p5)
    def choose_filter(self, type_=FilterType.RATING, value=None):
        """
        :type type_: FilterType
        :type value: Rating | str| None
        :rtype: Filter
        """
        filter_ = Filter(
            type_=type_,
            value=self.__draw_filtering(value)
        )
        return filter_

    @Report.debug(Service.CRS, Priority.p5)
    def choose_sorter(self, type_=None, order=None):
        """
        :type type_: SortType
        :type order: SortOrder
        :rtype: Sorter
        """
        sorter = Sorter(
            type_=type_,
            order=self.__draw_sorting(order)
        )
        return sorter

    @Report.debug(Service.CRS, Priority.p5)
    def choose_limit(self):
        """
        :rtype: int
        """
        limit = random.randint(1, self.__config.get("max_reviews_limit") + 1)
        return limit

    @Report.debug(Service.CRS, Priority.p5)
    def choose_page(self, endpoint, limit, page=None):
        """
        Returns a `page` parameter value related to total amount of reviews
        :type endpoint: Endpoint
        :type limit: int
        :type page: int | None
        :rtype: int
        """
        try:
            result = page or ceil(random.randint(1, self.__get_total_reviews(endpoint) + 1) / limit)
            return result
        except (TypeError, ZeroDivisionError) as e:
            raise ExceptionMessage.DETERMINING_PAGE_PARAMETER_ERROR.format(exception=e)

    @Report.debug(Service.CRS, Priority.p5)
    def __get_response(self, endpoint, api_version, method, **params):
        """
        :type endpoint: Endpoint
        :type api_version: str
        :type method: str
        :type params: dict
        :rtype: ResponseData
        """
        url = self.__prepare_request_url(
            endpoint=endpoint,
            api_version=api_version,
            params=params
        )
        auth = (
            self.__config.get("auth_login"), self.__config.get("auth_pass")) if params.get("is_auth_required") else ""
        response = self.__do_request(url=url, cookies=self.__get_cookies(), auth=auth, method=method)
        return response

    @Report.debug(Service.CRS, Priority.p5)
    def __get_cookies(self):
        """
        :rtype: dict
        """
        cookies = {}
        cookies.update(eskyver=self.__settings.eskyver)
        cookies.update(eskysrv=self.__settings.eskysrv) if self.__settings.eskysrv != EskySrv.ABS else ""
        return cookies

    @Report.debug(Service.CRS, Priority.p5)
    def __get_total_reviews(self, endpoint):
        """
        Return total amount of reviews for given (randomly selected) airline code
        :type endpoint: Endpoint
        :rtype: int | None
        """
        data = self.get_collected_data(endpoint, limit=1, page=1)

        if not data.response.content:
            return

        total = data.response.content.get("total")
        return total

    @Report.debug(Service.CRS, Priority.p5)
    def __prepare_request_url(self, endpoint, api_version, params):
        """
        :type endpoint: Endpoint
        :type api_version: str
        :type params: dict
        :rtype: str
        """
        app_url = self.__config.get("app_url")
        request_parameter = params.get("request_parameter")
        try:
            sorting = request_parameter.sorter.type_
        except AttributeError:
            sorting = None
        try:
            filtering = request_parameter.filter_.type_
        except AttributeError:
            filtering = None
        sorting_parameters = self.__config.get("sorting") if sorting else ""
        filtering_parameters = self.__config.get("filtering") if filtering else ""
        if endpoint == Endpoint.internal_reviews_endpoint_get:
            endpoint_url = self.__config.get(endpoint)
        else:
            endpoint_url = "{0}{1}{2}".format(self.__config.get(endpoint), sorting_parameters, filtering_parameters)
        url = urljoin(
            URLHelper.get_url(
                pro_url=app_url,
                environment=self.__settings.environment,
                branch=self.__settings.branch),
            endpoint_url
        )
        url = self.__replace_api_version(url, api_version)
        return self.__fill_url_placeholders(url, request_parameter)

    @Report.debug(Service.CRS, Priority.p5)
    def __replace_api_version(self, url, api_version):
        """
        :type url: str
        :type api_version: str
        :rtype: str
        """
        pattern = "\/(?P<api_version>v{1}\d.{1}\d)"
        search = re.search(pattern, url).group("api_version")
        result = url.replace(search, api_version) if api_version else url
        return result

    @Report.debug(Service.CRS, Priority.p5)
    def __fill_url_placeholders(self, url, request_parameter):
        """
        :type url: str
        :type request_parameter: RequestParameter
        :rtype: str
        """
        if not request_parameter:
            raise Exception(ExceptionMessage.OPTIONAL_PARAMETER_OBJECT_MALFUNCTION)

        try:
            if request_parameter.filter_.type_ == FilterType.RATING:
                filter_value = "{0}:{1}".format(
                    request_parameter.filter_.value.value[0], request_parameter.filter_.value.value[-1])
            else:
                filter_value = "{0}".format(request_parameter.filter_.value)
        except AttributeError:
            filter_value = ""

        result = url.format(
            code=request_parameter.airline_code or self.__draw_airline_code(),
            airport_code=request_parameter.airport_code or self.__draw_aiport_code(),
            page=request_parameter.page,
            limit=request_parameter.limit,
            locale=self.__settings.locale,
            sortType=request_parameter.sorter.type_,
            sortOrder=request_parameter.sorter.order,
            filterType=request_parameter.filter_.type_,
            filterValue=filter_value,
            review_id=request_parameter.review_id or self.__draw_review_id()
        )
        return result

    def __do_request(self, url, cookies, auth=False, verify=False, method="GET"):
        """
        :type url: str
        :type verify: bool
        :type auth: tuple
        :type method: str
        :rtype: ResponseData
        """
        try:
            if method == "GET":
                response = requests.get(url=url, cookies=cookies, auth=auth, verify=verify)
                return ResponseData(response)
            elif method == "PUT":
                response = requests.put(url=url, data=self.__config.get("json_data"),
                                        cookies=cookies, auth=auth, verify=verify)
                return ResponseData(response)
            elif method == "POST":
                json_to_post = self.__config.get("airline_review_addition")
                booking_id = json_to_post.get("bookingId").format(unique_part=str(uuid.uuid4())[:8].upper())
                json_to_post["bookingId"] = booking_id
                data = json.dumps(json_to_post)
                response = requests.post(url=url, data=data, cookies=cookies, auth=auth, verify=verify)
                return ResponseData(response)
        except SSLError as e:
            raise SSLError(ExceptionMessage.INSECURE_CONNECTION_ON_PRO_ENV.format(exception=e.args))
        except RequestException:
            raise RequestException(ExceptionMessage.NOT_ESTABLISHED_CONNECTION.format(endpoint=url))

    @Report.debug(Service.CRS, Priority.p5)
    def __draw_airline_code(self):
        """
        :rtype: str
        """
        airline_code = random.choice(self.__config.get("airline_code"))
        self.__airline_code = airline_code
        return airline_code

    @Report.debug(Service.CRS, Priority.p5)
    def __draw_review_id(self):
        """
        Randomly chooses review id from the list of review's ids containing reviews defined in CRSEndpointConfig.yml
        :rtype: str
        """
        review_id = random.choice(self.__config.get("review_id"))
        return review_id

    @Report.debug(Service.CRS, Priority.p5)
    def __draw_aiport_code(self):
        """
        Randomly chooses airport code from the list defined in CRSEndpointConfig.yml
        :rtype: str
        """
        airport_code = random.choice(self.__config.get("airport_code"))
        return airport_code

    @Report.debug(Service.CRS, Priority.p5)
    def __draw_filtering(self, filtering_value=None):
        """
        Returns a filtering value if argument is provided, otherwise randomly chooses the filtering value
        :type filtering_value: Rating | str | None
        :rtype: Rating | str
        """
        filtering_value = filtering_value or random.choice([value for value in Rating])
        return filtering_value

    @Report.debug(Service.CRS, Priority.p5)
    def __draw_sorting(self, order=None):
        """
        Returns an order of sorting if argument is provided, otherwise randomly chooses the sort order
        :type order: SortOrder
        :rtype: SortOrder
        """
        sorting_order = order or random.choice([SortOrder.DESCENGING, SortOrder.ASCENDING])
        return sorting_order

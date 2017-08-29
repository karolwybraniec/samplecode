#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from CRS.Model.Entity.RequestParameter import RequestParameter
from CRS.Model.Entity.ResponseData import ResponseData
from CRS.Model.Enum.Endpoint import Endpoint


class CollectedData:

    def __init__(self, response, endpoint, request_parameter):
        """
        :type response: ResponseData
        :type endpoint: Endpoint
        :type request_parameter: RequestParameter
        """
        self.response = response
        self.endpoint = endpoint
        self.request_parameter = request_parameter

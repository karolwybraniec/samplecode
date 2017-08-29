#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from requests.models import Response


class ResponseData:

    def __init__(self, response):
        """
        :type response: Response
        """
        self.__response = response

    @property
    def url(self):
        """
        :rtype: str
        """
        return self.__response.url

    @property
    def status_code(self):
        """
        :rtype: int
        """
        return self.__response.status_code

    @property
    def content(self):
        """
        :return: dict
        """
        return self.__response.json()

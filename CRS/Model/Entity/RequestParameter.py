#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from CRS.Model.Entity.Filter import Filter
from CRS.Model.Entity.Sorter import Sorter
from Common.Models.Enum.Locale import Locale


class RequestParameter:

    def __init__(self, locale, limit, page, filter_, sorter, review_id, airport_code, airline_code):
        """
        :type locale: Locale
        :type limit: str | None
        :type page: str | None
        :type filter_: Filter | None
        :type sorter: Sorter | None
        :type review_id: int | str | None
        :type airport_code: str | None
        :type airline_code: str | None
        """
        self.locale = locale
        self.limit = limit
        self.page = page
        self.filter_ = filter_
        self.sorter = sorter
        self.review_id = review_id
        self.airport_code = airport_code
        self.airline_code = airline_code

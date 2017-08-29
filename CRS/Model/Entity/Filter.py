#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from CRS.Model.Enum.Filter.Rating import Rating
from CRS.Model.Enum.FilterType import FilterType


class Filter:

    def __init__(self, type_=None, value=None):
        """
        :type type_: FilterType | None
        :type value: Rating | str | None
        """
        self.type_ = type_
        self.value = value

#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from CRS.Model.Enum.SortOrder import SortOrder
from CRS.Model.Enum.SortType import SortType


class Sorter:

    def __init__(self, type_=None, order=None):
        """
        :type type_: SortType | None
        :type order: SortOrder | None
        """
        self.type_ = type_
        self.order = order

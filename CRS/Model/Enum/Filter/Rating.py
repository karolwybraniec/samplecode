#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from enum import Enum


class Rating(Enum):

    all = [round(.1 * x, 2) for x in range(10, 51)]
    excellent = [round(.1 * x, 2) for x in range(40, 51)]
    good = [round(.1 * x, 2) for x in range(30, 40)]
    mixed = [round(.1 * x, 2) for x in range(20, 30)]
    ratherPoor = [round(.1 * x, 2) for x in range(10, 20)]

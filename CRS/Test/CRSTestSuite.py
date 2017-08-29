#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import unittest
import sys

from Common.Helpers.EnvironmentHelper import Environment, Branch
from Common.Models.Enum.Locale import Locale

from CRS.Test.CRSTestCases import CRSTestCases


def suite():

    test_suite = unittest.TestSuite()

    # test_suite.addTest(CRSTestCases("test_airline_endpoint"))
    # test_suite.addTest(CRSTestCases("test_airport_endpoint"))
    # test_suite.addTest(CRSTestCases("test_internal_status_endpoint"))
    test_suite.addTest(CRSTestCases("test_internal_review_endpoint"))
    # test_suite.addTest(CRSTestCases("test_helpful_endpoint"))
    # test_suite.addTest(CRSTestCases("test_airports_stats_endpoint"))
    # test_suite.addTest(CRSTestCases("test_airlines_stats_endpoint"))

    environment = Environment.STAGING
    branch = Branch.STABLE
    locale = Locale.pl_PL.name

    CRSTestCases.settings.environment = environment
    CRSTestCases.settings.branch = branch
    CRSTestCases.settings.locale = locale

    return test_suite

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(suite())
    sys.exit(not result.wasSuccessful())

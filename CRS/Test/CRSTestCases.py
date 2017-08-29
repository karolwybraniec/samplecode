#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import unittest
from unittest.case import TestCase

from CRS.Controller.CRSController import CRSController
from Common.Helpers.UnittestHelper import UnittestHelper
from Common.Models.Report import Service
from Common.Settings.CRSSettings import CRSSettings
from Common.Tools.EventLog.Controller.EventLogController import EventLogController


class CRSTestCases(TestCase):

    settings = CRSSettings()

    # region Setup of the Unittests
    def setUp(self):
        self.settings.test_suite = UnittestHelper.get_testsuite_name(self)

    def tearDown(self):
        EventLogController.generate(Service.CRS)
    # endregion

    def test_airline_endpoint(self):
        controller = CRSController(self.settings)
        controller.handle_airline_endpoint()

    def test_airport_endpoint(self):
        controller = CRSController(self.settings)
        controller.handle_airport_endpoint()

    def test_internal_status_endpoint(self):
        controller = CRSController(self.settings)
        controller.handle_internal_status_endpoint()

    def test_internal_review_endpoint(self):
        controller = CRSController(self.settings)
        controller.handle_internal_review_endpoint()

    def test_helpful_endpoint(self):
        controller = CRSController(self.settings)
        controller.handle_helpful_endpoint()

    def test_airports_stats_endpoint(self):
        controller = CRSController(self.settings)
        controller.handle_airports_stats_endpoint()

    def test_airlines_stats_endpoint(self):
        controller = CRSController(self.settings)
        controller.handle_airlines_stats_endpoint()

if __name__ == "__main__":
    unittest.main()

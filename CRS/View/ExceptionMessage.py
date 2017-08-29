#!/usr/bin/python3.4
# -*- coding: utf-8 -*-


class ExceptionMessage:

    HELPFUL_COUNTER_MALFUNCTION = "`helpful` field should get greater with each PUT request. After second request " \
                                  "counter hasn`t increased."
    DETERMINING_PAGE_PARAMETER_ERROR = "An error occured while trying to choose page parameter number." \
                                       " Exception stack is: {exception}"
    UNEXPECTED_ERROR = "Unexpected error occured for url {url}"
    OPTIONAL_PARAMETER_OBJECT_MALFUNCTION = "RequestOptionalParameter instance is None, so request to the API cannot " \
                                            "be done. Basically means, that something with the QA code is wrong."
    INCORRECT_REVIEW_ID_EXCEPTION = "Review ID placed in url does not correspond to id found in response`s field " \
                                    "({review_id}) for endpoint_url: {url}."
    FILTERING_MALFUNCTION = "Filtered ratings don`t fit into the range for endpoint url: {url}."
    FILTERING_BY_BOOKING_ID_NOT_FOUND_EXCEPTION = "Filtering by BookingId (bookingId: {booking_id}) returned " \
                                                  "0 results for endpoint url: {url}. For proper (meaning - " \
                                                  "there are records in db for that bookingId) bookingId`s " \
                                                  "it`s a bug."
    FILTERING_BY_BOOKING_ID_EXCEPTION = "Each review after filtering by BookingId (bookingId: {booking_id} " \
                                        "should refer to that bookingId. Issue occured on {url} for " \
                                        "review_id {id}."
    SORT_MALFUNCTION = "Sorting order parameter is mandatory in URL. Found None for endpoint url: {url}."
    ASCENDING_SORT_MALFUNCTION = "Ascending sorting doesn`t work properly for endpoint url: {url}. "
    DESCENDING_SORT_MALFUNCTION = "Descending sorting doesn`t work properly for endpoint url: {url}. "
    INCORRECT_FIELD_VALUE = "Field `{field}` has different value than expected in endpoint url: {url}."
    LIMIT_MALFUNCTION = "There is more reviews than limit states for given endpoint url {url}."
    INCORRECT_RATING_VALUE_EXCEPTION = "Rating value `{rating}` doesn't fit into the boundaries 1 >= rating <= 10.0. " \
                                       "Affected endpoint: {url}."
    INCORRECT_DATA_TYPE = "Incorrect data type of field `{field}` in url {url}."
    MISSING_AIRLINE_CODE_IN_URL = "Airline code `{code}` not found in endpoint url {url}."
    INCORRECT_STATUS_CODE_EXCEPTION = "Incorrect response status code for {url}."
    INSECURE_CONNECTION_ON_PRO_ENV = "SSL error occured. If it is production environment, then something is really " \
                                     "bad. {exception}"
    NOT_ESTABLISHED_CONNECTION = "Connection to endpoint {endpoint} was not established. " \
                                 "Check endpoint address or insecure status."
    LANGUAGE_NOT_FOUND_IN_TRANSLATION = "Language code {locale} not found in {url} review."
    TITLE_NOT_FOUND_IN_TRANSLATION = "Title field is empty for locale {locale} in {url}."
    CONTENT_NOT_FOUND_IN_TRANSLATION = "Content field is empty for locale {locale} in {url}."

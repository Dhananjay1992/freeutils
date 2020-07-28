import copy
import json
import traceback
from django.test import Client
import requests


class HTTPCoreError(Exception):
    pass


class HTTPRequests(object):
    def __init__(self, test_context, logger):

        self._url = ''
        self._requests = requests
        self._r = None
        self._logger = logger
        self._test_context = test_context
        self.service_response = {}

    def core(self, url, action, data='', files='', headers='', json_data='', ret=True, parser=None,
             response_object=True):
        """
            Abstraction of typical http events
            *http request wrapper with SSL cert verify disabled*
            :param str url: the url
            :param str action: one of the HTTP verbs (upper case)
            :param data:
            :param files:
            :param headers: additional headers besides the default one
            :param json_data: optional, json data to send
            :param response_object: optional, json data to send
            :param bool ret: optional, default True
            :param func parser:
            :return:
        """

        caller = 'N/A'
        self._logger.api_logger.info(
            {'url': url, 'api': caller, 'action': action, 'payload': {'data': data, 'json': json_data}})
        kwargs = {'verify': False}
        if headers:
            headers['Authorization'] = f"Bearer {self._test_context.auth_token}"
            kwargs.update(headers=headers)
        else:
            self._headers['Authorization'] = f"Bearer {self._test_context.auth_token}"
            kwargs.update(headers=self._headers)
        if data:
            kwargs.update(data=data)
        if files:
            kwargs.update(files=files)
        if json_data:
            kwargs.update(json=json_data)
        try:
            self._r = getattr(self.http, action.lower())(url, **kwargs)
            printable_headers = copy.deepcopy(self._headers)
            printable_headers.update(self._headers)
            printable_headers.update(headers)
            printable_headers.pop('Authorization')
            self._logger.api_logger.info(f"headers: {printable_headers}")
            return (self._r if response_object else parser(self.response_json) if parser else self.response_json) \
                if ret else None
        except Exception as e:
            printable_headers = copy.deepcopy(self._headers)
            printable_headers.update(self._headers)
            printable_headers.update(headers)
            printable_headers.pop('Authorization')
            self._logger.api_logger.error(f"headers: {printable_headers}")
            self._logger.api_logger.error({'short_message': 'http error', 'error': e})
            raise RuntimeError('http agent core => http error')

    def dispatcher(self, url, data, action, use_json=True, response_object=True):
        """

        :param data:
        :param action:
        :param headers:
        :param use_json:
        :param response_object: True if wanted to return the whole response object
        :return:
        """
        try:
            if use_json:
                self.service_response = self.core(url, action=action, data=json.dumps(data), headers=self._headers)
            else:
                self.service_response = self.core(url, action=action, data=data, headers=self._headers,
                                                  response_object=response_object)
            self._logger.api_logger.info(self.service_response)
        except (KeyError, ValueError, RuntimeError) as e:
            self.service_response = {}
            self._logger.api_logger.error(traceback.format_exc())
        return self.service_response

    @staticmethod
    def is_xml(text):
        return text.startswith('<?xml')

    @property
    def response(self):
        """
            :return: @property -- a response object from a request
        """
        return self._r

    @property
    def response_message(self):
        """
            :return: @property -- a response object from a request
        """
        return self._r.text

    @property
    def response_headers(self):
        return self.response.headers

    @property
    def status_code(self):
        # refer to http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        return self.response.status_code

    @property
    def response_json(self):
        """
            the json data from http response if applicable, otherwise return False
        """
        try:
            return self.response.json()
        except ValueError:
            if self.is_xml(self.response.text):
                return self.load_xml_data(self.response.text)
                # return json.loads(json.dumps(xmltodict.parse(self.response.text)))
            return {}

    @property
    def session(self):
        """
            a requests module or a session created by requests

            * http => a requests module
            * https => a session with a valid login user
        """
        return self._http

    @property
    def http(self):
        """
            back compatibility with runtime
        """
        return self._http

    @property
    def response_content(self):
        """
        :return: returns the response content
        """
        return self.response.content

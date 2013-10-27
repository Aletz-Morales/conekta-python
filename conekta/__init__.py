#!/usr/bin/python
#coding: utf-8
#(c) 2013 Julian Ceballos <@jceb>

import base64
import inspect
import urllib
from httplib2 import Http

try:
    import json
except ImportError:
    import simplejson as json

API_VERSION = '0.2.0'

__version__ = '0.6'
__author__ = 'Julian Ceballos'

API_BASE = 'https://api.conekta.io/'

HEADERS = {
    'Accept': 'application/vnd.conekta-v%s+json' % (API_VERSION),
    'Content-type': 'application/json'
}

api_key = ''

class ConektaError(Exception):
  def __init__(self, error_json):
      super(ConektaError, self).__init__(error_json)
      self.error_json = error_json

class _Resource(object):
    def __init__(self, attributes):
        self.construct_from(attributes)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    @classmethod
    def build_request(cls, method, path, params):
        HEADERS['Authorization'] = 'Basic %s' % (base64.b64encode(api_key + ':'))
        absolute_url = API_BASE + path
        request = Http({}).request
        if method == 'GET':
            url = "%s?%s" % (absolute_url, urllib.urlencode(params))
            headers, body = request(url, method, headers=HEADERS)
        else:
            headers, body = request(absolute_url, method, headers=HEADERS, body=json.dumps(params))

        if headers['status'] == '200' or headers['status'] == '201':
            response_body = json.loads(body)
            return response_body
        raise ConektaError(json.loads(body))

    @classmethod
    def load_url(cls, path, method='GET', params={}):
        response = cls.build_request(method, path, params)
        return response

    @classmethod
    def class_name(cls):
        return "%s" % urllib.quote_plus(cls.__name__.lower())

    @classmethod
    def class_url(cls):
        return "%ss" % cls.class_name()

    def instance_url(self):
        return "%s/%s" % (self.class_url(), self.id)

    def construct_from(self, attributes):
        if attributes['id']:
            self.id = attributes['id']

        existing_keys = self.__dict__.keys()
        new_keys = attributes.keys()

        old_keys = set(existing_keys) - set(new_keys)
        for key in old_keys:
            self.__dict__[key] = None

        for key in new_keys:
            self.__dict__[key] = attributes[key]


    def refresh(self, url=None, method='POST', params={}):
        if url is None:
            url = self.instance_url()
            method = 'GET'

        response = self.load_url(url, method=method, params=params)

        self.construct_from(response)

        return self

class _CreateableResource(_Resource):
    @classmethod
    def create(cls, params):
        endpoint = cls.class_url()
        return cls(cls.load_url(endpoint, method='POST', params=params))

class _ListableResource(_Resource):
    @classmethod
    def retrieve(cls, _id):
        endpoint = cls.class_url()
        return cls(cls.load_url("%s/%s" % (endpoint, _id) ))

    @classmethod
    def all(cls, query={}, limit=10, offset=0, sort=[]):
        endpoint = cls.class_url()
        query['limit'] = limit
        query['offset'] = offset
        query['sort'] = sort
        return [cls(attributes) for attributes in cls.load_url(endpoint, 'GET', query)]


class Charge(_CreateableResource, _ListableResource):
    def refund(self, amount=None):
        if amount is None:
            return self.refresh("%s/refund" % self.instance_url())
        else:
            return self.refresh("%s/refund" % self.instance_url(), 'POST', {'amount':amount})

class Log(_ListableResource): pass

class Event(_ListableResource): pass



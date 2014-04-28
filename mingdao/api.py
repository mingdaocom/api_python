#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import os
import time
from urllib import urlencode
import json
import requests

data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
with open(os.path.join(data_path, 'mingdao_api.json')) as f:
	o = json.load(f)
with open(os.path.join(data_path, 'mingdao_api_errorcode.json')) as f:
	e = json.load(f)

def genAct(item, api):
	def act(args = {}):
		api_config = api.config
		token_obj = api._token_obj
		url = api_config['base_url'] + item.get('api')
		args['format'] = 'json'
		for api_arg in item.get('args'):
			if api_arg.get('name') in ['app_key', 'app_secret']:
				if api_arg.get('name') not in args.keys():
					args[api_arg.get('name')] = api_config[api_arg.get('name')]
			elif api_arg.get('name') == 'access_token':
				if api_arg.get('name') not in args.keys():
					args[api_arg.get('name')] = token_obj.get('access_token')
			if api_arg.get('required'):
				assert args.get(api_arg.get('name')), '%s is required for %s.' %\
					(api_arg.get('name'), item.get('api'))
		result = requests.request(item.get('method'), url, data=args)
		result = result.json()
		if api_config.get('throw_api_error') and result.get('error_code'):
			raise Exception(item.get('api'),
				result.get('error_code'), e.get(result.get('error_code')))
		return result
	act.__doc__ = item.get('description')
	return act

class Cat(object):
	""" API Category """
	def __init__(self, name):
		self.__name__ = name
		self._acts = {}
	def addAct(self, actName, act):
		self._acts[actName] = act
		self.__dict__[actName] = act
	def getAct(self, actName):
		return self._acts.get(actName)
	def getActs(self):
		return self._acts

class API(object):
	""" Mingdao API """
	def __init__(self, config):
		for config_arg in ['app_key', 'app_secret', 'redirect_uri']:
			assert (config_arg in config), '%s need to be configured.' % config_arg
		self.config = config
		if not self.config.get('base_url'):
			self.config['base_url'] = 'https://api.mingdao.com/'
		self._token_obj = None
		self.authorize_time = None
		self._cats = []
		apis = filter(lambda item: item.get('api') not in\
			['oauth2/authorize', 'oauth2/access_token'], o)
		for item in apis:
			api = item['api']
			catName, actName = api.split('/')
			if not self.__dict__.get(catName):
				self.__dict__[catName] = Cat(catName)
				self._cats.append(self.__dict__[catName])
			cat = self.__dict__.get(catName)
			act = genAct(item, self)
			act.info = item
			cat.addAct(actName, act)
	def getCats(self):
		return self._cats

	def _return_none_unless_authorized(fn):
		def dec(self):
			if self._token_obj and self.authorize_time:
				return fn(self)
			else:
				return None
		return dec
	@property
	@_return_none_unless_authorized
	def access_token(self):
		return self._token_obj.get('access_token')
	@property
	@_return_none_unless_authorized
	def refresh_token(self):
		return self._token_obj.get('refresh_token')
	@property
	@_return_none_unless_authorized
	def expires_in(self):
		return int(self._token_obj.get('expires_in'))
	@property
	@_return_none_unless_authorized
	def expires_at(self):
		return self.authorize_time + self.expires_in
	
	def get_authorize_url(self, **kw):
		for config_arg in ['app_key', 'redirect_uri']:
			if not kw.get(config_arg):
				kw[config_arg] = self.config[config_arg]
		return self.config['base_url'] + 'oauth2/authorize?' + urlencode(kw)
	def authorize(self, code):
		result = requests.get(self.config['base_url'] + 'oauth2/access_token', params={
            'format': 'json',
            'app_key': self.config['app_key'],
            'app_secret': self.config['app_secret'],
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.config['redirect_uri'],
        }).json()
		if result.get('error_code'):
			raise Exception('oauth2/access_token', result.get('error_code'), e.get(result.get('error_code')))
		self.authorize_time = time.time()
		self._token_obj = result
	def refresh(self):
		result = requests.get(self.config['base_url'] + 'oauth2/access_token', params={
            'format': 'json',
            'app_key': self.config['app_key'],
            'app_secret': self.config['app_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }).json()
		if result.get('error_code'):
			raise Exception('oauth2/access_token', result.get('error_code'), e.get(result.get('error_code')))
		self.authorize_time = time.time()
		self._token_obj = result

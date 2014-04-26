#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from datetime import datetime
import json
from api import API

# The following configuration is only for testing purpose, please
# replace it with your own app_key and app_secret from open.mingdao.com
# 下列参数只供测试，请勿直接使用！
# 请从 open.mingdao.com 上申请一个新的应用并获取 app_key 和 app_secret
config = {
	'app_key': 'B6FE5A96BE0582B94FBA2B77C295AB2',
	'app_secret': 'B077C043EDDCFFBF4E9E5546883E24',
	'redirect_uri': 'http://localhost:8000/callback',
	'throw_api_error': False # API 返回错误码时是否抛出异常
}

try:
	import bottle
except Exception, e:
	print '''
bottle.py is required to run the demo. Install bottle with pip:
	pip install bottle
	'''
else:
	mingdao = API(config)
	@bottle.get('/')
	def index():
		return u'''<html><head><title>首页</title></head><body>
			<a href="%s">点击登录以获取 Token</a>
		</body></html>''' % mingdao.get_authorize_url()
	@bottle.get('/callback')
	def callback():
		code = bottle.request.query.get('code')
		refresh = bottle.request.query.get('refresh')
		if code:
			mingdao.authorize(code)
		elif refresh:
			mingdao.refresh()
		else:
			return ''' 参数不正确 '''
		return u'''<html><head><title>查看 Token</title></head><body>
			<p>access_token: %s </p>
			<p>有效期: %s 秒</p>
			<p>过期时间: %s </p>
			<p><a href="/callback?refresh=true">点击刷新 Token</a></p>
			<p><a href="/test">点击查看示例接口</a></p>
		</body></html>''' % (mingdao.access_token,
			mingdao.expires_in,
			datetime.fromtimestamp(mingdao.expires_at).isoformat())
	@bottle.get('/test')
	def test():
		import sys
		return u'''<html><head><title>示例</title></head><body>
			<div>''' u'''
			<p>帐号接口</p>
			<dl>''' +\
				''.join([u'<dt>%s</dt><dd><pre>%s</pre></dd>' % ('passport/' + name, json.dumps(act(),ensure_ascii=False,indent=2))
					for name, act in filter(
						lambda actItem: actItem[0] != 'logout' and not filter(
							lambda arg: arg.get('name') not in \
								['access_token', 'app_key', 'app_secret']\
								and arg.get('required'), actItem[1].info.get('args')),
						mingdao.passport.getActs().iteritems())]) +\
			u'''</dl>''' u'''
			<p>动态更新接口</p>
			<dl>''' +\
				u'<dt>%s</dt><dd><pre>%s</pre></dd>' % ('post/followed',
					json.dumps(mingdao.post.followed({}),ensure_ascii=False,indent=2)) +\
			u'''</dl>'''\
			u'''</div>
		</body></html>'''
	bottle.run(host='localhost', port='8000', debug=True)
finally:
	pass
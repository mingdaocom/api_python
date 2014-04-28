#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from datetime import datetime
import json
from mingdao import API

if len(sys.argv) == 2 and sys.argv[1] == 'source':
	with(open(__file__)) as f:
		print(f.read())
	sys.exit(0)

print('\nThis is a demo of Mingdao app, just for your referrence.\n')

if len(sys.argv) != 3:
	print('''Usage:
	python -m mingdao source
		Print source code of this demo.

	python -m mingdao YOUR_APP_KEY YOUR_APP_SECRET
		Start the demo. Please register your app on
		http://open.mingdao.com and get the app_key
		and app_secret. 
		For this demo you should set redirect_uri as
		http://localhost:8000/auth
		''')
	sys.exit(1)

config = {
	'app_key': sys.argv[1],
	'app_secret': sys.argv[2],
	'redirect_uri': 'http://localhost:8000/callback',
}

try:
	import bottle
except Exception, e:
	print('''
bottle.py is required to run the demo. Install bottle with pip:
	pip install bottle
	''')
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
		return bottle.template(u'''<html><head><title>示例</title></head><body>
			<div><p>帐号接口</p>
			% for item in account_apis:
				<dt>{{item['path']}}</dt><dd><pre>{{item['result']}}</pre></dd>
			% end
			</div>
			<div><p>动态更新接口</p>
				<dt>followedposts['path']</dt><dd><pre>followedposts['result']</pre></dd>
			</div>
		</body></html>''', account_apis =[
			{'path': 'passport/' + name, 'result': json.dumps(act(),ensure_ascii=False,indent=2)}\
			for name, act in filter(
				lambda actItem: actItem[0] != 'logout' and not filter(
					lambda arg: arg.get('name') not in \
						['access_token', 'app_key', 'app_secret']\
						and arg.get('required'), actItem[1].info.get('args')),
				mingdao.passport.getActs().iteritems())
		], followedposts = {'path': 'post/followed',
			'result': json.dumps(mingdao.post.followed({}),ensure_ascii=False,indent=2)}
		)
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
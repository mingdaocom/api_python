api_python
==========

For Python

Install:
========
可以通过 pip 安装：

	pip install mingdao

或下载后执行

	python setup.py install

进行安装

依赖 requests 库, 如果需要直接运行 demo, 还需要 bottle 库, 可通过下面的命令安装依赖

	pip install requests
	pip install bottle

Demo:
=====
安装完成后可以通过

	python -m mingdao

运行 demo，访问地址为 http://localhost:8000

Usage:
======
请先在 http://open.mingdao.com 注册一个应用，并获取 app_key 和 app_secret

## Config

	import mingdao
	api = mingdao.API({
		'app_key': 你的 app_key(必填),
		'app_secret': 你的 app_secret(必填),
		'redirect_uri': 你设置的应用回调地址(必填),
		'throw_api_error': 在 API 返回错误码时是否抛出异常(可选),
		})

## Authorize
多数 API 需首先进行授权，获得 access_token
详情请参阅[明道开发指南](http://open.mingdao.com/Home_document_intro.html)：
用户登录后会回调应用的回调地址，并传递一个 code 参数，可用 api.authorize 方法进行授权：

	api.authorize(code)

查看授权过期时间：

	api.expires_in # 授权有效期
	api.expires_at # 过期时间

刷新授权：

	api.refresh()

## Call API
可通过 `api.分类名.接口名(参数)` 方式调用 API，access_token, app_key, app_secret 以及 format 参数无需指定。
以动态更新接口 `/post/followed` 为例：

	result = api.post.followed({
		'keywords': '关键字',
		'post_type': 1,
		'pagesize': 50,
		})

result 为反序列化 API 接口返回的 JSON 字符串后生成的字典对象。
API 接口详情请参阅[明道开发文档](http://open.mingdao.com/Home_document_intro.htm)
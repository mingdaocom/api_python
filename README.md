api_python
==========

For Python

Usage:
======
依赖 requests 库, 如果需要直接运行 demo, 还需要 bottle 库
如果已安装 pip, 可通过下面的命令安装依赖

	pip install requests
	pip install bottle

在 mingdao.py 里设置好 app_key 和 app_secret 并在明道应用管理后台设置 redirect_uri 为 http://localhost:8000/auth 后可以通过

	python mingao.py

运行 demo.
使用方式大致如下:

	import mingdao
	api = mingdao.API(app_key, app_secret, redirect_uri)
	api.get_access_token(code)
	result = api.request_api_with_token('passport/detail')

如果 API 返回错误码，程序会抛出异常

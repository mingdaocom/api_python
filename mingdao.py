#!/usr/env python
#-*- encoding: utf-8 -*-
import requests
import time

'''Mingdao API paths'''
P = {
    'base': 'https://api.mingdao.com/',
    'authorize': 'oauth2/authorize',
    'access_token': 'oauth2/access_token',
    'refresh_token': 'oauth2/access_token'
}

E = {
    u'10001': u'缺少参数',
    u'10002': u'参数所带值错误',
    u'10003': u'非法操作（如无授权删除他人的动态更新）',
    u'10004': u'无权查看群组数据',
    u'10005': u'内部错误（如数据执行失败）',
    u'10006': u'无权查看任务数据',
    u'10007': u'请求数据不存在（如已被删除)',
    u'10008': u'无权查看日程数据',
    u'10009': u'无权对任务进行操作(权限仅给任务负责人或任务创建者)',
    u'10010': u'无权对日程进行操作(权限仅给日程创建者)',
    u'10011': u'无权对群组进行操作(权限仅给群组管理员或网络管理员)',
    u'10012': u'无权对动态进行操作(权限仅给动态创建者或网络管理员)',
    u'10013': u'无权查看动态相关内容',
    u'10014': u'无权查看群组相关内容',
    u'10015': u'无权对群组进行操作(权限仅给群组管理员)',
    u'10016': u'无权对任务项目进行操作(权限仅给项目创建者)',
    u'10017': u'任务项目名称已存在',
    u'10018': u'权限仅给网络管理员',
    u'10019': u'权限仅供系统广播员',
    u'10020': u'无权对群组进行操作(权限仅给网络管理员)',
    u'10021': u'群组名称已存在',
    u'10101': u'请求令牌不存在',
    u'10102': u'请求令牌签名不合法',
    u'10103': u'用户账号不存在',
    u'10104': u'用户签名不合法(登录验证失败,密码错误）',
    u'10105': u'用户访问令牌失效',
    u'10106': u'用户状态不对 如用户未审核、拒绝申请、被屏蔽登录、已删除、被举报离职',
    u'10107': u'由于您的帐号尝试多次登录失败，已被锁定，请20分钟后再试',
    u'10108': u'code已经失效',
    u'10201': u'Email不合法',
    u'10202': u'Email已经注册',
    u'10203': u'非本网络Email',
    u'10204': u'非法邀请',
    u'10205': u'有效域名邮箱，不能通过来宾邀请加入',
    u'10206': u'无权限邀请来宾',
    u'10301': u'暂无应用的最新版本',
    u'10302': u'仅限企业应用调用',
    u'10303': u'仅限高级模式的管理员调用',
    u'10304': u'仅限高级模式可调用',
    u'10305': u'仅限应用创建者可调用',
    u'10401': u'扩展应用未安装',
    u'10402': u'扩展应用没权限直接通过用户账号获取令牌',
    u'10501': u'免费网络没有权限发送',
    u'10502': u'当前用户没有权限发送',
    u'10503': u'当前用户本月手机短信数超出',
    u'10504': u'当前网络余额不足',
    u'10505': u'发送手机信息内容超出500字',
    u'10506': u'信息接受者没有手机号',
    u'10507': u'发送手机短信失败',
    u'1': u'操作成功',
    u'2': u'操作失败（当捕获不到预期异常均返回此值）',
    u'2001': u'提交数据时参数缺失',
    u'2002': u'提交数据时参数值不对',
    u'2003': u'签名错误',
    u'2004': u'重复操作',
    u'2005': u'账户余额不足',
    u'2006': u'已经支付',
    u'2007': u'账单金额不正确',
    u'2008': u'出账应用不符合要求 ',
}

class API(object):
    def __init__(self, app_key, app_secret, redirect_uri, token_obj=None, get_token_time=None):
        self.app_key = app_key
        self.app_secret = app_secret
        self._redirect_uri = redirect_uri
        self.access_token = token_obj and token_obj.get('access_token') or None
        self.expires_in = token_obj and float(token_obj.get('expires_in')) or None
        self.refresh_token = token_obj and token_obj.get('refresh_token') or None
        self.get_token_time = get_token_time
        self.expires_at = get_token_time and token_obj and self.expires_in\
                and get_token_time + self.expires_in - time.time()
    def _api(self, api_path):
        return P['base'] + api_path
    @property
    def authorize_url(self):
        return self._api(P['authorize']) + '?'\
            'app_key=' + self.app_key + '&'\
            'redirect_uri=' + self._redirect_uri
    def get_token(self, code):
        res = requests.get(self._api(P['access_token']), params={
            'format': 'json',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self._redirect_uri,
        }).json()
        if res.get('error_code'):
            raise Exception(res, E.get(res.get('error_code')))
        self.access_token = res.get('access_token')
        self.refresh_token = res.get('refresh_token')
        self.expires_in = float(res.get('expires_in'))
        self.expires_at = time.time() + self.expires_in
        return self.access_token
    @property
    def expires_after(self):
        return self.expires_at - time.time()
    def refresh_access_token(self):
        res = requests.get(self._api(P['refresh_token']), params={
            'format': 'json',
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }).json()
        if res.get('error_code'):
            raise Exception(res, E.get(res.get('error_code')))
        self.access_token = res.get('access_token')
        self.refresh_token = res.get('refresh_token')
        self.expires_in = float(res.get('expires_in'))
        self.expires_at = time.time() + self.expires_in
        return self.access_token
    def request_api(self, api_path, method='GET', params={}):
        params['format'] = 'json'
        res = requests.request(method, self._api(api_path), data=params).json()
        if res.get('error_code'):
            raise Exception(res, E.get(res.get('error_code')))
        return res
    def request_api_with_token(self, api_path, method='GET', params={}):
        params['format'] = 'json'
        params['access_token'] = self.access_token
        res = requests.request(method, self._api(api_path), data=params).json()
        if res.get('error_code'):
            raise Exception(res, E.get(res.get('error_code')))
        return res
    def request_api_with_keysec(self, api_path, method='GET', params={}):
        params['format'] = 'json'
        params['app_key'] = self.app_key
        params['app_secret'] = self.app_secret
        print params
        res = requests.request(method, self._api(api_path), data=params).json()
        print res
        if res.get('error_code'):
            raise Exception(res, E.get(res.get('error_code')))
        return res

def start_server():
    import datetime
    import bottle
    app_key = 'YOUR_APP_KEY' # app_key
    app_secret = 'YOUR_APP_SECRET' # app_secret
    redirect_uri = 'http://localhost:8000/auth' # 在明道设置的回调地址
    api = API(app_key, app_secret, redirect_uri)
    @bottle.get('/')
    def index():
        return '<a href="%s">点击获取 Token</a>' % api.authorize_url
    @bottle.get('/auth')  # 在明道设置的回调地址
    def auth():
        code = bottle.request.query.get('code')
        if code:
            return u'token: %s' % api.get_token(code) + '\n'\
                u'过期时间: %s' % \
                    datetime.datetime.fromtimestamp(api.expires_at).isoformat() + '\n'\
                u'<a href="/refresh">点击刷新 Token</a>' +'\n'\
                u'<a href="/test">示例</a>'
        else:
            return 'Didn\'t receive a code'
    @bottle.get('/refresh')
    def refresh():
        return u'token: %s' % api.refresh_access_token() + '\n' +\
            u'过期时间: %s' %\
                datetime.datetime.fromtimestamp(api.expires_at).isoformat() + '\n'\
            u'<a href="/refresh">点击刷新 Token</a>' + '\n'\
            u'<a href="/test">示例</a>'
    @bottle.get('/test')
    def test():
        return '''
        获取账户信息: 
        %s
    ''' % api.request_api_with_token('passport/detail')
    bottle.run(host='localhost', port='8000', debug=True)

if __name__ == '__main__':
    start_server()

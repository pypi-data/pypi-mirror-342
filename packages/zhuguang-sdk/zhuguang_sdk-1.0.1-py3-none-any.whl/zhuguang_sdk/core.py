import time
import webbrowser

import pydash
import requests

from zhuguang_sdk import utils


class ZhuguangSDK:

    def __init__(self):
        self.server_url = None
        self.product_id = None
        self.config = utils.Config()
        self._user_token = self.config.get('user_token', None)
        self._qrcode_login = {}

    def init(self, server_url):
        self.server_url = server_url

    def login(self, username, password, login_ways="username"):
        """账号密码登录"""
        request_url = self.server_url + "/wp-json/zhuguang_theme/v1/user/login"
        data = {
            "username": username,
            "password": password,
            "login_ways": login_ways
        }

        try:
            res = requests.post(request_url, json=data)
        except:
            raise Exception('访问服务器失败，请稍后重试')

        res_data = None
        try:
            res_data = res.json()
        except:
            pass

        if res.status_code != 200 and res_data:
            raise Exception(res_data.get('message'))

        self._user_token = res_data.get('token')
        if self._user_token:
            self.config.update('user_token', self._user_token)
            return True
        else:
            return False

    def login_qrcode(self):
        """公众号扫码登录"""
        request_url = self.server_url + "/wp-json/zhuguang_theme/v1/wechat/get_login_qrcode"

        try:
            res = requests.get(request_url)
        except:
            raise Exception('访问服务器失败，请稍后重试')

        res_data = None
        try:
            res_data = res.json()
        except:
            pass

        if res.status_code != 200 and res_data:
            raise Exception(res_data.get('message'))

        self._qrcode_login = res_data
        ticket = res_data.get('ticket', False)

        if not ticket:
            return False

        tread, stop_tread = utils.generate_qr_and_show(res_data.get('url', ''))


        while tread.isAlive():
            # print("等待扫码中...")
            if self._check_qrcode_login(ticket, stop_tread):
                break

            time.sleep(1)

        # input("按Enter键退出主线程（子线程为守护线程会自动终止）\n")

        tread.join()
        if self._user_token:
            return True
        else:
            return False


    def _check_qrcode_login(self, ticket, stop_tread):
        request_url = self.server_url + "/wp-json/zhuguang_theme/v1/wechat/query_login_qrcode"
        data = {
            "ticket": ticket,
        }

        try:
            res = requests.get(request_url, params=data)
        except:
            raise Exception('访问服务器失败，请稍后重试')

        res_data = None
        try:
            res_data = res.json()
        except:
            pass

        if res.status_code != 200 and res_data:
            stop_tread()
            return False

        self._user_token = res_data.get('token')
        if self._user_token:
            self.config.update('user_token', self._user_token)
            stop_tread()
            return True
        else:
            return False

    def get_user_info(self):
        """获取当前登录用户账号信息，返回字典，需要登录后使用"""
        if not self._user_token:
            raise Exception('请先登录')

        request_url = self.server_url + "/wp-json/zhuguang_theme/v1/user/info"
        headers = {
            "Authorization": "Bearer" + self._user_token
        }
        try:
            res = requests.get(request_url, headers=headers)
        except:
            raise Exception('访问服务器失败，请稍后重试')

        res_data = None
        try:
            res_data = res.json()
        except:
            pass
        if res.status_code == 403:
            raise Exception('请先登录，身份验证已失效')

        if res.status_code != 200 and res_data:
            raise Exception(res_data.get('message'))

        return res_data.get('data', {})

    def get_post_content(self, post_id):
        """获取特定帖子内容，需要登录后使用"""
        if not self._user_token:
            raise Exception('请先登录')

        request_url = self.server_url + f"/wp-json/wp/v2/posts/{post_id}"
        headers = {
            "Authorization": "Bearer" + self._user_token
        }
        try:
            res = requests.get(request_url, headers=headers)
        except:
            raise Exception('访问服务器失败，请稍后重试')

        res_data = None
        try:
            res_data = res.json()
        except:
            pass
        if res.status_code == 403:
            raise Exception('请先登录，身份验证已失效')

        if res.status_code != 200 and res_data:
            raise Exception(res_data.get('message'))
        # print(res_data)
        return pydash.get(res_data, 'content.rendered', {})

    def get_posts_list(self, page=1, per_page=10, content_type="posts", **other_params):
        """获取帖子列表，需要登录后使用，返回[{id,标题}]"""
        if not self._user_token:
            raise Exception('请先登录')

        params = {
            "page": page,
            "per_page": per_page,
            **other_params
        }
        request_url = self.server_url + f"/wp-json/wp/v2/{content_type}"
        headers = {
            "Authorization": "Bearer" + self._user_token
        }
        try:
            res = requests.get(request_url, params=params, headers=headers)
        except:
            raise Exception('访问服务器失败，请稍后重试')

        res_data = None
        try:
            res_data = res.json()
        except:
            pass
        if res.status_code == 403:
            raise Exception('请先登录，身份验证已失效')

        if res.status_code != 200 and res_data:
            raise Exception(res_data.get('message'))
        # print(res_data)
        # map(res_data, )
        return res_data

    def set_product_id(self, product_id):
        """打开当前产品页面ID"""
        self.product_id = product_id

    def open_post_page(self, post_id):
        """打开特定id的帖子"""
        webbrowser.open(self.server_url + f"/{post_id}.html")

    def open_product_page(self):
        """打开当前产品页面"""
        webbrowser.open(self.server_url + f"/{self.product_id}.html")

    def open_vip_page(self):
        """打开VIP开通页面"""
        webbrowser.open(self.server_url + f"/vip")




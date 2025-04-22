"""
@author: noybzy
@time: 2024/4/14 下午15:02
@file: database.py
@describe: http操作
"""
import abc
import time
from typing import Optional

import requests
from loguru import logger


class RetryRequest(Exception):
    def __init__(self, flush=True):
        self.flush = flush


class BaseRequest(abc.ABC):

    def __init__(self, proxy_url: str):
        self.proxy_url = proxy_url
        self.proxy = None
        self.headers = None
        self.cookies = None
        self.timeout = 6
        self.verify = False
        self.req = None
        self.max_retry = 25
        self.flush_proxy()

    def get_proxy(self) -> Optional[dict]:
        if self.proxy_url:
            num = 0
            while True:
                num += 1
                try:
                    proxy = requests.get(self.proxy_url, timeout=6).json()
                    break
                except Exception as e:
                    logger.warning(f'获取代理出错_{num}:{e.__class__}')
                    time.sleep(5)
            return proxy
        return None

    def flush_proxy(self):
        logger.debug(f'刷新代理: flush')
        self.proxy = self.get_proxy()

    @abc.abstractmethod
    def get(self, url: str, params=None, headers=None, cookies=None, allow_redirects=True, show_debug=True,
            timeout=None, auth=None, stream=None, cert=None, verify=None
            ):
        pass

    @abc.abstractmethod
    def post(self, url, params=None, data=None, json=None, allow_redirects=True, headers=None,
             cookies=None, show_debug=False,
             timeout=None, auth=None, stream=None, cert=None, verify=None
             ):
        pass

    def request_interceptor(self, url: str, params: str, data, json_data: Optional[dict], method: str):
        """请求拦截器"""
        pass

    def response_interceptor(self, response):
        """响应拦截器"""
        pass

    def exception_interceptor(self, exc):
        pass

    def put(self, *args):
        pass

    def delete(self, *args):
        pass


class Request(BaseRequest):

    def __init__(self, proxy_url: str,headers=None, cookies=None, timeout=6):
        super().__init__(proxy_url=proxy_url)
        self.req = requests
        self.headers = headers
        self.cookies = cookies
        self.timeout = timeout

    def exception_interceptor(self, e):
        try:
            raise e
        except requests.exceptions.ProxyError as e:
            logger.debug(f"代理错误: {e.__class__.__name__}")
            raise RetryRequest()
        except requests.exceptions.Timeout as e:
            logger.debug(f"超时: {e.__class__.__name__}")
            raise RetryRequest()
        except Exception as e:
            raise e

    def get(self, url: str, params=None, headers=None, cookies=None, allow_redirects=True, show_debug=True,
            timeout=None, auth=None, stream=None, cert=None, verify=None) -> Optional[requests.Response]:
        """
        发送get请求
        :param cookies:
        :param headers:
        :param allow_redirects:
        :param url:
        :param params:
        :param show_debug:
        :return:
        """
        num = 0
        # 请求拦截器
        while True:
            num = num + 1
            self.request_interceptor(url, params, None, None, 'get')

            final_cookies = cookies if cookies is not None else self.cookies
            final_headers = headers if headers is not None else self.headers
            final_timeout = timeout if timeout is not None else self.timeout
            final_verify = verify if verify is not None else self.verify

            if show_debug:
                logger.debug(f"发送请求GET_{num}：{url}")
            try:
                response = self.req.get(
                    url=url, proxies=self.proxy, cookies=final_cookies, headers=final_headers,
                    timeout=final_timeout, verify=final_verify, params=params, auth=auth,
                    stream=stream, cert=cert,
                    allow_redirects=allow_redirects
                )
                self.response_interceptor(response)
                return response
            except RetryRequest as e:
                if num > self.max_retry:
                    raise e
                if e.flush:
                    self.flush_proxy()
            except Exception as e:
                if num > self.max_retry:
                    raise e
                try:
                    self.exception_interceptor(e)
                except RetryRequest as e:
                    if e.flush:
                        self.flush_proxy()
                    continue
                except Exception as e:
                    raise e

    def post(self, url, params=None, data=None, json=None, allow_redirects=True, headers=None, cookies=None,
             show_debug=False, timeout=None, auth=None, stream=None, cert=None, verify=None) -> Optional[
        requests.Response]:
        """
        发送post请求
        :param allow_redirects:
        :param url:
        :param params:
        :param data:
        :param json_data:
        :return:
        """
        num = 0
        while True:
            num = num + 1
            self.request_interceptor(url, params, None, None, 'get')

            final_cookies = cookies if cookies is not None else self.cookies
            final_headers = headers if headers is not None else self.headers
            final_timeout = timeout if timeout is not None else self.timeout
            final_verify = verify if verify is not None else self.verify

            if show_debug:
                logger.debug(f"发送请求POST_{num}：{url}")
                if json:
                    logger.debug(f'json_data:{json}')
                if data:
                    logger.debug(f'data:{data}')

            try:
                response = self.req.post(url=url, proxies=self.proxy, cookies=final_cookies, headers=final_headers,
                                         timeout=final_timeout, verify=final_verify, params=params, data=data,
                                         json=json, allow_redirects=allow_redirects, stream=stream, cert=cert,
                                         auth=auth)
                self.response_interceptor(response)
                return response
            except RetryRequest as e:
                if num > self.max_retry:
                    raise e
                if e.flush:
                    self.flush_proxy()
            except Exception as e:
                if num > self.max_retry:
                    raise e
                try:
                    self.exception_interceptor(e)
                except RetryRequest as e:
                    if e.flush:
                        self.flush_proxy()
                    continue
                except Exception as e:
                    raise e

# -*- coding: utf-8 -*-
# @Time   : 2024/4/28 16:40
import random
from functools import partial
from typing import Optional, Union
import requests as requests_requests

from requests.exceptions import ProxyError
from urllib3.exceptions import ReadTimeoutError

try:
    # 需要 py3.7+
    from curl_cffi import requests as curl_cffi_requests
    from urllib3 import HTTPHeaderDict

except ImportError:
    curl_cffi_requests = None
from urllib.parse import urlparse

# from faker import Faker
# from loguru import logger
from requests import RequestException

# from python_sec.core import ExceptionHandler
# from python_sec.tutil.crawler_exception import DOWNLOAD_CODE
# from python_sec.tutil.sec_proxy import VpsProxy
# from python_sec.tutil.trace_tool import track_monitor



class Request():
    def __init__(self, timeout: int = 10, try_times: int = 3, use_proxy: bool = True, proxy_conf: Optional[dict] = None):
        self.timeout = timeout
        self.try_times = try_times
        self.get = partial(self.request, "GET")
        self.post = partial(self.request, "POST")
        self.head = partial(self.request, "HEAD")
        self.put = partial(self.request, "PUT")
        self.options = partial(self.request, "OPTIONS")
        self.delete = partial(self.request, "DELETE")
        self.patch = partial(self.request, "PATCH")

    # @track_monitor("req")
    def request(
            self,
            method: str,
            url: str,
            data: Optional[dict] = None,
            params: Optional[dict] = None,
            headers: Optional[dict] = None,
            cookies: Optional[dict] = None,
            json: Optional[dict] = None,
            verify: Optional[bool] = False,
            stream: Optional[bool] = None,
            timeout: Optional[int] = None,  # 超时时间，默认为全局配置
            proxies: Optional[dict] = None,
            allow_redirects: bool = True,
            use_proxy: Union[int, bool] = True,
            try_times: Optional[int] = None,  # 尝试请求次数，默认为全局配置
            delay: Optional[int] = None,  # 请求间隔
            impersonate: Optional[str] = None,  # 伪装请求,如果设置了,则使用curl_cffi_requests
            cipher: Optional[str] = None,  # 设置加密算法, 如果设置了，则更改原生requests的加密算法
            req_uid: Optional[str] = None,
            proxy_conf: Optional[dict] = None,
            **kwargs,
    ):
        if not kwargs:
            kwargs = dict()
        if impersonate:
            # https://github.com/lwthiker/curl-impersonate/tree/main
            kwargs["impersonate"] = impersonate
            if not curl_cffi_requests:
                raise Exception("请安装 curl_cffi")
            _requests = curl_cffi_requests
        else:
            kwargs["stream"] = stream
            _requests = requests_requests
            if cipher:
                cipher = cipher.split(",")
                random.shuffle(cipher)
                cipher = ",".join(cipher)
                _requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = cipher
        times = 1
        url_parse = urlparse(url)
        hostname = url_parse.hostname
        url_path = url_parse.path
        # http_proxies, _req_uid = self.prepare_proxies(url, use_proxy, proxies, req_uid, proxy_conf)
        # headers = self.prepare_headers(headers, impersonate)
        # if http_proxies:
        #     print(f"{hostname}{url_path} 代理启用 req_uid: {_req_uid} {http_proxies['network']}")
        # else:
        #     print(f"{hostname}{url_path} 代理未启用")

        _retry_times = try_times or self.try_times
        _timeout = timeout or self.timeout
        while times <= _retry_times:
            try:
                response = _requests.request(
                    url=url,
                    # proxies=http_proxies,
                    method=method.upper(),
                    data=data,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    json=json,
                    timeout=_timeout,
                    allow_redirects=allow_redirects,
                    verify=verify,
                    **kwargs,
                )
            except (Exception, RequestException, OSError, ProxyError, ReadTimeoutError) as e:
                times += 1
                # if delay:
                #     time.sleep(delay or self.delay)
                if times > _retry_times:
                    msg = f"url {url} req_id: {req_uid} 请求失败, error: {e} try_times {times - 1}"
                    # raise ExceptionHandler.handler_exception(ex=e, error_message=msg, error_code=DOWNLOAD_CODE)
                print(f"url {url} req_id: {req_uid} 请求失败, error: {e} try_times {times - 1}")
                continue

            return response

    def prepare_proxies(self, url, use_proxy, proxies, req_uid=None, proxy_conf=None):
        if not use_proxy or not self.use_proxy:
            return None, ""
        # 优先使用传入的代理
        if proxies:
            return proxies, ""
        if proxy_conf:
            final_proxy_conf = proxy_conf.copy()
        else:
            final_proxy_conf = self.proxy_conf.copy()
        if not final_proxy_conf:
            raise Exception(f"url: {url} 请先配置代理信息， req_uid: {req_uid}")
        if proxy_conf and isinstance(proxy_conf, dict):
            final_proxy_conf.update(proxy_conf)
        if req_uid:
            final_proxy_conf["req_uid"] = req_uid
        if not final_proxy_conf.get("req_uid"):
            url_parse = urlparse(url)
            hostname = url_parse.hostname
            url_path = url_parse.path
            final_proxy_conf["req_uid"] = f"{hostname}_{url_path}_{int(time.time() * 1000)}"

        # proxies = VpsProxy.get_http_proxies(final_proxy_conf)
        return proxies, final_proxy_conf.get("req_uid", "")

    @staticmethod
    def prepare_headers(headers, impersonate) -> dict:
        if not headers:
            return {}
            # return (
            #     {"User-Agent": fake.chrome()} if not impersonate else {}
            # )  # 如果是使用tls伪装,则不需要设置ua,会自动设置
        if headers and not isinstance(headers, dict):
            raise Exception(f"headers: {headers} 必须是字典")
        # 转为 HTTPHeaderDict, 用于处理大小写问题
        headers = HTTPHeaderDict(headers)
        if impersonate:
            # 如果是使用tls伪装,则需要删除一些头部信息，默认 curl_cffi_requests 会自动添加，如果不删除会覆盖 curl_cffi_requests 的设置
            headers.pop(
                "sec-ch-ua", None
            )  # ua信息，如'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
            headers.pop("sec-ch-ua-platform", None)  # 平台信息，如 "macOS"、"Windows"、"Linux"
            headers.pop("User-Agent", None)  # ua
        # elif not headers.get("User-Agent"):
        #     headers["User-Agent"] = fake.chrome()
        # headers.pop("x-forwarded-for", None)  # ua
        final_headers = dict(headers)
        return final_headers

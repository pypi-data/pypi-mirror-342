# -*- coding: UTF-8 -*-

import re
import random
import primp
from .utils import parse_client_hints
from .base import BaseCracker


class DatadomeCracker(BaseCracker):
    cracker_name = "datadome"
    cracker_version = "universal"

    """
    datadome
    :param href: 触发验证的页面地址
    调用示例:
    cracker = KasadaCtCracker(
        user_token="xxx",
        href="https://rendezvousparis.hermes.com/client/register",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        proxy="user:pass@ip:port",
        debug=True,
    )
    ret = cracker.crack()
    """

    # 必传参数
    must_check_params = ["href", "proxy"]
    # 默认可选参数
    option_params = {
        "branch": "Master",
        "captcha": None,
        "captcha_url": None,
        "captcha_html": None,
        "js_url": None,
        "js_key": None,
        "did": None,
        "user_agent": None,
        "interstitial": False,
        "accept_language": "en-US,en;q=0.9",
        "country": None,
        "ip": None,
        "timezone": None,
        "geolocation": None,
        "html": False,
        "timeout": 30
    }

    def request(self):
        country = self.wanda_args.get("country")
        _ip = self.wanda_args.get("ip")
        timezone = self.wanda_args.get("timezone")
        geolocation = self.wanda_args.get("geolocation")
        
        if not self.interstitial and not self.js_key and not self.captcha and not self.captcha_url and not self.captcha_html:
            if not self.user_agent:
                version = random.randint(115, 134)
                if random.random() > .4:
                    if random.random() > .5:
                        self.user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36"
                    else:
                        self.user_agent = f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36'
                else:
                    if random.random() > .5:
                        self.user_agent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0'
                    else:
                        self.user_agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36 Edg/{version}.0.0.0"
            else:
                version = int(re.search(r'Chrome\/(\d+)\.\d+\.\d+\.\d+', self.user_agent)[1])
                
            if 'Edg' in self.user_agent:
                impersonate_brand = "edge"
                impersonate_versions = [122, 127, 131]
            else:
                impersonate_brand = "chrome"
                impersonate_versions = [114, 116, 117, 118, 119, 120, 123, 124, 126, 127, 128, 129, 130, 131]
            
            min_version = None
            impersonate_version = None
            for v in impersonate_versions:
                cv = abs(v - version)
                if not min_version or cv < min_version:
                    min_version = cv
                    impersonate_version = v
                    
            impersonate = f'{impersonate_brand}_{impersonate_version}'
            
            proxy = None
            if self.proxy:
                proxy = "http://" + self.proxy
            self.session = primp.Client(impersonate=impersonate, impersonate_os="macos" if 'Mac' in self.user_agent else "windows", proxy=proxy)
                
            if self.cookies:
                self.session.cookies.update(self.cookies)

            # 跟 ua 版本对应
            sec_ch_ua = parse_client_hints(self.user_agent)
            sec_ch_ua_ptf = '"macOS"' if 'Mac' in self.user_agent else '"Windows"'

            headers = {
                'sec-ch-ua': sec_ch_ua,
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': sec_ch_ua_ptf,
                'upgrade-insecure-requests': '1',
                'user-agent': self.user_agent,                
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-fetch-site': "none",
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': "document",
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': self.accept_language,
                "priority": "1"
            }
            
            response = self.session.get(self.href, headers=headers)
            if response.status_code == 403:
                dd_match = re.search(r'var dd=(\{.*?\})', response.text)
                if dd_match:
                    self.wanda_args = {
                        "href": self.href,
                        "captcha_html": response.text,
                        "user_agent": self.user_agent,
                        "cookies": {
                            "datadome": response.cookies.get("datadome") or "",
                        },
                        "proxy": self.proxy,
                        
                        "did": self.did,
                        "html": self.html,
                        
                        "branch": self.branch,
                        "is_auth": self.wanda_args["is_auth"],
                    }
                else:
                    raise Warning("代理异常或触发未知验证")
            else:
                if not self.js_key:
                    dd_js_key = re.search(r"ddjskey = .(.{30}).", response.text)
                    if dd_js_key:
                        self.js_key = dd_js_key[1]
                
                if self.js_url and self.js_key:
                    self.wanda_args = {
                        "href": self.href,
                        "js_url": self.js_url,
                        "js_key": self.js_key,
                        "user_agent": self.user_agent,
                        "cookies": {
                            "datadome": self.session.cookies.get("datadome") or "",
                        },
                        "proxy": self.proxy,
                        
                        "did": self.did,
                        "html": self.html,
                        
                        "branch": self.branch,
                        "is_auth": self.wanda_args["is_auth"],
                    }
                else:
                    self.wanda_args = {
                        "href": self.href,
                        "interstitial": True,
                        "user_agent": self.user_agent,
                        "proxy": self.proxy,
                        
                        "did": self.did,
                        "html": self.html,
                        
                        "branch": self.branch,
                        "is_auth": self.wanda_args["is_auth"],
                    }

        if country:
            self.wanda_args["country"] = country
            
        if _ip:
            self.wanda_args["ip"] = _ip
        
        if timezone:
            self.wanda_args["timezone"] = timezone
        
        if geolocation:
            self.wanda_args["geolocation"] = geolocation
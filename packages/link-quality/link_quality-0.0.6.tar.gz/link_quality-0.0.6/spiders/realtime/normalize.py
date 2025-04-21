import json
import sys
import re
from enum import Enum

from collections import OrderedDict
from html import unescape
from typing import Union
from urllib.parse import urlparse, parse_qsl, urlunparse, ParseResult, quote_plus, unquote, unquote_plus

from aiocache import cached, SimpleMemoryCache
from redis import asyncio
from tldextract import tldextract

from spiders.realtime.link_filter import LinkFilter, Result
from spiders.realtime.rt_logger import logger


def urlencode(query, safe='', encoding=None, errors=None,
              quote_via=quote_plus):
    """
    重写urlencode函数 修复空参数末尾加=问题
    :param query:
    :param safe:
    :param encoding:
    :param errors:
    :param quote_via:
    :return:
    """
    if hasattr(query, "items"):
        query = query.items()
    else:
        try:
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
        except TypeError:
            ty, va, tb = sys.exc_info()
            raise TypeError("not a valid non-string sequence "
                            "or mapping object").with_traceback(tb)

    l = []
    for k, v in query:
        if isinstance(k, bytes):
            k = quote_via(k, safe)
        else:
            k = quote_via(str(k), safe, encoding, errors)

        if isinstance(v, bytes):
            v = quote_via(v, safe)
        else:
            v = quote_via(str(v), safe, encoding, errors)
        if not v:
            l.append(k)
        else:
            l.append(k + '=' + v)
    return '&'.join(l)


chinese_characters_re = re.compile(r'[\u4e00-\u9fff]+')


def params_unquote(encoded_str):
    """
    参数解码，去除 编码产物 amp;
    :param encoded_str:
    :return:
    """
    decoded_str = unquote(encoded_str)
    decoded_url = decoded_str
    while True:
        decoded_url_res = unescape(decoded_url)
        if decoded_url == decoded_url_res:
            break
        else:
            decoded_url = decoded_url_res

    # decoded_str = decoded_str.replace("amp;", "")
    return decoded_url


def keep_chinese(source_url, decoded_url):
    """
    维持原始Url的中文编码状态
    :param decoded_url:
    :return:
    """
    contains_chinese = chinese_characters_re.search(source_url) is not None
    if contains_chinese:
        # url 解码 ，维持中文
        decoded_url = unquote_plus(decoded_url)
    return decoded_url


def validate_url(url):
    """
    url 合法性验证
    :param url:
    :return:
    """
    if not url:
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class ReturnType(Enum):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    ## 规则匹配成功
    normal = (0, "normal")

    no_rules = (0, "no corresponding rules")  # 没有域名对应规则

    ## 异常
    url_parse_error = (1, "url parse error")  # URL 解析异常
    rule_not_match = (2, "rule not match")  # 规则引擎匹配失败
    normalize_error = (3, "normalize error")  # 归一化处理异常
    url_is_invalid = (4, "url is invalid")  # URL 非法


class NormalizeResult(Result):
    def __init__(self, hit: bool, msg: str, code: int, rule: Union[str, dict], extra: dict, url, normalize_url):
        super().__init__(hit=hit, msg=msg, code=code, rule=rule, extra=extra)
        self.url = url
        self.normalize_url = normalize_url


class Normalizer:
    def __init__(self, rds_host=None, rds_port=None, rds_password=None):
        self.client = asyncio.Redis(
            host=rds_host,
            port=rds_port,
            password=rds_password,
            db=4,
            max_connections=300,
        )
        self.link_filter = LinkFilter()
        self.normalize_table_key = "normalize:rules"

    async def manual_evaluate(self, url, rules=None, data=None):
        """
        归一化手动传入规则。如果有链接匹配规则先判断是否匹配，匹配后再判断再做归一化。如果 mirror 和 scheme 存在则替换为相应的值。
        @param url: 链接
        @param rules: 链接匹配规则
        @param data 归一化规则
        """

        keys = data.get("keys")
        mirror = data.get("mirror")
        new_scheme = data.get("scheme")
        try:

            scheme, netloc, path, params, query, domain = self.parse_url(url)
            query = params_unquote(query)
        except Exception as exc:
            # URL 解析异常
            logger.exception(f"url parse error", exc)
            return Result(hit=True, msg=ReturnType.url_parse_error.msg, code=ReturnType.url_parse_error.code,
                          rule=rules,
                          extra={"ori_url": url, "new_url": url, "data": data}
                          ).to_dict()
        else:
            # 判断是否命中前置规则（规则引擎）
            link_filter_result: Result = await self.link_filter.manual_evaluate(url, rules, serialize=False)

            rest_parts = []
            if link_filter_result.hit:
                parts = parse_qsl(query)
                for part, value in parts:
                    if part in keys:
                        if not int(keys[part]) == 1:
                            rest_parts.append((part, value))
                    else:
                        rest_parts.append((part, value))
            else:
                return Result(hit=False, msg=ReturnType.rule_not_match.msg, code=ReturnType.rule_not_match.code,
                              rule=rules,
                              extra={"ori_url": url, "new_url": url, "data": data}
                              ).to_dict()
            if mirror:
                netloc = mirror
            if new_scheme:
                scheme = new_scheme
            parse_result = ParseResult(scheme=scheme, netloc=netloc, path=path, params=params,
                                       query=urlencode(rest_parts), fragment=None)
            new_url = urlunparse(parse_result)
            return Result(hit=url != new_url, msg=ReturnType.normal.msg, code=ReturnType.normal.code, rule=rules,
                          extra={"ori_url": url, "new_url": new_url, "data": data}).to_dict()

    async def evaluate(self, url):
        """
        归一化接口。
        @param url: 链接
        """
        new_url, rule, extra, return_type = await self.check(url)
        return NormalizeResult(hit=url != new_url, msg=return_type.msg, code=return_type.code, rule=rule,
                               extra=extra, url=url, normalize_url=new_url).to_dict()

    @staticmethod
    def assemble_url(scheme: str, netloc: str, path: str, params: Union[str, None], query: dict[str, str]):
        return urlunparse(
            ParseResult(scheme=scheme, netloc=netloc, path=path, params=params, query=urlencode(query), fragment=None)
        )

    @cached(ttl=86400, cache=SimpleMemoryCache)
    async def get(self, domain):
        return await self.client.hget(self.normalize_table_key, domain)

    @staticmethod
    def parse_url(url):
        url_obj = urlparse(url)

        scheme = url_obj.scheme
        netloc = url_obj.netloc
        path = url_obj.path
        params = url_obj.params
        query = url_obj.query

        domain = tldextract.extract(url).registered_domain
        return scheme, netloc, path, params, query, domain

    @classmethod
    def normalize_offline(cls, scheme, netloc, path, params, query_dict):
        verified_url = cls.assemble_url(scheme=scheme, netloc=netloc, path=path, params=params, query=query_dict)
        logger.info(f"verified_url: {verified_url}")

    async def check(self, url: str):
        try:
            scheme, netloc, path, params, query, domain = self.parse_url(url)
        except Exception as exc:
            # URL 解析异常
            logger.exception(f"url parse error", exc)
            return url, dict(), dict(), ReturnType.url_parse_error

        if not all([scheme, netloc]):
            return url, dict(), dict(), ReturnType.url_is_invalid

        try:
            query = params_unquote(query)

            query_params = parse_qsl(query, keep_blank_values=True)

            rules = await self.get(domain)
            query_dict = dict()
            exclude_set = set()

            if not rules:
                # 新站点，直接走离线验证
                for k, v in query_params:
                    query_dict[k] = v
                    self.normalize_offline(scheme=scheme, netloc=netloc, path=path, params=params,
                                           query_dict=query_dict)
                return url, dict(), dict(), ReturnType.no_rules
            else:
                rules = json.loads(rules)

                for rule in rules:
                    data = rule.get("data")
                    extra = rule.pop("extra")

                    keys = data.get("keys")
                    mirror = data.get("mirror")
                    new_scheme = data.get("scheme")
                    link_filter_result = await self.link_filter.manual_evaluate(url, {domain: [rule]}, serialize=False)
                    if link_filter_result.hit:
                        for k, v in query_params:
                            check_code = keys.get(k)
                            if not check_code:
                                # 没有验证过的参数，当做必要参数 todo 离线验证，使用弹外能够使用的 rds 或者其他
                                query_dict[k] = v
                                self.normalize_offline(scheme=scheme, netloc=netloc, path=path, params=params,
                                                       query_dict=query_dict)
                            elif check_code == 3:
                                query_dict[k] = v
                            else:
                                exclude_set.add(k)

                        if mirror:
                            netloc = mirror
                        # if new_scheme:
                        #     scheme = new_scheme

                        # 重组url
                        new_url = self.assemble_url(scheme=scheme, netloc=netloc.lower(), path=path, params=params,
                                                    query=OrderedDict(sorted(query_dict.items())))

                        # 维持原始编码状态
                        res_url = keep_chinese(url, new_url)
                        return res_url, rule, extra, ReturnType.normal
                return url, dict(), dict(), ReturnType.rule_not_match
        except Exception as exc:
            logger.exception("url normalize error", exc)
            return url, dict(), dict(), ReturnType.normalize_error
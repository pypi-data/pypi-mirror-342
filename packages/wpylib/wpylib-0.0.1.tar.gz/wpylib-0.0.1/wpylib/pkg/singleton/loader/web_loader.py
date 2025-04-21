"""
@File: web_loader.py
@Date: 2024/2/27 00:07
@Desc: 第三方Web文档加载器
"""
from typing import List, Any
from langchain_core.documents import Document as LangChainDocument
import requests

WEB_LOADER_ENGINE_JINA = "jina"


def requests_get(url: str, params=None, data=None, _json=None, parse_result=True, **kwargs) -> Any:
    """
    使用requests库发起POST请求
    :param url: 请求地址
    :param params: 请求数据
    :param data: 请求数据, 类型为str
    :param _json: 请求数据, 类型为字典(即JSON), 即指的是一个可JSON序列化的Python对象
    :param parse_result: 是否解析结果
    """
    response = requests.get(url=url, params=params, data=data, json=_json, **kwargs)
    if response.status_code not in [0, 200]:
        raise RuntimeError(f"http code error: code={response.status_code} | response={response.text} | url={url}")

    if parse_result:
        try:
            res = response.json()
        except Exception as e:
            raise RuntimeError(f"requests_get exception: e={e}")
        return res
    return response.text


class SimpleWebDocument(LangChainDocument):
    """
    Web文档对象
    """
    # 注意: 如果使用私有属性, 会提示没有此属性, 所以修改为公开属性
    title: str = ""
    url: str = ""
    description: str = ""
    content: str = ""

    def __init__(self, title: str = "", url: str = "", description: str = "", content: str = "", **kwargs: Any):
        super().__init__(content, **kwargs)
        self.title = title
        self.url = url
        self.description = description
        self.content = content

    def get_title(self) -> str:
        """
        获取title
        """
        return self.title

    def get_url(self) -> str:
        """
        获取url
        """
        return self.url

    def get_description(self) -> str:
        """
        获取description
        """
        return self.description

    def get_content(self) -> str:
        """
        获取content
        """
        return self.content


class WebLoader:
    """
    Web文档加载器
    """

    # 变量
    _engine: str = WEB_LOADER_ENGINE_JINA
    _jina_engine_config: dict = {
        "host": "https://r.jina.ai",
        "headers": {
            "Accept": "application/json",
        }
    }

    def __init__(self, engine: str = WEB_LOADER_ENGINE_JINA):
        self._engine = engine

    def load(self, resource_info_list: list[dict], proxies: dict = None, requests_kwargs: dict = None,
             headers: dict = None) -> List[SimpleWebDocument]:
        """
        加载网页
        """
        new_docs: List[SimpleWebDocument] = []

        # JINA爬虫引擎
        if self._engine == WEB_LOADER_ENGINE_JINA:
            new_docs = self._load_by_jina(
                resource_info_list=resource_info_list,
                proxies=proxies,
                requests_kwargs=requests_kwargs,
                headers=headers
            )
        return new_docs

    def _load_by_jina(self, resource_info_list: list[dict], proxies: dict = None, requests_kwargs: dict = None,
                      headers: dict = None) -> List[SimpleWebDocument]:
        """
        使用jina加载网页, jina控制参数都是在header中设置的
        """
        # 参数处理
        if requests_kwargs is None:
            requests_kwargs = {}
        if headers is None:
            headers = {}
        headers = dict(self._jina_engine_config["headers"], **headers)

        # 开始准备爬取网页
        new_docs: List[SimpleWebDocument] = []
        for url_info in resource_info_list:
            url = self._jina_engine_config["host"] + "/" + url_info["url"]
            resp = requests_get(url=url, headers=headers)
            new_docs.append(SimpleWebDocument(
                title=resp["data"]["title"],
                url=resp["data"]["url"],
                description=resp["data"]["description"],
                content=resp["data"]["content"],
            ))

        # 生成新的文档
        return new_docs

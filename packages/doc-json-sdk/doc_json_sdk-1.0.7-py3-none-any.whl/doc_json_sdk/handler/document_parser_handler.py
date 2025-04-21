import os
import time
from typing import Dict, Callable

from alibabacloud_credentials.client import Client as CredClient

from alibabacloud_docmind_api20220711 import models as docmind_api20220711_models
from alibabacloud_docmind_api20220711.client import Client as docmind_api20220711Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from doc_json_sdk.utils.log_util import log
from doc_json_sdk.handler.document_handler_interface import DocumentHandler


class DocumentParserHandlerBase(DocumentHandler):
    """
    文档解析处理器 - 不使用回调函数的版本
    
    -------------------
    
    access_key_id [optional] 阿里云开通DocMind服务AK
    access_key_secret [optional] 阿里云开通DocMind服务SK
    """

    def __init__(self):
        self._access_key_id = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')
        self._access_key_secret = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
        self._cred = CredClient()
        self._DOCMIND_HOST = os.environ.get('DOCMIND_HOST', 'docmind-api.cn-hangzhou.aliyuncs.com')
        log.info("ask host %s", self._DOCMIND_HOST)
        pass

    def get_document_json(self, file_path: str = None, file_url: str = None, **kwargs) -> Dict:
        """
        获取doc json信息

        ----------------------------
            :param file_path: 本地文件路径
            :param file_url: 文件URL
            :param kwargs: 额外参数
                - formula_enhancement: 公式增强
                - llm_enhancement: LLM增强
                - http_proxy: HTTP代理
                - https_proxy: HTTPS代理
        :return: doc-json
        """
        if file_url is not None:
            response = self._submit_url(file_url, **kwargs)
        elif file_path is not None:
            response = self._submit_file(file_path, **kwargs)
        else:
            raise ValueError("file_url and file_path is null")
        if response.body.data.id is None:
            raise Exception(response.body)
        
        # 获取请求ID并查询结果
        request_id = response.body.data.id
        log.info("Doc parser job submitted with ID: %s", request_id)
        
        # 等待处理完成
        status = None
        while True:
            status_response = self._query_status(request_id, **kwargs)
            if status_response.status == "success":
                status = status_response
                break
            elif status_response.status == "fail":
                raise Exception(f"Document parsing failed: {status_response}")
            # 继续等待处理
            time.sleep(2)
        
        # 获取完整结果
        result = self._get_complete_result(request_id, status.number_of_successful_parsing, **kwargs)
        return result

    def _submit_file(self, file_path: str, **kwargs):
        config = open_api_models.Config(
            access_key_id=self._access_key_id if self._access_key_id is not None else self._cred.get_access_key_id(),
            access_key_secret=self._access_key_secret if self._access_key_secret is not None else self._cred.get_access_key_secret(),
            connect_timeout=60000,
            read_timeout=60000,
            endpoint=self._DOCMIND_HOST,
            http_proxy=kwargs["http_proxy"] if "http_proxy" in kwargs else None,
            https_proxy=kwargs["https_proxy"] if "https_proxy" in kwargs else None
        )
        client = docmind_api20220711Client(config)
        formula_enhancement = True if "formula_enhancement" in kwargs and kwargs["formula_enhancement"] else False
        llm_enhancement = True if "llm_enhancement" in kwargs and kwargs["llm_enhancement"] else False
        
        request = docmind_api20220711_models.SubmitDocParserJobAdvanceRequest(
            file_url_object=open(file_path, "rb"),
            file_name=file_path.rsplit("/", 1)[-1],
            file_name_extension=file_path.rsplit(".", 1)[-1],
            formula_enhancement=formula_enhancement,
            llm_enhancement=llm_enhancement
        )
        runtime = util_models.RuntimeOptions()
        runtime.read_timeout = 60000
        runtime.connect_timeout = 60000
        if "http_proxy" in kwargs:
            runtime.https_proxy = kwargs["http_proxy"]
        if "http_proxys" in kwargs:
            runtime.https_proxys = kwargs["http_proxys"]
        try:
            response = client.submit_doc_parser_job_advance(request, runtime)
            log.info("doc_parser_job_advance with %s", response.body)
            return response
        except Exception as error:
            log.error(str(error))
            UtilClient.assert_as_string(str(error))
            raise error

    def _submit_url(self, file_url: str, **kwargs):
        config = open_api_models.Config(
            access_key_id=self._access_key_id if self._access_key_id is not None else self._cred.get_access_key_id(),
            access_key_secret=self._access_key_secret if self._access_key_secret is not None else self._cred.get_access_key_secret(),
            connect_timeout=60000,
            read_timeout=60000,
            endpoint=self._DOCMIND_HOST,
            http_proxy=kwargs["http_proxy"] if "http_proxy" in kwargs else None,
            https_proxy=kwargs["https_proxy"] if "https_proxy" in kwargs else None
        )
        client = docmind_api20220711Client(config)
        file_path = file_url[:file_url.rfind("?")] if (file_url.rfind("?") != -1) else file_url[file_url.rfind("/"):]
        formula_enhancement = True if "formula_enhancement" in kwargs and kwargs["formula_enhancement"] else False
        llm_enhancement = True if "llm_enhancement" in kwargs and kwargs["llm_enhancement"] else False
        
        request = docmind_api20220711_models.SubmitDocParserJobRequest(
            file_url=file_url,
            file_name=file_path.rsplit("/", 1)[-1],
            file_name_extension=file_path.rsplit(".", 1)[-1],
            formula_enhancement=formula_enhancement,
            llm_enhancement=llm_enhancement
        )
        try:
            response = client.submit_doc_parser_job(request)
            log.info("doc_parser_job with %s", response.body)
            return response
        except Exception as error:
            log.error(str(error))
            UtilClient.assert_as_string(str(error))
            raise error

    def _query_status(self, request_id, **kwargs):
        config = open_api_models.Config(
            access_key_id=self._access_key_id if self._access_key_id is not None else self._cred.get_access_key_id(),
            access_key_secret=self._access_key_secret if self._access_key_secret is not None else self._cred.get_access_key_secret(),
            connect_timeout=60000,
            read_timeout=60000,
            endpoint=self._DOCMIND_HOST,
            http_proxy=kwargs["http_proxy"] if "http_proxy" in kwargs else None,
            https_proxy=kwargs["https_proxy"] if "https_proxy" in kwargs else None
        )
        client = docmind_api20220711Client(config)
        request = docmind_api20220711_models.QueryDocParserStatusRequest(id=request_id)
        try:
            response = client.query_doc_parser_status(request)
            return response.body.data
        except Exception as error:
            log.error(str(error))
            UtilClient.assert_as_string(str(error))
            raise error

    def _get_complete_result(self, request_id, total_layouts, **kwargs):
        """
        获取完整的解析结果
        """
        config = open_api_models.Config(
            access_key_id=self._access_key_id if self._access_key_id is not None else self._cred.get_access_key_id(),
            access_key_secret=self._access_key_secret if self._access_key_secret is not None else self._cred.get_access_key_secret(),
            connect_timeout=60000,
            read_timeout=60000,
            endpoint=self._DOCMIND_HOST,
            http_proxy=kwargs["http_proxy"] if "http_proxy" in kwargs else None,
            https_proxy=kwargs["https_proxy"] if "https_proxy" in kwargs else None
        )
        client = docmind_api20220711Client(config)
        
        # 一次性获取所有结果
        request = docmind_api20220711_models.GetDocParserResultRequest(
            id=request_id,
            layout_step_size=total_layouts,  # 获取所有布局
            layout_num=0  # 从第一个开始
        )
        try:
            response = client.get_doc_parser_result(request)
            return response.body.data
        except Exception as error:
            log.error(str(error))
            UtilClient.assert_as_string(str(error))
            raise error

    def get_document_json_by_request_id(self, request_id: str, **kwargs):
        """
        通过请求ID获取文档JSON
        :param request_id: 请求ID
        :return: 文档JSON
        """
        # 查询状态
        status = self._query_status(request_id, **kwargs)
        if status.status != "success":
            raise Exception(f"Document parsing not successful: {status.status}")
        
        # 获取结果
        result = self._get_complete_result(request_id, status.number_of_successful_parsing, **kwargs)
        return result


class DocumentParserHandler(DocumentParserHandlerBase):
    """
    文档解析处理器 - 不使用回调函数的版本
    
    -------------------
    
    access_key_id [optional] 阿里云开通DocMind服务AK
    access_key_secret [optional] 阿里云开通DocMind服务SK
    """

    def __init__(self):
        super().__init__()

    def get_document_json(self, file_path: str = None, file_url: str = None, **kwargs) -> Dict:
        """
        获取doc json信息

        ----------------------------
            :param file_path: 本地文件路径
            :param file_url: 文件URL
            :param kwargs: 额外参数
                - formula_enhancement: 公式增强
                - llm_enhancement: LLM增强
                - http_proxy: HTTP代理
                - https_proxy: HTTPS代理
        :return: doc-json
        """
        if file_url is not None:
            response = self._submit_url(file_url, **kwargs)
        elif file_path is not None:
            response = self._submit_file(file_path, **kwargs)
        else:
            raise ValueError("file_url and file_path is null")
        if response.body.data.id is None:
            raise Exception(response.body)
        
        # 获取请求ID并查询结果
        request_id = response.body.data.id
        log.info("Doc parser job submitted with ID: %s", request_id)
        
        # 等待处理完成
        status = None
        while True:
            status_response = self._query_status(request_id, **kwargs)
            if status_response.status == "success":
                status = status_response
                break
            elif status_response.status == "fail":
                raise Exception(f"Document parsing failed: {status_response}")
            # 继续等待处理
            time.sleep(2)
        
        # 获取完整结果
        result = self._get_complete_result(request_id, status.number_of_successful_parsing, **kwargs)
        return result


class DocumentParserWithCallbackHandler(DocumentParserHandlerBase):
    """
    文档解析处理器 - 使用回调函数的版本
    
    -------------------
    
    access_key_id [optional] 阿里云开通DocMind服务AK
    access_key_secret [optional] 阿里云开通DocMind服务SK
    """
    __callback: Callable[[Dict], None]
    __default_step: int

    def __init__(self, callback: Callable[[Dict], None], default_step: int = 20):
        super().__init__()
        self.__callback = callback
        self.__default_step = default_step

    def get_document_json(self, file_path: str = None, file_url: str = None, **kwargs):
        """
        获取doc json信息，通过回调函数处理结果

        ----------------------------
            :param file_path: 本地文件路径
            :param file_url: 文件URL
            :param kwargs: 额外参数
                - formula_enhancement: 公式增强
                - llm_enhancement: LLM增强
                - http_proxy: HTTP代理
                - https_proxy: HTTPS代理
        :return: None
        """
        if file_url is not None:
            response = self._submit_url(file_url, **kwargs)
        elif file_path is not None:
            response = self._submit_file(file_path, **kwargs)
        else:
            raise ValueError("file_url and file_path is null")
        if response.body.data is None or response.body.data.id is None:
            raise EnvironmentError("response error", response)
        
        response_id = response.body.data.id
        # print(response_id)
        number_of_successful_parsing = 0
        number_of_processing = 0
        res = self._query_status(response_id, **kwargs)
        while 1:
            if number_of_processing < number_of_successful_parsing:
                result = self._query_group(response_id, number_of_processing, self.__default_step, **kwargs)
                for layout in result["layouts"]:
                    self.__callback(layout)
                number_of_processing = number_of_processing + self.__default_step
            elif res and res.status == "success" and number_of_processing >= number_of_successful_parsing:
                break
            if res and res.status == "fail":
                break
            elif res and res.status == "success" and res.number_of_successful_parsing > number_of_successful_parsing:
                number_of_successful_parsing = res.number_of_successful_parsing
            elif res and res.status == 'processing':
                res = self._query_status(response_id, **kwargs)
                number_of_successful_parsing = res.number_of_successful_parsing
            elif res and res.status == 'init':
                res = self._query_status(response_id, **kwargs)

    def get_document_json_by_request_id(self, request_id: str, **kwargs):
        raise NameError("DocumentParserWithCallbackHandler does not support get_document_json_by_request_id")

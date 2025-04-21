"""
@File: chain.py
@Date: 2024/12/10 10:00
@desc: 第三方chain模块
"""
from langchain import LLMChain
from wpylib.pkg.langchain.log_callback import LogCallback
from langchain_core.prompts.base import BasePromptTemplate
from src.pkg.langfuse.langfuse import global_instance_langfuse
from langchain_core.language_models.base import BaseLanguageModel
from src.pkg.localcache.localcache import global_instance_localcache


def get_chain_callbacks() -> list:
    """
    获取回调函数
    :return:
    """
    callbacks = [
        global_instance_langfuse.update_instance_handler(
            trace_name="",
            session_id=global_instance_localcache.get_log_id(),
        )
    ]
    return callbacks


def create_chain(model: BaseLanguageModel, prompt: BasePromptTemplate, verbose: bool = False) -> LLMChain:
    """
    创建chain
    chain.invoke(*args, config={"callbacks": get_callbacks()}, **kwargs)
    chain.predict(*args, callbacks=get_callbacks(), **kwargs)
    chain.apredict(*args, callbacks=get_callbacks(), **kwargs)
    :param model: 模型
    :param prompt: 提示词
    :param verbose: 是否开启打印
    :return:
    """
    return LLMChain(
        llm=model,
        prompt=prompt,
        verbose=verbose,
        callbacks=[LogCallback()]
    )

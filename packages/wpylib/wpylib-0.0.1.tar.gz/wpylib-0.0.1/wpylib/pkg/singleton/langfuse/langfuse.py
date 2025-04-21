"""
@File: langfuse.py
@Date: 2024/12/10 10:00
@Desc: 第三方langfuse单例模块
"""
from wpylib.util.x.xtyping import is_not_none
from langfuse.callback import CallbackHandler
from src.const.const import ENV_DEV, ENV_TEST
from langfuse import Langfuse as OfficialLangfuse
from src.pkg.logger.logger import global_instance_logger
from src.init.init import global_config as init_global_config
from src.pkg.localcache.localcache import global_instance_localcache


class Langfuse:
    """
    Langfuse对象
    """
    # 基础属性
    _is_not_prod: bool
    _langfuse_config: dict

    # 初始化需要的配置
    _global_config: dict

    # 使用到的实例对象
    _instance_langfuse: OfficialLangfuse = None
    _instance_langfuse_handler: CallbackHandler = None

    # 单例类
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self, langfuse_config: dict, global_config: dict = None):
        if is_not_none(global_config) and "env" in global_config:
            self._is_not_prod = global_config["env"] in (ENV_DEV, ENV_TEST)
        self._langfuse_config = langfuse_config
        self._global_config = global_config

        # 初始化langfuse实例对象
        self._instance_langfuse = OfficialLangfuse(
            secret_key=self._langfuse_config["secret_key"],
            public_key=self._langfuse_config["public_key"],
            host=self._langfuse_config["host"],
            # debug=self._is_not_prod,
            debug=False,
            # flush_interval=5
        )

        # 初始化langfuse的回调handler
        self._instance_langfuse_handler = CallbackHandler(
            # langfuse凭证
            secret_key=self._langfuse_config["secret_key"],
            public_key=self._langfuse_config["public_key"],
            host=self._langfuse_config["host"],
            # debug=self._is_not_prod,
            debug=False,
            # flush_interval=5
        )

        # 连接状态
        connect_success = self._instance_langfuse.auth_check()
        if connect_success:
            global_instance_logger.log_info(
                "connected to langfuse successfully",
                {"langfuse_config": langfuse_config}
            )
        else:
            global_instance_logger.log_error("failed to connect langfuse", {"langfuse_config": langfuse_config})

    def get_instance(self) -> OfficialLangfuse:
        """
        获取_instance_langfuse实例对象
        """
        return self._instance_langfuse

    def get_instance_handler(self) -> CallbackHandler:
        """
        获取_instance_langfuse_handler实例对象
        """
        return self._instance_langfuse_handler

    def update_instance_handler(self, **kwargs) -> CallbackHandler:
        """
        更新langfuse_handler实例
        1. 不使用这种方式来更新状态, 因为这种方式和目前设计不符而且只有invoke调用的时候才可以传递
           langfuse_context.update_current_trace()
           langfuse_context.get_current_langchain_handler()
        2. 注意这个大坑, 必须创建一个新的对象, 保证线程安全, 不然queue的get操作会一直阻塞导致无法返回数据, 所以就不会上传到langfuse
           所以这里自动创建一个新对象
        """
        if "session_id" not in kwargs:
            kwargs["session_id"] = global_instance_localcache.get_log_id()
        if "trace_name" not in kwargs:
            kwargs["trace_name"] = "unknown"
        if "tags" not in kwargs:
            kwargs["tags"] = []

        new_handler = CallbackHandler(
            secret_key=self._langfuse_config["secret_key"],
            public_key=self._langfuse_config["public_key"],
            host=self._langfuse_config["host"],
            # debug=self._is_not_prod,
            debug=False,
            session_id=kwargs["session_id"],
            trace_name=kwargs["trace_name"],
            tags=kwargs["tags"],
        )
        return new_handler

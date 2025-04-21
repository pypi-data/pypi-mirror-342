"""
@File: stream_response.py
@Date: 2024/12/10 10:00
@Desc: 第三方流式响应模块
"""
from src.util.x.xjson import stringify
from src.app.http.code_msg import SYS_ERROR
from src.pkg.sse.stream_queue import StreamQueue
from src.pkg.logger.logger import global_instance_logger
import threading
import queue

STREAM_MESSAGE_PING = "ping"


class StreamResponseGenerator(object):
    """
    流式响应
    """

    def __init__(self, target, args=(), kwargs=None, queue_max: int = 20):
        self.queue = StreamQueue(queue_max)
        if not kwargs:
            kwargs = {}
        kwargs['queue'] = self.queue
        self.thread = threading.Thread(None, target, 'stream_response_thread', args, kwargs, daemon=True)
        self.target = target
        self.ev = threading.Event()
        self.ev.clear()

    def __iter__(self):
        self.thread.start()
        try:
            while self.queue.is_running():
                try:
                    e = self.queue.get(True, 3)
                except queue.Empty:
                    self.queue.send_message(type_str=STREAM_MESSAGE_PING)
                    continue
                if not e:
                    continue
                if e['event'] == 'message':
                    self.queue.task_done()
                    yield self._format_message(**e)
                    continue
                elif e['event'] == 'message_end':
                    self.queue.task_done()
                    yield self._format_message(**e)
                    self.queue.close()
                    break
        except GeneratorExit:
            # 无法再yield
            # 此异常出现的时机为第三方 sse 断开连接导致无法yield, 该不可抗拒因素导致的异常无法处理，因此忽略该异常仅 log info
            global_instance_logger.log_info("stream_response GeneratorExit")
            self.queue.close()
            self.thread.join(5)
            return
        except Exception as e:
            global_instance_logger.log_error("stream_response exception", {"e": e})
            self.queue.send_message_end({"code": SYS_ERROR, "msg": "服务异常"})
            return
        finally:
            global_instance_logger.log_info("stream_response finally")
            self.queue.close()
            self.thread.join(5)

    def _format_message(self, event, data):
        """
        格式化消息
        :param event: 事件
        :param data: 数据
        :return:
        """
        return 'data: {}\n\n'.format(stringify({
            'event': event,
            'data': data
        }))

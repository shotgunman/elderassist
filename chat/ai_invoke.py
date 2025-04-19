from openai import OpenAI, OpenAIError
import threading
import time


# 定义读写锁
class ReadWriteLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0
        self._writers = 0

    def acquire_read(self):
        """Acquire a read lock."""
        with self._read_ready:
            while self._writers > 0:
                self._read_ready.wait()
            self._readers += 1

    def release_read(self):
        """Release a read lock."""
        with self._read_ready:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    def acquire_write(self):
        """Acquire a write lock."""
        with self._read_ready:
            while self._readers > 0 or self._writers > 0:
                self._read_ready.wait()
            self._writers += 1

    def release_write(self):
        """Release a write lock."""
        with self._read_ready:
            self._writers -= 1
            self._read_ready.notify_all()


# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="sk-qxDxVejTBrBIrMbonD05zwmW1Nw5RDRaWKb5NTaFLDvXnpzW",  # 替换为你的 API Key
    base_url="http://127.0.0.1:9988/v1",
)

# 定义系统消息
system_messages = [
    {"role": "system",
     "content": "你叫南山寿，你是一位贴心的老年助手，专门为老年人提供帮助和支持。你需要对用户聊天记录中的信息包含的问题做出回答。你熟悉老年人的生活需求和习惯，能够用简单、亲切、耐心的方式与他们交流。你的目标是让老年人的生活更加便捷、舒适和安心。你会为他们提供关于健康养生、日常起居、情感陪伴、社交娱乐等方面的建议和帮助。同时，你会避免使用复杂的技术术语，尽量用通俗易懂的语言表达。"},
]

# 定义全局消息列表和读写锁
messages = []
rw_lock = ReadWriteLock()


def make_messages(input_messages: list[dict], n: int = 20) -> list[dict]:
    """
    控制每次请求的消息数量，使其保持在一个合理的范围内。
    """
    # 获取写锁
    rw_lock.acquire_write()
    try:
        # 添加用户消息到全局消息列表
        messages.extend(input_messages)

        # 构建新的消息列表
        new_messages = system_messages[:]
        if len(messages) > n:
            new_messages.extend(messages[-n:])
        else:
            new_messages.extend(messages)
    finally:
        # 释放写锁
        rw_lock.release_write()

    return new_messages


def chat(input_data: list[dict]) -> str:
    """
    支持多轮对话的函数。
    """
    try:
        # 构建消息列表
        messages_to_send = make_messages(input_data)

        messages_to_send.append(system_messages[0])

        # 调用 API
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages_to_send,
            temperature=0.3,
        )

        # 获取助手回复
        assistant_message = completion.choices[0].message

        # 获取写锁
        rw_lock.acquire_write()
        try:
            # 将助手消息添加到全局消息列表
            messages.append(assistant_message)
        finally:
            # 释放写锁
            rw_lock.release_write()

        return assistant_message.content
    except OpenAIError as e:
        # 捕获 OpenAI API 的异常
        print(f"API Error: {e}")
        return "Error: Unable to complete the request."
    except Exception as e:
        # 捕获其他异常
        print(f"Unexpected Error: {e}")
        return "Error: An unexpected error occurred."
    finally:
        # 限制 API 调用频率
        time.sleep(1)


'''

# 废弃的测试内容

def test_chat(thread_id):
    print(f"Thread {thread_id} starting...")
    response = chat(f"Thread {thread_id} says hello!")
    print(f"Thread {thread_id} got response: {response}")

# 创建多个线程测试
threads = []
for i in range(1):
    thread = threading.Thread(target=test_chat, args=(i,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()
'''

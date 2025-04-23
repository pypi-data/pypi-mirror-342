import threading

from datetime import datetime, timezone

from pyutils_spirit.annotation.interpreter import singleton


@singleton(signature="spirit_id")
class SpiritID:
    __instance = None  # 单例模式实现
    __lock = threading.Lock()  # 类级别锁用于单例创建

    # 初始化方法设为私有
    def __init__(self):
        self.BEGIN_TIMESTAMP = 1695600000  # 开始时间戳
        self.COUNT_BIT = 32  # 位移位数
        self.incr_count = 0
        self.instance_lock = threading.Lock()  # 实例级别锁用于计数器操作

    def _get_all_seconds(self):
        """获取当前UTC时间与基准时间的秒差"""
        now = datetime.now(timezone.utc)
        return int(now.timestamp()) - self.BEGIN_TIMESTAMP  # 精确到秒的时间差[4](@ref)

    def next(self, prefix):
        """生成带前缀的ID"""
        timestamp_part = self._get_all_seconds()

        with self.instance_lock:  # 保证原子操作[4](@ref)
            self.incr_count += 1
            if self.incr_count >= (1 << self.COUNT_BIT):  # 处理32位溢出
                raise OverflowError("Sequence number overflow")

            combined = (timestamp_part << self.COUNT_BIT) | self.incr_count
            return f"{prefix}{combined}"

from datetime import time, datetime, timedelta
from abc import ABC, abstractmethod
import pytz

class BaseSymbol(ABC):
    def __init__(self, symbol='', exchange=None, timezone=pytz.timezone("Asia/Hong_Kong")):
        self.symbol = symbol
        self.exchange = exchange or "Unknown"
        self.timezone = timezone
        self.trading_hours = self._init_trading_hours()

    @abstractmethod
    def _init_trading_hours(self):
        """子类必须实现，定义一周每一天的交易时间"""
        pass

    def is_trading_time(self, current_datetime: datetime) -> bool:
        """检查当前时间是否在交易时间内"""
        # 将输入时间转换为目标时区
        if current_datetime.tzinfo is None:
            # 如果输入时间没有时区信息，假设为 UTC
            current_datetime = pytz.utc.localize(current_datetime)
        local_datetime = current_datetime.astimezone(self.timezone)
        
        current_weekday = local_datetime.weekday()
        current_time = local_datetime.time()

        # 获取当前交易日的交易时间
        if current_weekday not in self.trading_hours:
            return False

        for start_time, end_time in self.trading_hours[current_weekday]:
            if start_time <= end_time:
                # 同一天内：start_time <= current_time <= end_time
                if start_time <= current_time <= end_time:
                    return True
            else:
                # 跨天情况：current_time >= start_time 或 current_time <= end_time
                if current_time >= start_time:
                    return True
                elif current_time <= end_time:
                    # 确保次日仍在交易日范围内（例如，周五到周六）
                    next_day = local_datetime + timedelta(days=1)
                    return next_day.weekday() in self.trading_hours
        return False
    
    @abstractmethod
    def __str__(self):
        pass
from datetime import datetime


class DateUtils(object):
    @staticmethod
    def parse_date_string(date_str: str, format_str: str = "%a %b %d %I:%M:%S %p %Y") -> datetime:
        """
        将日期字符串转换为 datetime 对象。

        :param date_str: 要解析的日期字符串
        :param format_str: 日期字符串的格式，默认值为 "%a %b %d %I:%M:%S %p %Y"
                            例如："Fri Aug 09 02:08:37 pm 2024"
        :return: 转换后的 datetime 对象
        :raises ValueError: 如果日期字符串与提供的格式不匹配，抛出异常
        """
        try:
            return datetime.strptime(date_str, format_str)
        except ValueError as e:
            raise ValueError(f"无法解析日期字符串 '{date_str}'，请检查格式。") from e

    @staticmethod
    def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        将 datetime 对象格式化为字符串。

        :param date: datetime 对象
        :param format_str: 格式化字符串，默认值为 "%Y-%m-%d %H:%M:%S"
        :return: 格式化后的日期字符串
        """
        return date.strftime(format_str)

    @staticmethod
    def get_current_datetime(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        获取当前时间并以指定格式返回字符串。

        :param format_str: 格式化字符串，默认值为 "%Y-%m-%d %H:%M:%S"
        :return: 当前时间的格式化字符串
        """
        return datetime.now().strftime(format_str)

    @staticmethod
    def convert_to_timestamp_millis(date_string):
        # 定义日期格式
        date_format = "%Y-%m-%d %H:%M:%S"

        # 将字符串转换为 datetime 对象
        date_obj = datetime.strptime(date_string, date_format)

        # 返回毫秒级时间戳
        return int(date_obj.timestamp() * 1000)

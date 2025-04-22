# custom_fields.py
from django.db import models
from ulid import ULID
from datetime import datetime

class JULIDField(models.CharField):
    description = "ULID (Universally Unique Lexicographically Sortable Identifier 通用唯一字典排序标识符)"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 32  # ULID 是 26 个字符的字符串。为了兼容uuid32
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_u12(dt: datetime = None) -> str:
        """
        获取12位ULID。截取ulid26位的第2-10位为时间，第11-13位为随机数
        @param dt: 指定生成时间，精确到毫秒。默认为当前时间
        """
        if not dt:
            dt = datetime.now()
        u12 = str(ULID.from_datetime(dt))[1:13]
        # print('get_u12', u12, dt)
        JULIDField.from_u12(u12)
        return u12.lower()

    @staticmethod
    def from_u12(u12: str) -> ULID:
        if len(u12) != 12:
            return
        u26 = ULID.from_str('0' + u12 + '0000000000000')
        # print('from_u12', u26, u26.datetime)
        return u26


    # @staticmethod
    # def get_u16(dt: datetime = None) -> str:
    #     """
    #     获取12位ULID
    #     @param dt: 指定生成时间，精确到毫秒。默认为当前时间
    #     """
    #     if not dt:
    #         dt = datetime.now()
    #     u16 = str(ULID.from_datetime(dt))[0:16]
    #     return u16
    #
    # @staticmethod
    # def from_u16(u16: str) -> ULID:
    #     if len(u16) != 16:
    #         return
    #     u26 = ULID.from_str(u16 + "0000000000")
    #     # print('from_u12', u26, u26.timestamp)
    #     return u26


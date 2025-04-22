import socket
import sys
import uuid

from django.db import models
from django.contrib import admin
from django.utils import timezone
from .libs.DjangoUeditor.models import UEditorField
from django.utils.html import format_html

from .utils.j_django_simple_api import JDjangoSimpleApi
from .utils.j_ulid_field import JULIDField

if 'xj_user' in sys.modules:
    from xj_user.models import BaseInfo

# from apps.user.models import User
# from apps.user.models import BaseInfo

models.Model.to_json = JDjangoSimpleApi.serialize_model
# models.query.QuerySet.to_json = JDjangoSimpleApi.serialize_queryset
# models.query.RawQuerySet.to_json = JDjangoSimpleApi.serialize_queryset

hostname = socket.gethostname()
my_ip_addr = socket.gethostbyname(hostname)

content_coding_choices = [('TEXT', '文本(支持换行)'), ('HTML', 'HTML超文本语言'), ('MARKDOWN', 'MD标记语言'), ('UBB', 'UBB标记语言')]
access_level_choices = [
    (1, '所有人 EVERYONE'),
    (2, '访客 VISITOR'),
    (3, '会员 STAFF'),
    (4, '主管 MANAGER'),
    (5, '管理员 ADMINISTRATOR'),
    (11, '好友 FRIEND'),
    (12, '指定人 SOMEONE'),
    (13, '指定群组 GROUP'),
    (14, '仅与用户 EACH_OTHER'),
    (15, '私人可见 PRIVATE'),
    (21, '指定角色 ROLE'),
    (31, '阅后即焚(只能看一次) BURN_AFTER_READ'),
    (32, '已焚毁 BURNED_AND_READ'),
]


class Thread(models.Model):
    """ 1、Thread_Thread 信息主表  [NF2] """

    id = models.BigAutoField(verbose_name='ID', primary_key=True, help_text='')
    uuid = JULIDField(verbose_name='UUID', default=JULIDField.get_u12(), unique=True, editable=True,
                      db_index=True, help_text='系统默认使用ULID12位码，并兼容UUID32位码')
    category = models.ForeignKey(verbose_name='类别ID', to='ThreadCategory', on_delete=models.DO_NOTHING, null=True,
                                 blank=True, db_constraint=False, help_text='')
    classify = models.ForeignKey(verbose_name='分类ID', to='ThreadClassify', on_delete=models.DO_NOTHING, null=True,
                                 blank=True, db_constraint=False, help_text='')
    show = models.ForeignKey(verbose_name='展示ID', to='ThreadShow', null=True, blank=True, on_delete=models.DO_NOTHING,
                             related_name='+', db_constraint=False,
                             help_text='如果没有传入显示类型，则使用分类表中的默认显示类型')  # 如果没有传入显示类型，则使用分类表中的默认显示类型
    user_id = models.BigIntegerField(verbose_name='用户ID', db_column='user_id', db_index=True, blank=True, null=True, help_text='')
    user_uuid = JULIDField(verbose_name='用户UUID', editable=True, blank=True, null=True,
                           db_index=True)
    with_user_id = models.BigIntegerField(verbose_name='与用户ID', db_column='with_user_id', blank=True, null=True, db_index=True, help_text='')
    with_user_uuid = JULIDField(verbose_name='与用户UUID', editable=True, blank=True, null=True,
                           db_index=True)
    group_id = models.BigIntegerField(verbose_name='分组ID', blank=True, null=True, db_index=True, help_text='')
    thread_no = models.CharField(verbose_name='信息编号', max_length=32, blank=True, null=True, db_index=True,
                                 help_text='')  # 20230823 改contract_code为thread_no信息编号 by Sieyoo。
    title = models.CharField(verbose_name='标题', max_length=128, blank=True, null=True, db_index=True, help_text='')
    subtitle = models.CharField(verbose_name='子标题', max_length=255, blank=True, null=True, help_text='')
    summary = models.CharField(verbose_name='摘要', max_length=2048, blank=True, null=True, default="", help_text='')
    content = UEditorField(verbose_name='内容', blank=True, null=True,
                           help_text='信息列表页是不返回内容字段的，因为这会增加数据的体积')
    content_coding = models.CharField(verbose_name='内容译码类型', max_length=8, blank=True, null=True,
                                      choices=content_coding_choices, help_text='')
    keywords = models.CharField(verbose_name='关键字', max_length=1024, blank=True, null=True, help_text='多个用;号分隔')
    access_level = models.IntegerField(verbose_name='访问级别', blank=True, null=True, db_index=True,
                                       choices=access_level_choices, help_text='')  # add-2022-05-20
    author = models.CharField(verbose_name='作者/主办者', max_length=128, blank=True, null=True,
                              help_text='')  # add-2022-05-20
    region_code = models.CharField(verbose_name='所属行政区划编码', max_length=12, blank=True, null=True, db_index=True,
                                   help_text='行政编码格式：省(2), 市(2), 区县(2), 乡镇街道(3), 村(3)')
    ip = models.GenericIPAddressField(verbose_name='网络IP', blank=True, null=True, protocol='both',
                                      default=socket.gethostbyname(socket.gethostname()))  # 只记录创建时的IP
    # has_enroll = models.BooleanField(verbose_name='有报名', blank=True, null=True, help_text='')
    # has_fee = models.BooleanField(verbose_name='有小费', blank=True, null=True, help_text='')
    # has_comment = models.BooleanField(verbose_name='有评论', blank=True, null=True, help_text='')
    # has_location = models.BooleanField(verbose_name='有定位', blank=True, null=True, help_text='')
    cover = models.CharField(verbose_name='封面', max_length=1024, blank=True, null=True, help_text='')
    photos = models.JSONField(verbose_name='照片集', blank=True, null=True,
                              help_text='')  # 对象数组，存放{id, url} 获取列表时使用，查看详细时再匹配资源表
    video = models.CharField(verbose_name='视频', max_length=1024, blank=True, null=True, help_text='')
    files = models.JSONField(verbose_name='文件集', blank=True, null=True, help_text='')  # 对象数组，存放{id, url}
    price = models.DecimalField(verbose_name='价格/原价', max_digits=32, decimal_places=8, null=True, blank=True,
                                help_text='')  # add-2022-05-20
    is_original = models.BooleanField(verbose_name='是否原创/独有权', blank=True, null=True, help_text='')  # add-2022-05-20
    link = models.URLField(verbose_name='跳转/参考链接', max_length=1024, blank=True, null=True, help_text='跳转/参考链接')
    logs = models.JSONField(verbose_name='日志', blank=True, null=True,
                            help_text='')  # 用户的修改记录等日志信息，数组对象类型 使用CRC32来比较哪些字段被修改过，并记录
    more = models.JSONField(verbose_name='更多信息', blank=True, null=True, help_text='')
    sort = models.IntegerField(verbose_name="排序", blank=True, null=True, help_text='默认排序为升序')
    language_code = models.CharField(verbose_name='语言代码', max_length=2, blank=True, null=True, help_text='')
    # is_subitem_thread = models.BooleanField(verbose_name='是否是分项', default=0, blank=True, null=True,
    #                                         help_text='是否是主项信息的分项信息')
    # main_thread = models.ForeignKey(verbose_name='主项信息ID', to="Thread", on_delete=models.DO_NOTHING, related_name='+',
    #                                 blank=True, null=True,
    #                                 db_constraint=False, help_text='主项信息ID')
    remark = models.CharField(verbose_name='备注', max_length=1024, blank=True, null=True, help_text='')
    create_time = models.DateTimeField(verbose_name='创建时间', blank=True, null=True, default=timezone.now, db_index=True,
                                       help_text='')
    update_time = models.DateTimeField(verbose_name='更新时间', blank=True, null=True, auto_now=True, db_index=True,
                                       help_text='')  # 不显示，系统自动填。
    publish_time = models.DateTimeField(verbose_name='发布时间', blank=True, null=True, default=timezone.now, db_index=True,
                                        help_text='')  # add-2023-09-13
    is_delete = models.BooleanField(verbose_name='是否删除', blank=True, null=True, default=0, db_index=True)

    class Meta:
        db_table = 'thread'  # 指定数据库的表名，否则默认会显示app名+class名。
        verbose_name_plural = '01. 信息 - 基本信息'  # 指定管理界面的别名，否则默认显示class名。末尾不加s。
        # ordering = ['-create_time']  # TODO 不能在模块设计中写排序，否则会导致所有查询都进行排序，会影响速度，尤其是这张表是大数据表，所有已使用代码都要改掉 sieyoo by 20221105

    def __str__(self):
        return f"({self.id}) {str(self.title)[0:30]}..." if len(str(self.title)) > 30 else f"({self.id}) {self.title}"

    # 注：本代码仅做试验，因为这种写法非常吃数据库资源 20230824 by Sieyoo
    def username_query(self):
        user_set = BaseInfo.objects.filter(id=self.user_id).first()
        return format_html(
            '<span style="display: inline-block; width: 100px">{}</span>',
            f"{user_set.fullname} ({user_set.username})"
        ) if user_set else f"({self.user_id})"

    username_query.short_description = '用户'

    # @property  # 只能用在实例时访问，query_set需要遍历很麻烦，无法直接导出 20241226 by Sieyoo
    # def uuid_str(self):
    #     return str(self.uuid).replace('-', '') if self.uuid else None

    # 判断指定字段长度,超出部分用省略号代替
    @admin.display
    def title_short(self):
        return format_html(
            '<span style="display: inline-block; width: 200px; font-weight: bold;">{}</span>',
            str(self.title)
        )

    title_short.short_description = '标题'

    # 判断指定字段长度,超出部分用省略号代替
    def subtitle_short(self):
        return f'{str(self.subtitle)[0:30]}...' if len(str(self.subtitle)) > 30 else str(self.subtitle)

    subtitle_short.short_description = '子标题'

    # 判断指定字段长度,超出部分用省略号代替
    def summary_short(self):
        summary = f'{str(self.summary)[0:50]}...' if len(str(self.summary)) > 50 else str(self.summary)
        return format_html(
            '<span style="display: inline-block; width: 200px; font-size: 12px;">{}</span>',
            str(summary)
        )

    summary_short.short_description = '摘要'

    # 判断指定字段长度,超出部分用省略号代替
    def content_short(self):
        content = f'{str(self.content)[0:50]}...' if len(str(self.content)) > 50 else str(self.content)
        return format_html(
            '<span style="display: inline-block; width: 200px; font-size: 12px;">{}</span>',
            str(content)
        )

    # 字段数据处理后,字段verbose_name参数失效
    # 需要重新指定,否则列表页字段名显示的是方法名(short_content)
    content_short.short_description = '内容'

    def cover_short(self):
        return f'{str(self.cover)[0:15]}...' if len(str(self.cover)) > 15 else str(self.cover)

    cover_short.short_description = '封面'

    def video_short(self):
        return f'{str(self.video)[0:15]}...' if len(str(self.video)) > 15 else str(self.video)

    video_short.short_description = '视频'

    def photos_short(self):
        return f'{str(self.photos)[0:15]}...' if len(str(self.photos)) > 15 else str(self.photos)

    photos_short.short_description = '照片集'

    def files_short(self):
        return f'{str(self.files)[0:15]}...' if len(str(self.files)) > 15 else str(self.files)

    files_short.short_description = '文件集'

    def logs_short(self):
        return f'{str(self.logs)[0:15]}...' if len(str(self.logs)) > 15 else str(self.logs)

    logs_short.short_description = '日志'

    def more_short(self):
        return f'{str(self.more)[0:30]}...' if len(str(self.more)) > 30 else str(self.more)

    more_short.short_description = '更多信息'


# 扩展字段的下拉选项
type_choices = [
    # 存储类型
    ("bool", "布尔型-bool"),
    ("int", "整型-int"),
    ("float", "浮点型-float"),
    ('number', '数字类型-number'),
    ("string", "字符串型-string"),
    ('text', '长文本型-text'),

    # 表单类型
    ('plain', '普通文字-plain'),
    ('input', '输入框-plain'),
    ('password', '密码框-password'),
    ('textarea', '多行文本框-textarea'),
    ('editor', '富文本编辑器-editor'),
    ('switch', '开关切换-switch'),
    ("select", "选择框-select"),
    ("radio", "单选框-radio"),
    ("checkbox", "多选框-checkbox"),
    ('cascader', '级联选择器-cascader'),
    ("color", "色彩选择器-color"),
    ('slot', '插槽-slot'),

    # 文档类型
    ('image', '图片-image'),
    ('audio', '音频-audio'),
    ('video', '视频-video'),
    ('file', '文件-file'),
    ('upload', '上传类型-upload'),

    # 时间类型
    ('time', ' 时间-time'),
    ("datetime", "日期时间-datetime"),
    ('date', '日期-date'),
    ('month', '月份-month'),
    ('year', '年-year'),
]


class ThreadCategory(models.Model):
    """
    2、Thread_Category 主类别表
    类别。类似于版块大类的概念，用于圈定信息内容所属的主要类别
    """
    id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
    parent = models.ForeignKey(to="self", verbose_name='父类别', db_column='parent_id', blank=True, null=True,
                               db_index=True, on_delete=models.DO_NOTHING, db_constraint=False, help_text='')
    platform_code = models.CharField(verbose_name="平台码", max_length=16, db_index=True, blank=True, null=True)
    value = models.CharField(verbose_name='类别标识值', max_length=32, help_text='类别唯一标识值是标识类别的唯一选项', unique=True)
    name = models.CharField(verbose_name='类别名称', max_length=128, blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')
    icon = models.CharField(verbose_name='图标', max_length=255, blank=True, null=True, help_text='')
    config = models.JSONField(verbose_name='前端配置', blank=True, null=True, default=dict, help_text='')
    total = models.IntegerField(verbose_name="总计", blank=True, null=True, help_text='自动计算信息总数（含子类别）')
    need_auth = models.BooleanField(verbose_name="登录可见", blank=True, null=True, help_text='类别是否登录后才能查看')
    sort = models.IntegerField(verbose_name="排序", blank=True, null=True, help_text='默认排序为升序')
    disable = models.BooleanField(verbose_name='禁用', null=True, blank=True, help_text='默认不禁用')

    class Meta:
        db_table = 'thread_category'
        verbose_name_plural = '02. 信息 - 主要类别'
        # ordering = ['platform_code', 'parent_id__id', 'sort']

    def short_description(self):
        if len(str(self.description)) > 30:
            return '{}...'.format(str(self.description)[0:30])
        return str(self.description)

    short_description.short_description = '描述'

    def short_icon(self):
        if len(str(self.icon)) > 30:
            return '{}...'.format(str(self.icon)[0:30])
        return str(self.icon)

    short_icon.short_description = '图标'

    def short_config(self):
        if len(str(self.config)) > 30:
            return '{}...'.format(str(self.config)[0:30])
        return str(self.config)

    short_config.short_description = '前端配置'

    def __str__(self, help_text=''):
        return f"{self.name} ({self.value or ''})"

    # 处理字段出现 前后空格问题
    def clean(self):
        """模型清洗"""
        if self.name:
            self.value = self.value.strip()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ThreadCategory, self).save(*args, **kwargs)


class ThreadClassify(models.Model):
    """
    3、Thread_Classify 分类表
    @brief 分类。具体的分类，可以是按行业、兴趣、学科的分类，是主类别下的子分类。
    @note 考虑到多语言翻译的问题，不需要写接口，由运维在后台添加
    """
    id = models.AutoField(verbose_name='分类ID', primary_key=True)
    category = models.ForeignKey(verbose_name='所属类别', to=ThreadCategory, db_column='category_id', related_name='+',
                                 on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True, help_text='')
    parent = models.ForeignKey(to="self", verbose_name='父分类', db_column='parent_id', blank=True, null=True,
                               help_text='', db_constraint=False, on_delete=models.DO_NOTHING)
    value = models.CharField(verbose_name='分类标识值', max_length=32, unique=True, help_text='')
    name = models.CharField(verbose_name='分类名称', max_length=128, blank=True, null=True, help_text='')
    show = models.ForeignKey(verbose_name='默认展示ID', to='ThreadShow', db_column='show_id', related_name='+',
                             on_delete=models.DO_NOTHING, db_constraint=False, null=True, blank=True, help_text='')
    icon = models.CharField(verbose_name='图标', max_length=255, blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')
    config = models.JSONField(verbose_name='前端配置', blank=True, null=True, default=dict, help_text='')
    sort = models.IntegerField(verbose_name="排序", blank=True, null=True, help_text='默认排序为升序')

    class Meta:
        db_table = 'thread_classify'
        verbose_name_plural = '03. 信息 - 分类'
        # ordering = ['category', 'parent_id__id', 'sort']  # TODO 不能在这里写排序，否则会导致所有查询都进行排序，会影响速度，所有已使用代码都要改掉 sieyoo by 20221105

    def __str__(self, help_text=''):
        return f"{self.name} ({self.value or ''})"


class ThreadShow(models.Model):
    """
    4、Thread_Show 展示类型表
    展示类型。用于对前端界面的显示样式进行分类
    """
    id = models.AutoField(verbose_name='展示类型ID', primary_key=True, help_text='')
    value = models.CharField(verbose_name='展示类型值', max_length=50, help_text='')
    name = models.CharField(verbose_name='展示类型名', max_length=255, blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')
    config = models.JSONField(verbose_name='前端配置', blank=True, null=True, default=dict,
                              help_text='')  # 用于存放前端自定义的界面或样式相关的配置数据

    class Meta:
        db_table = 'thread_show'
        verbose_name_plural = '04. 信息 - 展示类型'

    def __str__(self):
        return f"{self.name} ({self.value or ''})"


field_index_choices = [
    ("field_1", "自定义字段1 (数字)"),
    ("field_2", "自定义字段2 (数字)"),
    ("field_3", "自定义字段3 (数字)"),
    ("field_4", "自定义字段4 (数字)"),
    ("field_5", "自定义字段5 (数字)"),
    ("field_6", "自定义字段6 (数字)"),
    ("field_7", "自定义字段7 (数字)"),
    ("field_8", "自定义字段8 (数字)"),
    ("field_9", "自定义字段9 (数字)"),
    ("field_10", "自定义字段10 (数字)"),
    ("field_11", "自定义字段11 (文本)"),
    ("field_12", "自定义字段12 (文本)"),
    ("field_13", "自定义字段13 (文本)"),
    ("field_14", "自定义字段14 (文本)"),
    ("field_15", "自定义字段15 (文本)"),
    ("field_16", "自定义字段16 (文本)"),
    ("field_17", "自定义字段17 (文本)"),
    ("field_18", "自定义字段18 (文本)"),
    ("field_19", "自定义字段19 (文本)"),
    ("field_20", "自定义字段20 (文本)"),
    ("field_21", "自定义字段20 (长文本)"),
    ("field_22", "自定义字段20 (长文本)"),
]


# 扩展字段表。用于声明扩展字段数据表中的(有序)字段具体对应的什么键名。注意：扩展字段是对分类的扩展，而不是主类别的扩展
class ThreadExtendField(models.Model):
    """ 5、Thread_Extend_Field 扩展字段表 """
    id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
    category = models.ForeignKey(verbose_name='类别ID', to=ThreadCategory, null=False, blank=False,
                                 db_column='category_id', related_name='+', db_constraint=False,
                                 on_delete=models.DO_NOTHING, help_text='')
    field_index = models.CharField(verbose_name='映射的字段索引', max_length=8, help_text='',
                                   choices=field_index_choices)  # 眏射ThreadExtendData表的键名
    field = models.CharField(verbose_name='自定义字段', max_length=32, help_text='')  # 眏射ThreadExtendData表的键名
    value = models.CharField(verbose_name='字段标签', max_length=128, null=True, blank=True, help_text='')
    default = models.CharField(verbose_name='默认值', max_length=255, blank=True, null=True, help_text='')
    type = models.CharField(verbose_name='字段类型', max_length=8, blank=True, null=True, choices=type_choices,
                            help_text='')
    unit = models.CharField(verbose_name='参数单位', max_length=8, blank=True, null=True, help_text='')
    config = models.JSONField(verbose_name='字段配置', blank=True, null=True, default=dict, help_text='')
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')
    enable = models.BooleanField(verbose_name='启用', blank=True, null=True, help_text='默认未启用')

    class Meta:
        db_table = 'thread_extend_field'
        verbose_name_plural = '05. 信息 - 扩展字段'
        unique_together = (("category_id", "field"),)  # 组合唯一，分类+字段
        # ordering = ['-category_id']

    def __str__(self):
        return f"{self.id}"


# 扩展字段数据表。用于扩展一些自定义的版块功能的数据
class ThreadExtendData(models.Model):
    """ 6、Thread_Extend_Data 扩展字段数据表 """
    thread = models.OneToOneField(verbose_name='信息ID', to='Thread', related_name="thread_extend_data",
                                  db_column='thread_id', primary_key=True, on_delete=models.DO_NOTHING, help_text='')
    thread_uuid = JULIDField(verbose_name='UUID', default=JULIDField.get_u12(), unique=True, editable=True,
                      db_index=True, help_text='')
    category = models.ForeignKey(verbose_name='类别ID', to='ThreadCategory', on_delete=models.DO_NOTHING, null=True,
                                 db_column='category_id', blank=True, db_constraint=False, help_text='')
    field_1 = models.DecimalField(verbose_name='自定义字段_1 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_2 = models.DecimalField(verbose_name='自定义字段_2 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_3 = models.DecimalField(verbose_name='自定义字段_3 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_4 = models.DecimalField(verbose_name='自定义字段_4 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_5 = models.DecimalField(verbose_name='自定义字段_5 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_6 = models.DecimalField(verbose_name='自定义字段_6 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_7 = models.DecimalField(verbose_name='自定义字段_7 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_8 = models.DecimalField(verbose_name='自定义字段_8 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_9 = models.DecimalField(verbose_name='自定义字段_9 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_10 = models.DecimalField(verbose_name='自定义字段_10 (数字)', max_digits=32, decimal_places=8, blank=True, null=True)
    field_11 = models.CharField(verbose_name='自定义字段_11 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_12 = models.CharField(verbose_name='自定义字段_12 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_13 = models.CharField(verbose_name='自定义字段_13 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_14 = models.CharField(verbose_name='自定义字段_14 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_15 = models.CharField(verbose_name='自定义字段_15 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_16 = models.CharField(verbose_name='自定义字段_16 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_17 = models.CharField(verbose_name='自定义字段_17 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_18 = models.CharField(verbose_name='自定义字段_18 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_19 = models.CharField(verbose_name='自定义字段_19 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_20 = models.CharField(verbose_name='自定义字段_20 (文本)', max_length=255, blank=True, null=True, help_text='')
    field_21 = models.TextField(verbose_name='自定义字段_20 (长文本)', blank=True, null=True, help_text='')
    field_22 = models.TextField(verbose_name='自定义字段_20 (长文本)', blank=True, null=True, help_text='')

    class Meta:
        db_table = 'thread_extend_data'
        verbose_name_plural = '06. 信息 - 扩展数据'

    def __str__(self):
        return f"{self.thread_id}"

    def short_field_11(self):
        if self.field_11 and len(self.field_11) > 25:
            return f"{self.field_11[0:25]}..."
        return self.field_11

    short_field_11.short_description = '自定义字段11'

    def short_field_12(self):
        if self.field_12 and len(self.field_12) > 25:
            return f"{self.field_12[0:25]}..."
        return self.field_12

    short_field_12.short_description = '自定义字段12'

    def short_field_13(self):
        if self.field_13 and len(self.field_13) > 25:
            return f"{self.field_13[0:25]}..."
        return self.field_13

    short_field_13.short_description = '自定义字段13'

    def short_field_14(self):
        if self.field_14 and len(self.field_14) > 25:
            return f"{self.field_14[0:25]}..."
        return self.field_14

    short_field_14.short_description = '自定义字段14'

    def short_field_15(self):
        if self.field_15 and len(self.field_15) > 25:
            return f"{self.field_15[0:25]}..."
        return self.field_15

    short_field_15.short_description = '自定义字段15'

    def short_field_16(self):
        if self.field_16 and len(self.field_16) > 25:
            return f"{self.field_16[0:25]}..."
        return self.field_16

    short_field_16.short_description = '自定义字段16'

    def short_field_17(self):
        if self.field_17 and len(self.field_17) > 25:
            return f"{self.field_17[0:25]}..."
        return self.field_17

    short_field_17.short_description = '自定义字段17'

    def short_field_18(self):
        if self.field_18 and len(self.field_18) > 25:
            return f"{self.field_18[0:25]}..."
        return self.field_18

    short_field_18.short_description = '自定义字段18'

    def short_field_19(self):
        if self.field_19 and len(self.field_19) > 25:
            return f"{self.field_19[0:25]}..."
        return self.field_19

    short_field_19.short_description = '自定义字段19'

    def short_field_20(self):
        if self.field_20 and len(self.field_20) > 25:
            return f"{self.field_20[0:25]}..."
        return self.field_20

    short_field_20.short_description = '自定义字段20'


# 访问权限类型。
class ThreadAuthType(models.Model):
    class Meta:
        db_table = 'thread_auth_type'
        verbose_name_plural = '07. 信息 - 权限类型'

    id = models.AutoField(verbose_name='ID', primary_key=True)
    value = models.CharField(verbose_name='权限值', max_length=50, help_text='推荐统一为宏命名法（由大写字母和下划线组成）')
    name = models.CharField(verbose_name='权限名', max_length=50)

    def __str__(self):
        return f"{self.value} ({self.name})"


crud_choices = [
    ("C", "新增 (Create)"),
    ("R", "查找 (Read)"),
    ("U", "修改 (Update)"),
    ("D", "删除 (Delete)"),
]


# 访问权限。作者指定允许哪里用户可以访问，例如私有、公开、好友、指定某些人可以访问等。
class ThreadAuthField(models.Model):
    class Meta:
        db_table = 'thread_auth_field'
        verbose_name_plural = '08. 信息 - 权限字段'

    id = models.AutoField(verbose_name='ID', primary_key=True)
    category = models.ForeignKey(verbose_name='类别ID', to=ThreadCategory, null=False, blank=False,
                                 db_column='category_id', related_name='+', db_constraint=False,
                                 on_delete=models.DO_NOTHING, help_text='')
    crud = models.CharField(verbose_name='CRUD', max_length=1, null=True, blank=True, choices=crud_choices,
                            help_text='CRUD（Create, Read, Update, Delete，简称CRUD）')
    auth_level = models.ForeignKey(verbose_name='权限类型', to=ThreadAuthType, null=False, blank=False,
                                   db_column='auth_level', related_name='+', db_constraint=False,
                                   on_delete=models.DO_NOTHING, help_text='')
    allow_fields = models.CharField(verbose_name='允许字段', max_length=1024, null=True, blank=True,
                                    help_text='允许可见的字段，多个字段以英文分号;分隔')
    ban_fields = models.CharField(verbose_name='禁止字段', max_length=1024, null=True, blank=True,
                                  help_text='禁止可见的字段，注意：当允许和禁止字段冲突时，禁止的优先级更高，以分号;分隔')
    is_list = models.BooleanField(verbose_name='是否列表', blank=True, null=True,
                                  help_text='选是过滤列表数据，默认过滤详情数据。注意：列表页禁止显示content, logs, more字段')
    enable = models.BooleanField(verbose_name='启用', blank=True, null=True, help_text='默认未启用')

    def __str__(self):
        return f"{self.category.value}"


# class ThreadTag(models.Model):
#     """
#     7、Thread_Tag 标签类型表
#     标签类型，存放预置标签。用于智能化推送信息，以及关键字检索。未来应设计成根据信息内容自动生成标签。
#     """
#     id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
#     value = models.CharField(verbose_name='标签名', max_length=255, blank=True, null=True, help_text='')
#     user_id = models.IntegerField(verbose_name='用户ID', blank=True, null=True, default=0,
#                                   help_text='如果是私人标签则不为空，如果为0代表公域标签。')
#     thread = models.ManyToManyField(to='Thread', through='ThreadTagMapping', through_fields=('tag_id', 'thread_id'),
#                                     blank=True, help_text="")
#
#     class Meta:
#         db_table = 'thread_tag'
#         verbose_name_plural = '09. 信息 - 标签类型'
#
#     def __str__(self):
#         return f"{self.value}"
#
#
# class ThreadTagMapping(models.Model):
#     """
#     8、Thread_Tag_Mapping 标签映射表
#     标签映射，存放数据。即将标签和信息关联起来 """
#     id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
#     thread = models.ForeignKey(verbose_name='信息ID', to=Thread, related_name="thread", db_column='thread_id',
#                                blank=True, null=True, db_constraint=False, on_delete=models.DO_NOTHING, help_text='')
#     tag = models.ForeignKey(verbose_name='标签ID', to=ThreadTag, db_column='tag_id', related_name='+',
#                             blank=True, null=True, on_delete=models.DO_NOTHING, db_constraint=False, help_text='')
#     # 由于django的外键使用规范，无法一个外键字段关联两个模型，所以使用该字段,关联
#     statistic = models.ForeignKey(verbose_name='统计ID', to='ThreadStatistic', db_column='statistic_id',
#                                   related_name='thread_statistic', blank=True, null=True, on_delete=models.DO_NOTHING,
#                                   db_constraint=False, help_text='统计关联')
#
#     class Meta:
#         db_table = 'thread_tag_mapping'
#         verbose_name_plural = '10. 信息 - 标签映射'
#
#     def __str__(self):
#         return f"{self.id}"


# class ThreadImageAuth(models.Model):
#     """
#     9、Thread_Image_Auth  图片权限表
#     图片权限。作者可以指定上传的图片的访问权限。如公开照片、阅后即焚、已焚毁、红包、红包阅后即焚、红包阅后已焚毁
#     """
#     id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
#     value = models.CharField(verbose_name='值', max_length=255, blank=True, null=True, help_text='')
#
#     class Meta:
#         db_table = 'thread_image_auth'
#         verbose_name_plural = '09. 信息 - 图片权限'


class ThreadStatistic(models.Model):
    """ 10、Thread_Statistic 信息统计表 """
    thread_id = models.OneToOneField(verbose_name='信息ID', to=Thread, primary_key=True, db_column="thread_id",
                                     db_constraint=False, on_delete=models.DO_NOTHING, help_text='')
    flag_classifies = models.CharField(verbose_name='分类标识', max_length=255, null=True, blank=True, help_text='')
    flag_weights = models.CharField(verbose_name='权重标识', max_length=255, null=True, blank=True, help_text='')
    weight = models.FloatField(verbose_name='权重', default=0, db_index=True, help_text='')
    views = models.IntegerField(verbose_name='浏览数', default=0, help_text='')
    plays = models.IntegerField(verbose_name='完阅数', default=0, help_text='')
    comments = models.IntegerField(verbose_name='评论数', default=0, help_text='')
    likes = models.IntegerField(verbose_name='点赞数', default=0, help_text='')
    favorite = models.IntegerField(verbose_name='收藏数', default=0, help_text='')
    shares = models.IntegerField(verbose_name='分享数', default=0, help_text='')

    class Meta:
        db_table = 'thread_statistic'
        verbose_name = '12. 信息 - 信息统计'
        verbose_name_plural = verbose_name

# # 图片信息表。用于存放图片的各种信息，存放图片地址但不存放图。
# class ThreadResource(models.Model):
#     class Meta:
#         db_table = 'thread_resource'
#         verbose_name_plural = '图片表'
#
#     id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
#     name = models.CharField(verbose_name='图片名称', max_length=255, null=True, blank=True, help_text='')
#     url = models.CharField(verbose_name='图片链接', max_length=1024, null=True, blank=True, help_text='')
#     filename = models.CharField(verbose_name='文件名', max_length=255, null=True, blank=True, help_text='')
#     filetype = models.SmallIntegerField(verbose_name='文件类型', null=True, blank=True, help_text='')  # 文件类型0:图片，1:视频，2:文件
#     format = models.CharField(verbose_name='文件格式', max_length=50, help_text='')
#     image_auth_id = models.ForeignKey(verbose_name='图片权限ID', to=ThreadImageAuth, db_column='image_auth_id', related_name='+', on_delete=models.DO_NOTHING, null=True, blank=True, help_text='')
#     price = models.DecimalField(verbose_name='价格', max_digits=32, decimal_places=8, db_index=True, null=True, blank=True, help_text='')
#     snapshot = models.JSONField(verbose_name='快照', blank=True, null=True, help_text='')  # 存放图片的快照数据，如缩略图等。json对象
#     logs = models.JSONField(verbose_name='日志', blank=True, null=True, help_text='')  # 用于存放点击量，点赞量等,数组对象
#     # user_id = models.ForeignKey(verbose_name='用户ID', to=User, db_column='user_id', related_name='+', on_delete=models.DO_NOTHING)
#     user_id = models.BigIntegerField(verbose_name='用户ID', help_text='')
#     thread = models.ManyToManyField(to='Thread', through='ThreadToResource', through_fields=('resource_id', 'thread_id'), blank=True, help_text='')


# # 标签映射，存放数据。即将标签和信息关联起来
# class ThreadToResource(models.Model):
#     class Meta:
#         db_table = 'thread_to_resource'
#         verbose_name_plural = '图文关联表'
#
#     id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
#     thread_id = models.ForeignKey(verbose_name='信息ID', to=Thread, db_column='thread_id', related_name='+', on_delete=models.DO_NOTHING, help_text='')
#     resource_id = models.ForeignKey(verbose_name='图片ID', to=ThreadResource, db_column='resource_id', related_name='+', on_delete=models.DO_NOTHING, help_text='')

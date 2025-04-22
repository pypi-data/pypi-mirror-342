# from django.conf import settings
from django.contrib import admin
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
from .models import Thread, ThreadStatistic
from .models import ThreadExtendData
from .models import ThreadExtendField
from .models import ThreadShow, ThreadClassify, ThreadCategory
from .models import ThreadAuthType, ThreadAuthField
# from .models import ThreadTag, ThreadTagMapping
from .utils.custom_paginator import CustomPaginator


# admin.site.site_header = settings.MAIN_CONFIG.get('site_header')
# admin.site.site_title = settings.MAIN_CONFIG.get('site_title')

# total_count_cache = 0


# @receiver(post_save, sender=Thread)
# @receiver(post_delete, sender=Thread)
# def update_total_count_cache(sender, **kwargs):
#     global total_count_cache
#     # 重新计算总量并更新缓存
#     total_count_cache = Thread.objects.count()

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    paginator = CustomPaginator
    fieldsets = [
        ('主要信息', {'classes': 'collapse', 'fields': (
            'id', 'uuid', ('category', 'classify', 'show'), ('user_id','user_uuid', 'username_query', 'with_user_id'),
            ('group_id', 'thread_no'), ('title', 'subtitle'), 'summary', 'content', 'content_coding', 'keywords',
        )}),
        ('版权信息', {'classes': 'collapse', 'fields': (
            'access_level', 'author', ('region_code', 'ip'),
            # ('has_enroll', 'has_fee', 'has_comment', 'has_location'),
        )}),
        ('媒体信息', {'classes': 'collapse', 'fields': (
            ('cover', 'photos'), ('video', 'files'), 'price', 'is_original', 'link',
        )}),
        ('更多设置', {'classes': 'collapse', 'fields': (
            ('logs', 'more'), ('sort', 'language_code'), 'remark',
            ('create_time', 'update_time', 'publish_time'), 'is_delete',
        )}),
    ]
    list_display = (
        'id', 'uuid', 'thread_no', 'category', 'classify', 'show', 'group_id',
        'user_id', 'user_uuid', 'username_query', 'with_user_id',
        'title_short', 'subtitle_short', 'summary_short', 'content_short', 'keywords',
        'access_level', 'author', 'region_code', 'ip',
        # 'has_enroll', 'has_fee', 'has_comment', 'has_location',
        'cover_short', 'photos_short', 'video_short', 'files_short', 'price', 'is_original',
        'link', 'logs_short', 'more_short', 'sort', 'language_code',
        'remark', 'create_time', 'update_time', 'publish_time', 'is_delete',
    )
    list_filter = ['category', 'classify', 'show', 'group_id', 'access_level', 'region_code']
    list_display_links = ['id', 'uuid', 'title_short']
    search_fields = ('thread_no', 'title', 'subtitle', 'summary', 'region_code')
    raw_id_fields = ['category', 'classify', 'show']
    readonly_fields = ('id', 'uuid', 'update_time', 'username_query')  # 只读
    # ordering = ['-update_time']  # 排序 # 使用 ModelAdmin.ordering 排序可能会导致性能问题，因为在一个大的查询集上排序会很慢。
    list_per_page = 20  # 每页显示10条

    # def get_queryset(self, request):
    #     print('get_queryset request:', request)
    #     # 使用缓存的总量值
    #     qs = super().get_queryset(request)
    #     print('get_queryset qs:', qs)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)

    # def get_changelist(self, request, **kwargs):
    #     print("> ThreadAdmin: get_changelist:", request)
    #     res = super().get_changelist(request, **kwargs)
    #     print("> ThreadAdmin: get_changelist res:", res)
    #     return res

    # # 如果你需要在admin界面上显示总量，可以这样做：
    # def changelist_view(self, request, extra_context=None):
    #     print("> ThreadAdmin: changelist_view:", request, extra_context)
    #     extra_context = extra_context or {}
    #     extra_context['total_count'] = 516  # 使用全局变量
    #     res = super().changelist_view(request, extra_context=extra_context)
    #     print("> ThreadAdmin: changelist_view res:", res)
    #     return res

    # def get_list_display_links(self, request, list_display):
    #     print('get_list_display_links request:', request, list_display)
    #     return self.list_display_links


@admin.register(ThreadCategory)
class ThreadCategoryAdmin(admin.ModelAdmin):
    class ThreadExtendFieldInline(admin.TabularInline):
        model = ThreadExtendField
        fields = ['field_index', 'field', 'value', 'default', 'type', 'unit', 'description', 'enable', ]
        extra = 0

    class ThreadAuthInline(admin.TabularInline):
        model = ThreadAuthField
        extra = 0

    inlines = [ThreadExtendFieldInline, ThreadAuthInline, ]
    fields = (
        'id', 'parent', 'platform_code', 'value', 'name', 'description', 'icon', 'config', 'total',
        'need_auth', 'sort', 'disable',)
    list_display = (
        'id', 'platform_code', 'value', 'name', 'short_icon', 'short_config', 'short_description', 'parent',
        'total', 'need_auth', 'sort', 'disable',)
    list_display_links = ['id', 'value', 'name']
    search_fields = ('id', 'platform_code', 'value', 'name',)
    readonly_fields = ('id', 'total')
    ordering = ['platform_code', 'parent', 'sort']


@admin.register(ThreadClassify)
class ThreadClassifyAdmin(admin.ModelAdmin):
    fields = ('id', ('value', 'name'), ('category', 'show'), ('icon', 'config'), 'parent', 'description', 'sort',)
    list_display = ('id', 'value', 'name', 'category', 'show', 'icon', 'config', 'parent', 'description', 'sort',)
    list_display_links = ('id', 'value', 'name')
    search_fields = ('id', 'value', 'name', 'category', 'show')
    raw_id_fields = ['category', 'show', 'parent']
    readonly_fields = ['id']
    ordering = ['category', 'parent', 'sort']


@admin.register(ThreadShow)
class ThreadShowAdmin(admin.ModelAdmin):
    fields = ('id', 'value', 'name', 'config', 'description')
    list_display = ('id', 'value', 'name', 'config', 'description')
    search_fields = ('id', 'value', 'name', 'config')
    readonly_fields = ('id',)


@admin.register(ThreadExtendField)
class ThreadExtendFieldAdmin(admin.ModelAdmin):
    fields = ('id', 'category', 'field_index', 'field', 'value', 'default', 'type', 'unit', 'config', 'description',
              'enable',)
    list_display = ('id', 'category', 'field_index', 'field', 'value', 'default', 'type', 'unit', 'description',
                    'enable',)
    list_filter = ['category']
    list_display_links = ['id', 'field']
    search_fields = ('category__value', 'field_index', 'type')
    raw_id_fields = ['category']
    readonly_fields = ('id',)
    ordering = ['-category_id']
    list_per_page = 20  # 每页显示20条


@admin.register(ThreadExtendData)
class ThreadExtendDataAdmin(admin.ModelAdmin):
    fields = (
        'thread', 'thread_uuid', 'category',
        ('field_1', 'field_2'), ('field_3', 'field_4'), ('field_5', 'field_6'), ('field_7', 'field_8'),
        ('field_9', 'field_10'),
        ('field_11', 'field_12'), ('field_13', 'field_14'), ('field_15', 'field_16'), ('field_17', 'field_18'),
        ('field_19', 'field_20'),
        ('field_21', 'field_22'))
    list_display = (
        'thread', 'thread_uuid', 'category',
        'field_1', 'field_2', 'field_3', 'field_4', 'field_5',
        'field_6', 'field_7', 'field_8', 'field_9', 'field_10', 'short_field_11',
        'short_field_12', 'short_field_13', 'short_field_14', 'short_field_15', 'short_field_16', 'short_field_17',
        'short_field_18', 'short_field_19', 'short_field_20',)
    search_fields = ('thread__title', 'category__value')
    raw_id_fields = ['thread', 'category', ]
    list_per_page = 20  # 每页显示10条


@admin.register(ThreadAuthType)
class ThreadAuthTypeAdmin(admin.ModelAdmin):
    fields = ('id', 'value', 'name')
    list_display = ('id', 'value', 'name')
    list_display_links = ['id', 'value']
    search_fields = ('value',)
    readonly_fields = ('id',)


@admin.register(ThreadAuthField)
class ThreadAuthFieldAdmin(admin.ModelAdmin):
    fields = ('id', 'category', 'crud', 'auth_level', 'allow_fields', 'ban_fields', 'is_list', 'enable')
    list_display = ('id', 'category', 'crud', 'auth_level', 'allow_fields', 'ban_fields', 'is_list', 'enable')
    list_display_links = ['id', 'auth_level']
    search_fields = ('category',)
    raw_id_fields = ['category']
    readonly_fields = ('id',)


# @admin.register(ThreadTag)
# class ThreadTagAdmin(admin.ModelAdmin):
#     fields = ('id', 'value', 'user_id')
#     search_fields = ('id', 'value', 'user_id')
#     list_display = ('id', 'value')
#     readonly_fields = ('id', 'thread')
#
#
# @admin.register(ThreadTagMapping)
# class ThreadTagMappingAdmin(admin.ModelAdmin):
#     fields = ('thread', 'tag', 'statistic')
#     list_display = ('id', 'thread', 'tag', 'statistic')
#     search_fields = ('id', 'thread', 'tag')
#     raw_id_fields = ['thread', 'tag', 'statistic']


# @admin.register(ThreadImageAuth)
# class ThreadImageAuthAdmin(admin.ModelAdmin):
#     list_display = ('id', 'value')
#     search_fields = ('id', 'value')
#     fields = (
#         'id',
#         'value',
#     )
#     readonly_fields = ('id',)


@admin.register(ThreadStatistic)
class ThreadStatisticAdmin(admin.ModelAdmin):
    fields = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', ('views', 'plays', 'comments'),
        ('likes', 'favorite', 'shares'),)
    list_display = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', 'views', 'plays', 'comments', 'likes', 'favorite',
        'shares',)
    search_fields = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', 'views', 'plays', 'comments', 'likes', 'favorite',
        'shares',)
    raw_id_fields = ['thread_id']

# @admin.register(ThreadResource)
# class ThreadImageAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     search_fields = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     fields = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     readonly_fields = ('id',)


# @admin.register(ThreadAuth)
# class ThreadAuthAdmin(admin.ModelAdmin):
#     list_display = ('id', 'value')
#     search_fields = ('id', 'value')
#     fields = ('id', 'value',)
#     readonly_fields = ('id',)

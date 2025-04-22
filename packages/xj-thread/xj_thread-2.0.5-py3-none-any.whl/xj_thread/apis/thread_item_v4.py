"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块单挑数据删除/修改/详情
"""
import sys
import re
from rest_framework.views import APIView
if 'xj_user' in sys.modules:
    from xj_user.services.user_service import UserService
# if 'xj_enroll' in sys.modules:
#     from xj_enroll.service.enroll_services import EnrollServices
from ..services.thread_item_service_v2 import ThreadItemService
from ..utils.custom_response import util_response
from ..utils.request_params_wrapper import request_params_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper
from ..utils.parse_data import parse_data
from ..utils.x_request_wrapper import x_request_wrapper


class ThreadItemAPI(APIView):
    @request_params_wrapper
    def get(self, *args, request_params, **kwargs):
        """
        信息表详情。获取一条信息，查，改，删
        @param pk 主键。允许传信息ID或UUID
        """
        pk = kwargs.get("pk", None)
        # print("ThreadItemAPI::get:", pk, type(pk))
        if not pk:
            return util_response(msg="缺少主键uuid 或 id。", err=1000)

        tid = pk if str.isdigit(pk) else None
        uuid = pk if not str.isdigit(pk) else None
        data, error_text = ThreadItemService.detail(pk=tid, uuid=uuid)
        if not error_text:
            return util_response(data=data)
        return util_response(err=8206, msg=error_text)

    def post(self, request):
        # 用户令牌验证
        token = request.META.get('HTTP_AUTHORIZATION', None)
        token_serv, error_text = UserService.check_token(token)
        print("ThreadAdd: token_serv:", token_serv)
        if error_text:
            return util_response(err=6045, msg=error_text)
        user_uuid= token_serv.get('user_uuid', None)

        # # 编辑主键验证
        # pk = kwargs.get("pk", None)
        # uuid = kwargs.get("uuid", None)
        # if not pk and not uuid:
        #     return util_response(msg="缺少主键uuid 或 id。", err=1000)

        params = parse_data(request)
        category_value= params.get('category_value', None)
        if not category_value:
            return util_response(err=8201, msg="类别值必填。")
        # # 表单初步验证
        # validator = ThreadAddValidator(params)
        # is_pass, error = validator.validate()
        # if not is_pass:
        #     return util_response(err=4022, msg=error)
        # 插入服务
        data, err_txt = ThreadItemService.add(user_uuid, category_value, params)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    # @user_authentication_force_wrapper
    @x_request_wrapper
    # def put(self, *args, request, request_params, user_info, **kwargs):
    def put(self, request, request_params, *args, **kwargs):
        """信息表编辑"""
        # print("> ThreadItemAPI::put:", "request:", request, ", request_params:", request_params, ", args:", args, ", kwargs:", kwargs)

        pk = kwargs.get("pk", None)
        uuid = kwargs.get("uuid", None)
        if not pk and not uuid:
            return util_response(msg="缺少主键uuid 或 id。", err=1000)

        data, error_text = ThreadItemService.edit(pk=pk, uuid=uuid, params=request_params)
        if error_text:
            return util_response(err=1002, msg=error_text)

        return util_response(data=data)


    @user_authentication_force_wrapper
    def delete(self, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return util_response(msg="非法请求", err=1000)

        data, error_text = ThreadItemService.delete(pk)
        if not error_text:
            return util_response()
        return util_response(err=47767, msg=error_text)

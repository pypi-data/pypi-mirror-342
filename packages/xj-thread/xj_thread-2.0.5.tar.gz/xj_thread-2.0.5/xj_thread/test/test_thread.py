from django.test import TestCase
from ..services.thread_list_service_v2 import ThreadListService
from ..services.thread_category_service import ThreadCategoryService
from ..services.thread_item_service_v2 import ThreadItemService

from datetime import datetime
from ..utils.j_ulid_field import JULIDField
from ulid import ULID


class ThreadTest(TestCase):
    def setUp(self):
        pass

    __right = {
        # "id": 1,
        # "uuid": 1,
        "thread_no": 1,
        "category_value": 'caa',
        "category_name": 1,
        "classify_id": 1,
        "classify_value": 1,
        "classify_name": 1,
        "show_id": 1,
        "show_value": 1,
        "show_name": 1,
        "user_id": 1,
        "user_uuid": 1,
        "with_user_id": 1,
        "group_id": 1,
        "title": 1,
        "subtitle": 1,
        "summary": 1,
        "content": 1,
        "content_coding": 1,
        "author": 1,
        "access_level": 1,
        "region_code": 1,
        "ip": 1,
        "has_enroll": 1,
        "has_fee": 1,
        "has_comment": 1,
        "has_location": 1,
        "cover": 1,
        "photos": 1,
        "video": 1,
        "files": 1,
        "price": 1,
        "is_original": 1,
        "link": 1,
        "logs": 1,
        "more": 1,
        "sort": 1,
        "language_code": 1,
        "remark": 1,
        "create_time": 1,
        "update_time": 1,
        "publish_time": 1,
        "is_delete": 1,
    }
    __category_dict = {
        "platform_code": 2,
        "category_value": 'caa',
        "name": '甲类',
        "need_auth": True,
        "description": 6,
        "sort": 7,
        # "parent_id": 8,
    }

    def test_add(self):
        print('> ulid 1970:', JULIDField.get_u12(datetime(1970,1,3,0,0,0,0)))
        print('> ulid 1990:', JULIDField.get_u12(datetime(1990,1,1,0,0,0,0)))
        print('> ulid 2000:', JULIDField.get_u12(datetime(2000,1,1,0,0,0,0)))
        print('> ulid 2004:', JULIDField.get_u12(datetime(2004,1,1,0,0,0,0)))
        print('> ulid 2005:', JULIDField.get_u12(datetime(2005,1,1,0,0,0,0)))
        print('> ulid 2015:', JULIDField.get_u12(datetime(2015,1,1,0,0,0,0)))
        print('> ulid 2025:', JULIDField.get_u12(datetime(2025,1,1,0,0,0,0)))
        print('> ulid 2035:', JULIDField.get_u12(datetime(2035,1,1,0,0,0,0)))
        print('> ulid 2055:', JULIDField.get_u12(datetime(2055,1,1,0,0,0,0)))
        print('> ulid 2100:', JULIDField.get_u12(datetime(2100,1,1,0,0,0,0)))
        ThreadCategoryService.add(self.__category_dict)
        result, err = ThreadItemService.add(self.__right['user_uuid'], self.__right['category_value'], self.__right)
        print("> ThreadTest: test_add err:", result, err)
        self.assertEqual(err, None)

    def test_detail(self):
        ThreadCategoryService.add(self.__category_dict)
        exist, err = ThreadItemService.add(self.__right['user_uuid'], self.__right['category_value'], self.__right)
        print("> ThreadTest: test_detail exist:", exist)
        result, err = ThreadItemService.detail(exist['id'])
        print("> ThreadTest: test_detail:", result)
        self.assertEqual(err, None)

    # def test_edit(self):
    #     ThreadItemService.add(self.__right)
    #     exist, err = ThreadItemService.detail(self.__right['value'])
    #     print("> ThreadTest: test_edit 1 exist:", exist)
    #     exist['name'] = '乙类'
    #     result, err = ThreadItemService.edit(exist, pk=exist['id'])
    #     print("> ThreadTest: test_edit:", result)
    #     self.assertEqual(err, None)
    #
    # def test_delete(self):
    #     ThreadItemService.add(self.__right)
    #     exist, err = ThreadItemService.detail(self.__right['value'])
    #     print("> ThreadTest: test_delete: exist:", exist)
    #
    #     result, err = ThreadItemService.delete(exist['id'])
    #     print("> ThreadClassifyTest::test_delete:", result)
    #     self.assertEqual(err, None)
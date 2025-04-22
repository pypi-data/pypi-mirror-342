from django.test import TestCase
from ..services.thread_category_service import ThreadCategoryService
from ..services.thread_category_list_service import ThreadCategoryListService


class ThreadCategoryTest(TestCase):
    def setUp(self):
        pass

    __right = {
        "platform_code": 2,
        "category_value": 'caa',
        "name": '甲类',
        "need_auth": True,
        "description": 6,
        "sort": 7,
        # "parent_id": 8,
    }

    def test_add(self):
        result, err = ThreadCategoryService.add(self.__right)
        print("> ThreadCategoryTest: test_add:", result)
        self.assertEqual(err, None)

    def test_get(self):
        ThreadCategoryService.add(self.__right)
        result, err = ThreadCategoryService.detail(self.__right['category_value'])
        print("> ThreadCategoryTest: test_get:", result)
        self.assertEqual(err, None)
        self.assertEqual(result['category_value'], self.__right['category_value'], '获取类别失败')

    def test_edit(self):
        ThreadCategoryService.add(self.__right)
        exist, err = ThreadCategoryService.detail(self.__right['category_value'])
        print("> ThreadCategoryTest: test_edit 1 exist:", exist)
        exist['name'] = '乙类'
        result, err = ThreadCategoryService.edit(self.__right['category_value'], exist)
        print("> ThreadCategoryTest: test_edit:", result)
        self.assertEqual(err, None)

    def test_delete(self):
        ThreadCategoryService.add(self.__right)
        result, err = ThreadCategoryService.delete(self.__right['category_value'])
        print("> ThreadClassifyTest::test_delete:", result)
        self.assertEqual(err, None)

    def test_list(self):
        ThreadCategoryService.add(self.__right)
        result, err = ThreadCategoryListService.list()
        print("> ThreadCategoryTest: test_list:", result)
        self.assertEqual(err, None)
        self.assertIsInstance(result['list'], list, '获取类别列表失败')
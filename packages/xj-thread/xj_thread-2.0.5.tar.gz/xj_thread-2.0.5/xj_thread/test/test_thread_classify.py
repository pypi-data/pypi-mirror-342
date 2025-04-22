from django.test import TestCase
from django.core import serializers

from ..services.thread_classify_service import ThreadClassifyService
from ..services.thread_classify_service import ThreadClassify


class ThreadClassifyTest(TestCase):
    def setUp(self):
        pass

    __right = {
        "value": "cla",
        "name": "甲分",
        "show_id": 1,
        "description": 1,
        "category_id": 1,
        "icon": 1,
        "sort": 1,
        "parent_id": 1,
        "config": {},
    }

    def test_add(self):
        result, err = ThreadClassifyService.add(self.__right)
        print("> ThreadClassifyTest::test_add:", result)
        self.assertEqual(err, None)

    def test_get(self):
        ThreadClassifyService.add(self.__right)
        exist_set = ThreadClassify.objects.first()
        print("> ThreadClassifyTest::test_get: exist_set:", exist_set)

        result, err = ThreadClassifyService.get(exist_set.id)
        print("> ThreadClassifyTest: test_get:", result)
        self.assertEqual(err, None)
        self.assertEqual(result['value'], self.__right['value'], '获取类别失败')

    def test_edit(self):
        ThreadClassifyService.add(self.__right)
        exist_obj = ThreadClassify.objects.values().first()
        print("> ThreadClassifyTest::test_edit exist_obj:", exist_obj)

        new_obj = self.__right
        new_obj['name'] = '乙分'
        result, err = ThreadClassifyService.edit(new_obj, pk=exist_obj['id'])
        print("> ThreadClassifyTest::test_edit:", result)
        self.assertEqual(err, None)

    def test_list(self):
        ThreadClassifyService.add(self.__right)
        result, err = ThreadClassifyService.list()
        print("> ThreadClassifyTest::test_list:", result)
        self.assertEqual(err, None)
        self.assertIsInstance(result['list'], list, '获取类别列表失败')

    def test_delete(self):
        ThreadClassifyService.add(self.__right)
        exist_obj = ThreadClassify.objects.values().first()
        print("> ThreadClassifyTest::test_delete exist_obj:", exist_obj)

        result, err = ThreadClassifyService.delete(exist_obj['id'])
        print("> ThreadClassifyTest::test_delete:", result)
        self.assertEqual(err, None)

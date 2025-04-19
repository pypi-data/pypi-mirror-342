# -*- coding: utf-8 -*-
# @Time    : 2025/4/19 11:54
# @Author  : jayden

import unittest
import time
from redis_http_client import RedisHTTPClient, RedisHTTPError


class TestRedisHTTPClient(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # 初始化客户端
        cls.client = RedisHTTPClient(
            base_url="http://localhost:8081",
            username="jayden",
            password="jayden",
        )

        # 注册测试用户 (实际应用中应该单独处理)
        cls.client.register()

    def test_basic_operations(self):
        # 测试基本键值操作
        self.assertTrue(self.client.set("test_key", "hello_world", ex=10))
        self.assertEqual(self.client.get("test_key"), "hello_world")
        self.assertEqual(self.client.ttl("test_key"), 10)

        # 测试删除
        self.assertEqual(self.client.delete("test_key"), 1)
        self.assertIsNone(self.client.get("test_key"))

    def test_bloom_filter(self):
        # 测试布隆过滤器
        bloom_key = "test_bloom"

        # 创建布隆过滤器
        self.assertTrue(self.client.create_bloom_filter(
            bloom_key,
            capacity=1000,
            error_rate=0.01
        ))

        # 添加元素
        self.assertTrue(self.client.bloom_add(bloom_key, "item1"))
        self.assertEqual(self.client.bloom_add(bloom_key, "item2", "item3"), [1, 1])

        # 检查元素
        self.assertTrue(self.client.bloom_check(bloom_key, "item1"))
        self.assertEqual(self.client.bloom_check(bloom_key, "item2", "item4"), [1, 0])

        # 清理
        self.assertEqual(self.client.delete(bloom_key), 1)

    def test_monitoring(self):
        # 测试监控接口
        memory_info = self.client.get_memory_info()
        self.assertIn("used_memory", memory_info)
        self.assertIn("maxmemory", memory_info)

        slow_queries = self.client.get_slow_queries()
        self.assertIsInstance(slow_queries, list)

    def test_error_handling(self):
        # 测试错误处理
        with self.assertRaises(RedisHTTPError):
            self.client.execute_command("NON_EXISTENT_COMMAND")

        with self.assertRaises(RedisHTTPError):
            self.client.bloom_check("non_existent_bloom", "item1")

    def test_rate_limiting(self):
        # 测试限流 (注意: 这个测试可能会因为限流而失败)
        for _ in range(10):  # 不要设置太大，避免触发限流
            self.client.get_memory_info()
            time.sleep(0.1)


if __name__ == "__main__":
    unittest.main()

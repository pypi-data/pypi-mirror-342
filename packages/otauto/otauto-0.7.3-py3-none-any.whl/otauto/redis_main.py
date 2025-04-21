import redis
from redis import ConnectionPool

from otauto.ini_file_operationv2 import INIFileHandler


class RedisHashManager:
    def __init__(self, host='localhost', port=6379, db=0):
        """初始化 Redis 连接池和客户端"""
        self.ini_handler=INIFileHandler()
        self.ini_dict=self.ini_handler.get_section_items("redis")
        host=self.ini_dict.get("ip",host)
        port=int(self.ini_dict.get("port",port))
        self.pool = ConnectionPool(host=host, port=port, db=db)
        self.redis_client = redis.Redis(connection_pool=self.pool)

    def set_hash(self, key, mapping):
        """设置哈希中的多个字段"""
        self.redis_client.hset(key, mapping=mapping)
        return f"Hash '{key}' set with fields: {mapping}"

    def get_hash(self, key):
        """获取哈希中的所有字段及其值,并解码为字符串"""
        raw_data = self.redis_client.hgetall(key)
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in raw_data.items()}

    def get_field(self, key, field):
        """获取哈希中指定字段的值,并解码为字符串"""
        value = self.redis_client.hget(key, field)
        return value.decode('utf-8') if value else None

    def set_field(self, key, field, value):
        """设置哈希中指定字段的值"""
        self.redis_client.hset(key, field, value)
        return f"Field '{field}' in hash '{key}' set to '{value}'"

    def delete_field(self, key, field):
        """删除哈希中指定字段"""
        self.redis_client.hdel(key, field)
        return f"Field '{field}' deleted from hash '{key}'"

    def batch_get_fields(self, key, fields):
        """批量获取哈希中多个字段的值,并解码为字符串"""
        raw_values = self.redis_client.hmget(key, fields)
        return [value.decode('utf-8') if value else None for value in raw_values]

    def batch_set_fields(self, key, mapping):
        """批量设置哈希中多个字段的值"""
        self.redis_client.hset(key, mapping=mapping)
        return f"Fields in hash '{key}' updated with: {mapping}"

    def delete_hash(self, key):
        """删除整个哈希"""
        self.redis_client.delete(key)
        return f"Hash '{key}' deleted"

    def scan_keys(self, pattern):
        """使用 SCAN 命令查找匹配的键"""
        cursor = 0
        matching_keys = []

        while True:
            cursor, keys = self.redis_client.scan(cursor, match=pattern)
            matching_keys.extend(keys)
            if cursor == 0:
                break

        return [key.decode('utf-8') for key in matching_keys]  # 返回字符串列表


# 示例用法
# if __name__ == "__main__":
#     redis_manager = RedisHashManager()
#
#     # 定义哈希的键和值
#     team_key = "team:1"
#     team_data = {
#         "端口": "vnc_port",
#         "队伍职务": "team_duty",
#         "角色名称": "role_name",
#         "进度器": -1,
#         "交互器": -1,
#         "updated_at": -1,
#     }
#
#     # 设置哈希
#     print(redis_manager.set_hash(team_key, team_data))
#
#     # 获取整个哈希
#     print(redis_manager.get_hash(team_key))
#
#     # 获取指定字段
#     print(redis_manager.get_field(team_key, "端口"))
#
#     # 设置指定字段
#     print(redis_manager.set_field(team_key, "进度器", 1))
#
#     # 批量获取字段
#     print(redis_manager.batch_get_fields(team_key, ["端口", "队伍职务"]))
#
#     # 批量设置字段
#     print(redis_manager.batch_set_fields(team_key, {"交互器": 2, "updated_at": 2023}))
#
#     # 删除指定字段
#     print(redis_manager.delete_field(team_key, "角色名称"))
#
#     # 删除整个哈希
#     print(redis_manager.delete_hash(team_key))

    # # 查找以 'team:1' 开头的所有哈希键
    # keys = redis_manager.scan_keys('team:1:*')
    # print("Matching keys:", keys)
import time
from deepdiff import DeepDiff
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from otauto.ini_file_operationv2 import INIFileHandler # 导入INIFileHandler类
from loguru import logger

"""
功能: mongodb数据库操作
更新日志: 2024-11-14 20:00:57
"""

class MongoDBHandler:
    def __init__(self, url="192.168.110.146", port=27017, database_name="game_data"):
        """
        初始化 MongoDB 连接
        :param url: MongoDB URI
        :param port: MongoDB 端口(默认为27017)
        :param database_name: 数据库名称 , 默认为game_data
        """
        self.ini_handler = INIFileHandler()
        self.ini_dict = self.ini_handler.get_section_items("mongobd")
        url = self.ini_dict.get("ip", url)
        port = int(self.ini_dict.get("port", port))

        # 尝试连接到 MongoDB
        try:
            self.client = MongoClient(url, port)
            # 尝试访问数据库以确认连接成功
            self.db = self.client[database_name]
            # 通过简单的命令检查连接
            self.db.command("ping")  # 发送 ping 命令以确认连接
            logger.success(f"成功连接到 MongoDB 数据库: {database_name} 在 {url}:{port}")
        except Exception as e:
            logger.success(f"连接 MongoDB 数据库失败: {e}")
            self.db = None  # 连接失败时将 db 设置为 None

    def set_database(self, database_name):
        """
        设置当前操作的数据库
        :param database_name: 数据库名称
        :return:
        """
        self.db = self.client[database_name]

    def insert_document(self, collection_name, document):
        """
        插入文档到指定的集合中
        :param collection_name: 集合名称
        :param document: 要插入的文档
        :return: 插入文档的ID
        """
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return result.inserted_id
        except CollectionInvalid as e:
            print(f"Error inserting document: {e}")
            return None

    def find_document_one(self, collection_name, query):
        """
        #示例代码
            db_handler.find_document_one("collection_role", {"职业":"蜀山"})
        查询指定集合中的文档,仅返回符合查询条件的第一个文档
        :param collection_name: 集合名称
        :param query: 查询条件
        :return: 查找到的文档
        """
        try:
            collection = self.db[collection_name]
            document = collection.find_one(query)
            return document
        except CollectionInvalid as e:
            print(f"Error finding document: {e}")
            return None

    def find_document_all(self, collection_name, query):
        """
        #示例代码
            db_handler.find_document_all("collection_role", {"职业":"蜀山"})
        查询指定集合中的所有符合条件的文档,返回文档列表
        :param collection_name: 集合名称
        :param query: 查询条件
        :return: 查找到的文档列表
        """
        try:
            collection = self.db[collection_name]
            documents = collection.find(query)
            return list(documents)
        except Exception as e:  # 修改异常捕获为更通用的 Exception
            print(f"Error finding documents: {e}")
            return []

    def update_document_one(self, collection_name, query, update_values,operator:str='$set'):
        """
        #示例代码
            db_handler.update_document_one("collection_role",{"职业":"蜀山"}, {"职业":"五毒"})
        更新指定集合中的文档,仅更新符合查询条件的第一个文档
        :param collection_name: 集合名称
        :param query: 查询条件
        :param update_values: 更新值
        :param operator: 更新操作符，默认为$set,$push表示追加
        :return: 更新的文档数量
        """
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {operator: update_values},upsert=True)
            return result.modified_count
        except CollectionInvalid as e:
            print(f"Error updating document: {e}")
            return 0

    def update_document_all(self, collection_name, query, update_values,operator:str='$set'):
        """
        #示例代码
            db_handler.update_document_all("collection_role",{"职业":"蜀山"}, {"职业":"五毒"})
        更新指定集合中的文档,更新符合查询条件的所有文档
        :param collection_name: 集合名称
        :param query: 查询条件
        :param update_values: 更新值
        :param operator: 更新操作符，默认为$set,$push表示追加
        :return: 更新的文档数量
        """
        try:
            collection = self.db[collection_name]
            result = collection.update_many(query, {operator: update_values}, upsert=True)
            return result.modified_count
        except CollectionInvalid as e:
            print(f"Error updating documents: {e}")
            return 0

    def delete_document(self, collection_name, query):
        """
        删除指定集合中的文档
        :param collection_name: 集合名称
        :param query: 查询条件
        :return: 删除的文档数量
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count
        except CollectionInvalid as e:
            print(f"Error deleting document: {e}")
            return 0

    def close_connection(self):
        """
        关闭与MongoDB服务器的连接
        :return:
        """
        self.client.close()

    def update_check_recent(self, collection_name: str, query_filter: dict = None, document_name: str = "updated_at",
                            time_window: int = 30) -> bool:
        """
        检查指定集合是否在过去指定时间窗口内有符合条件的文档更新。

        :param collection_name: MongoDB 的集合名称
        :param document_name: 时间戳字段名(默认是 'updated_at')
        :param query_filter: 额外的查询条件(默认 None,表示不加额外条件)
        :param time_window: 时间窗口(默认30秒)
        :return: 如果过去指定时间窗口内有更新返回 True,否则返回 False
        """
        # 检查 collection_name 是否有效
        if not collection_name:
            print("未提供有效的集合名称。")
            return False

        # 检查集合是否存在
        if collection_name not in self.db.list_collection_names():
            print(f"集合 '{collection_name}' 不存在。")
            return False

        # 获取当前时间的 UNIX 时间戳并计算时间窗口前的时间戳
        time_window_ago = time.time() - time_window
        query = {document_name: {"$gte": time_window_ago}}

        # 合并额外的查询条件
        if query_filter:
            query.update(query_filter)

        # 查询文档
        collection = self.db[collection_name]
        has_update = collection.count_documents(query)

        if has_update:
            print("数据库最近有更新!")
            return True
        else:
            print("数据库最近没有更新。")
            return False

    def get_data_diff(self, collection_name, query, new_data):
        """
        获取 MongoDB 文档和新数据之间的差异
        # 判断数据是否需要更新
            diff_dict=self.db_handler.get_data_diff("collection_equipment", {"id": self.db_id},  self.bd_equipment)
            if diff_dict:#如果存在差异
                if 'values_changed' in diff_dict and len(diff_dict['values_changed']) == 1:
                    changed_field = list(diff_dict['values_changed'].keys())[0]
                    if changed_field == "root['updated_at']":#如果更新的字段是updated_at，则表示数据为变化
                        return True
        参数:
        collection_name (str): 集合名称
        query: 要查询的文档的条件
        new_data (dict): 新的数据
        返回值:
        dict: 存在差异时，返回包含差异的字典；没有差异时，返回空字典
        """
        collection = self.db[collection_name]
        # 根据 doc_id 查找现有文档
        existing_doc = collection.find_one(query)
        # 如果没有找到对应的文档，返回 None
        if existing_doc is None:
            return None
        # 使用 DeepDiff 比较现有文档和新的数据
        diff = DeepDiff(existing_doc, new_data, ignore_order=True)
        return diff

    def find_document(self, collection_name, query):
        pass

    def update_document(self, collection_name, query, update_values):
        pass


# 示例用法

# uri = "192.168.110.146"  # 替换为你的MongoDB URI
# port = 27017  # MongoDB端口
# collection_name="game_data" #替换为你的集合名称
#
# try:
#     db_handler = MongoDBHandler()
#
#     # 插入文档
#     document = {'name': 'Alice', 'age': 30}
#     inserted_id = db_handler.insert_document(collection_name, document)
#     if inserted_id:
#         print(f'Inserted document ID: {inserted_id}')
#
#     # 查询文档
#     query = {'name': 'Alice'}
#     found_document = db_handler.find_document(collection_name, query)
#     if found_document:
#         print(f'Found document: {found_document}')
#
#     # 更新文档
#     update_values = {'age': 31}
#     updated_count = db_handler.update_document(collection_name, query, update_values)
#     print(f'Number of documents updated: {updated_count}')
#
#     # # 删除文档
#     # deleted_count = db_handler.delete_document('mycollection', query)
#     # print(f'Number of documents deleted: {deleted_count}')
#
# except (ConnectionFailure, OperationFailure) as e:
#     print(f"Error connecting to MongoDB: {e}")
# finally:
#     # 关闭连接
#     db_handler.close_connection()
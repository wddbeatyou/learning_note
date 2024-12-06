# -*- coding: utf-8 -*-
# @Author: wangdongdong
# @Time: 2024/12/4 16:42
from pymongo import MongoClient


# 注意： 在 MongoDB 中，集合只有在内容插入后才会创建! 就是说，创建集合(数据表)后要再插入一个文档(记录)，集合才会真正创建。
# 注意：数据库创建和集合创建后，需要在集合(数据表)中插入一个文档(记录)，数据库才会真正创建。

# ===========================数据库连接=======================================
# 连接mongdb数据库
# client = MongoClient('localhost', 27017)

client = MongoClient('mongodb://localhost:27017/')
# db = client.mydatabase

# client = MongoClient('mongodb://wdd:930817@localhost:27017/wdd')
db = client['wdd']
# ===========================数据表加载=========================================
# 选择表
collection = db["test"]
# ===========================数据表删除=========================================
# 删除表
collection.drop()
# ===========================数据表插入一条数据===================================
collection = db["test"]
document = {"name": "John", "age": 25, "city": "New York"}
collection.insert_one(document)
# ===========================数据表插入多条数据===================================
documents = [
    {"name": "Anna", "age": 28, "city": "London"},
    {"name": "Mike", "age": 32, "city": "Chicago"}
]
collection.insert_many(documents)
# ===========================数据表查询一条数据====================================
result = collection.find_one({"name": "John"})
# ===========================数据表查询多条数据====================================
# results = collection.find({"age": {"$gt": 25}})
# for result in results:
#     print(result)
# ===========================数据表更新一条数据====================================
collection.update_one({"name": "John"}, {"$set": {"age": 26}})
# results = collection.find({"age": {"$gt": 25}})
# for result in results:
#     print(result)
# ===========================数据表更新多条数据====================================
collection.update_many({"age": {"$gt": 26}}, {"$set": {"city": "San Francisco"}})
# results = collection.find({"age": {"$gt": 25}})
# for result in results:
#     print(result)
# ===========================数据表条件查询数据====================================
# 1 条件查询
"""
常用查询操作符：
    $eq：等于
    $ne：不等于
    $gt：大于
    $gte：大于等于
    $lt：小于
    $lte：小于等于
    $in：在指定数组内
    $nin：不在指定数组内
"""
# results = collection.find({"age": {"$gte": 25}})
# for result in results:
#     print(result)
# 2 逻辑操作符
"""
常用逻辑操作符：
    $and：与
    $or：或
    $not：非
    $nor：非或
"""
# results = collection.find({"$or": [{"age": {"$lt": 25}}, {"city": "San Francisco"}]})
# print(type(results))
# for result in results:
#     print(result)

# 3 正则表达式
# results = collection.find({"name": {"$regex": "^J"}})
# for result in results:
#     print(result)

# 4 字段选择
# results = collection.find({}, {"_id": 0, "name": 1, "age": 1})
# for result in results:
#     print(result)

# 5 排序
# results = collection.find().sort("age", 1)   # 正序：从小到大
# results = collection.find().sort("age", -1)   # 倒序：从大到小
# for result in results:
#     print(result)

# 6 限制和跳过
results = collection.find().skip(2).limit(10)
for result in results:
    print(result)

# ===========================数据表索引=========================================
# 1 创建索引
collection.create_index([("name", 1)])

# 2 列出索引
for index in collection.list_indexes():
    print(index)

# 3 删除索引
collection.drop_index("name_1")

# 4 删除所有索引
collection.drop_indexes()

# ===========================数据表聚合=========================================
"""
常用聚合操作符：
    $match：过滤数据
    $group：分组并进行计算
    $sort：排序
    $limit：限制结果数量
    $skip：跳过指定数量的结果
    $project：改变输出文档的结构
    $unwind：拆分数组字段中的元素
"""
pipeline = [
    {"$match": {"age": {"$gte": 25}}},
    {"$group": {"_id": "$city", "average_age": {"$avg": "$age"}}}
]
results = collection.aggregate(pipeline)
for result in results:
    print(result)

# ===========================数据表其他操作=========================================
# 1 统计集合文档数量
count = collection.count_documents({"age": {"$gte": 25}})
print(count)

# 2 执行命令
result = db.command("serverStatus")
print(result)

# ===========================数据表连接池和超时=========================================
# 1 设置连接池
# client = MongoClient('mongodb://localhost:27017/', maxPoolSize=50)   # 可以设置连接池参数，例如最大连接数

# 2 设置超时
# client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000, socketTimeoutMS=2000)


# ===========================案例=========================================
from pymongo import MongoClient
import datetime
# =======================================================================================================================
# 1.配置数据库连接信息
# 方式一：
# client1 = MongoClient("127.0.0.1", 27017)  # 如果是本地连接host,port参数可以省略
# 方式二：
# client2 = MongoClient("127.0.0.1:27017")
# 方式三：账号和密码
client3 = MongoClient("mongodb://root:root@127.0.0.1:27017/")

# 2.选择数据库
# 方式一：
db = client3["wdd"]
# 方式二：
# collection = client2.wdd   # client.db名

# 3.选择集合-表
# 方式一：
# collection = db["runoob"]
# 方式二：
# collection = db.wdd.runoob   # client.db名.集合名

# 4.判断数据库是否已经存在:list_database_names()
# db_list = client3.list_database_names()
# print(db_list)
# if "wdd" in db_list:
#     print('数据库已经存在！')

# 5.插入集合
# 5.1 插入单个文档：insert_one()
# my_col = db['test']
# dic = {'name': 'dgw', 'age': 26, 'sex': '男'}
# dic = {'_id': '666666', 'name': 'dgw2', 'age': 27, 'sex': '男'}
# data = my_col.insert_one(dic)
# print(data.inserted_id)

# 5.2 插入多个文档：insert_many()
# my_col = db['test_col']
# col_list = [
#     {'name': 'dgw1', 'age': 27, 'sex': '男'},
#     {'name': 'dgw2', 'age': 26, 'sex': '男'},
#     {'name': 'dgw3', 'age': 25, 'sex': '男'},
#     {'name': 'dgw4', 'age': 28, 'sex': '男'}
# ]
# col_list = [
#     {'_id': '1', 'name': 'dgw1', 'age': 27, 'sex': '男'},
#     {'_id': '2', 'name': 'dgw2', 'age': 26, 'sex': '男'},
#     {'_id': '3', 'name': 'dgw3', 'age': 25, 'sex': '男'},
#     {'_id': '4', 'name': 'dgw4', 'age': 28, 'sex': '男'}
# ]
# data = my_col.insert_many(col_list)
# print(data.inserted_ids)

# 6 查询数据
# 6.1 查询一条数据：find_one()
# my_col = db['test_col']
# data = my_col.find_one()
# print(data)

# 6.2 查询集合中的所有数据： find()
# my_col = db['test_col']
# datas = my_col.find()
# for data in datas:
#     print(data)

# 6.3 查询指定字段的数据
# 使用 find() 方法来查询指定字段的数据，将要返回的字段对应值设置为 1。
# 除了 _id，不能在一个对象中同时指定 0 和 1，如果你设置了一个字段为 0，则其他都为 1，反之亦然。
# 注意：除了_id外，同时指定0和1会报错。
# my_col = db['test_col']
# # datas = my_col.find({}, {'_id': 0, 'name': 1, 'age': 1})
# datas = my_col.find({}, {'_id': 1, 'name': 1, 'age': 1})
# for data in datas:
#     print(data)

# 6.4 根据指定条件查询
# my_col = db['test_col']
# query = {'name': 'dgw2'}
# datas = my_col.find(query)
# for data in datas:
#     print(data)

# 6.5 高级查询（$gt、$gte等）
# my_col = db['test_col']
# # query = {'_id': {'$gt': '2'}}
# # query = {'age': {'$gte': 27}}
# query = {'name': {'$gte': 'dgw3'}}
# datas = my_col.find(query)
# for data in datas:
#     print(data)

# 6.6 使用正则表达式$regex
# my_col = db['test_col']
# # query = {'name': {'$regex': '^d'}}
# query = {'name': {'$regex': '3$'}}
# datas = my_col.find(query)
# for data in datas:
#     print(data)

# 6.7 返回指定条数记录limit()
# my_col = db['test_col']
# datas = my_col.find().limit(3)
# for data in datas:
#     print(data)

# 6.8 指定从哪条数据开始skip()
# my_col = db['test_col']
# datas = my_col.find().skip(3)
# for data in datas:
#     print(data)
# print("*" * 100)
# datas2 = my_col.find().skip(3).limit(3)
# for data in datas2:
#     print(data)

# 6.9 排序sort()
# # sort() 方法可以指定升序或降序排序。
# # sort() 方法第一个参数为要排序的字段，第二个字段指定排序规则，1 为升序，-1 为降序，默认为升序。
# my_col = db['test_col']
# document = my_col.find().sort('age', -1)
# for doc in document:
#     print(doc)

# 6.10 时间范围查询
# 在MongoDB中，可以使用$gte和$lte运算符来进行时间范围查询。
# 首先，需要将时间转换为MongoDB支持的日期格式（ISODate），可以使用Python中的datetime模块来进行转换。
# start_time = datetime.datetime(2022, 1, 1)
# end_time = datetime.datetime(2022, 1, 31)
#
# start_time_iso = start_time.isoformat()
# end_time_iso = end_time.isoformat()
# print(start_time_iso)
# print(end_time_iso)
# collection = db['test']
# query = {
#     'timestamp': {
#         '$gte': start_time_iso,
#         '$lte': end_time_iso
#     }
# }
# result = collection.find(query)
# for doc in result:
#     print(doc)

# 7 修改数据
# 7.1 修改一条数据： update_one()或者replace_one()
# 使用 update_one() 方法修改文档中的记录。该方法第一个参数为查询的条件，第二个参数为要修改的字段。
# 如果查找到的匹配数据多于一条，则只会修改第一条。
# update_one()是局部更新替换，只需要替换更新需要修改的字段即可。
# my_col = db['test_col']
# query = {'_id': '1', 'name': 'dgw1'}
# new_value = {'$set': {'age': 21}}
# my_col.update_one(query, new_value)
# datas = my_col.find()
# for data in datas:
#     print(data)

# my_col = db['test_col']
# # replace_one要求是所有数据，少一个key-value则报错
# doument = {'stu_no': 3790567, 'stu_name': '张三', 'address': '山东省青岛市', 'phone_no': '12345678910', 'age': 26}
# my_col.replace_one({'stu_name': '张三'}, doument, upsert=True)
# for data in my_col.find():
#     print(data)

# 7.2 修改多条数据：update_many()
# my_col = db['test_col']
# query = {'name': 'dgw1'}
# new_value = {'$set': {'age': 23}}
# num = my_col.update_many(query, new_value)
# datas = my_col.find()
# for data in datas:
#     print(data)

# 8 删除数据
# 8.1 删除单个文档： delete_one()
# 使用 delete_one() 方法来删除一个文档，该方法第一个参数为查询对象，指定要删除哪些数据。
# 如果查询到多条数据，只会删除查询到的第一条数据。
# my_col = db['test_col']
# query = {'_id': '1', 'name': 'dgw1'}
# my_col.delete_one(query)
# document = my_col.find()
# for doc in document:
#     print(doc)

# 8.2 删除多个文档数据：delete_many()
# 使用 delete_many() 方法来删除多个文档，该方法第一个参数为查询对象，指定要删除哪些数据。
# my_col = db['test_col']
# query = {'name': 'dgw2'}
# num = my_col.delete_many(query)
# document = my_col.find()
# for doc in document:
#     print(doc)

# 8.3 删除集合中的所有文档
# my_col = db['test']
# num = my_col.delete_many({})
# document = my_col.find()
# for doc in document:
#     print(doc)

# 8.4 删除集合：drop()
my_col = db['test']
my_col.drop()






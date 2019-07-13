from django.test import TestCase

# Create your tests here.
# import redis
#
#
# conn_r = redis.Redis(host='127.0.0.1', port=6379)  #连接Redis
# # conn_r.set('key', 'value', ex=10)  #数据写入
# # print(conn_r.get('key'))  #数据读取
#
#
#
# #批量操作
# # conn_r.mset(a='abcd', b='bcde', name='胖胖')
# print(conn_r.mget('a', 'b'))
#
# # conn_r.get('a', '123')
#
# dic = {'a1': 'aa', "b1": 'bb'}
# conn_r.hmset('dic_name', dic)
# print(conn_r.hget('dic_name', 'b1'))

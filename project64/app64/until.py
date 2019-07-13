import pymysql
import json
from django.shortcuts import redirect, render


def conn_mysql():
    conn = pymysql.connect(user='root', db='project',
                           password='123456', host='127.0.0.1', port=3306)
    return conn


def user_exist(user_name, pass_word):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select Password from app64_user where User_name = '%s'" % str(user_name)
    try:
        cursor.execute(sql)
        pass_word_from_mysql = cursor.fetchone()
        conn.close()
        if pass_word_from_mysql[0] == str(pass_word):
            return True
        else:
            return False
    except:
        return False


def register_get_input_user_name_exist(UserName):
    '''
    :param UserName:  输入的用户名
    :return:  数据库若存在该用户 则返回FALSE 若无返回True
    '''
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select count(*) from app64_user where User_name = '%s'" % str(UserName)
    cursor.execute(sql)
    name_count_from_mysql = cursor.fetchone()
    conn.close()
    if int(name_count_from_mysql[0]) == 0:
        return True
    else:
        return False


def register_data_insert_into_mysql(un, pw, img):
    """

    :param un: 输入用户名
    :param pw: 输入密码
    :param img: 输入图片名称
    :return: 用来保存账号信息，无返回
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "insert into app64_user(User_name,Password,Photo,Level,Card,Money )""VALUES ('" + un + "', '" + pw + "', '" + img + "', '" + '0' + "', '" + '10' + "', '" + '0' + "')"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()


def register_author_insert_into_mysql(author):
    """

    :param author:输入作者名
    :return: 用来保存作者名到user表，无返回
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "insert into app64_user(Author)""VALUES ('" + author + "')"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()


def author_exit(name):
    """

    :param name: 输入用户名
    :return: 返回作者名
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql1 = "select Author from app64_user where User_name = '%s'" % name
    cursor.execute(sql1)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    a = data[0][0]
    print(a)
    return a


def author_data_insert_into_mysql(bk, au, img, typle):
    """

    :param bk: 书名
    :param au: 作者名
    :param img: 图片名
    :param typle: 书籍类型
    :return: 无
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql1 = "insert into app64_article(Book_name,Author,Photo,Art_path)""VALUES ('" + bk + "', '" + au + "', '" + img + "', '" + typle + "')"
    cursor.execute(sql1)
    conn.commit()
    conn.close()
    cursor.close()


def author_book_insert_into_mysql(bk, path, number, N_info, Art_info, time):
    """
    保存书本内容
    :param bk: 书名
    :param path: 书籍类型
    :param number: 章节
    :param N_info: 章节内容
    :param Art_info: 文章内容
    :param time: 时间
    :return: 无
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql1 = "insert into app64_book(B_name,Art_path,Number,N_info,Art_info,Art_time)""VALUES ('" + bk + "', '" + path + "', '" + number + "', '" + N_info + "', '" + Art_info + "', '" + time + "')"
    cursor.execute(sql1)
    conn.commit()
    conn.close()
    cursor.close()


def auth(func):
    def inner(reqeust, *args, **kwargs):
        data_cookies = reqeust.COOKIES.get('un_pw')  # 获取cookies值
        if data_cookies is None:
            return redirect('login')
            # return render(reqeust, 'login.html', {'data': {'form': form, 'err': '登录已过期!'}})
        data_cookies_json = json.loads(data_cookies)  # 将json数据转换成dict
        if not user_exist(data_cookies_json.get('un'), data_cookies_json.get('pw')):
            return render(reqeust, 'login.html')
        return func(reqeust, *args, **kwargs)

    return inner


def get_all_data_person():
    """
    获取用户所以信息
    :return: 用户信息列表
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_user"
    cursor.execute(sql)
    all_person_data = cursor.fetchall()
    conn.close()
    all_person_data_list = []
    for data_person in all_person_data:
        dict_by = {
            'name': data_person[0],
            'pw': data_person[1],
            'img': data_person[3]
        }
        all_person_data_list.append(dict_by)
    return all_person_data_list


def index_sort():
    """
    设置书籍类型
    :return: 书籍类型列表
    """
    data_sort = ('玄幻', '都市', '科幻', '奇异', '武侠', '军事', '现实 ', '轻小说', '历史 ', '体育', '游戏')
    data_urban_list = []
    for data_book in data_sort:
        data_urban_list.append(data_book)
    return data_urban_list


def index_find(info):
    """
    文章查询（模糊查询）
    :param info:
    :return: 书籍全部内容
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_article where Book_name like '%{}%'".format(info)
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_urban_list = []
    for data_book in data_urban:
        dict_by = {
            'name': data_book[0],
            # 'B_Info': data_book[1],
            'Author': data_book[2],
            'Catalog': data_book[3],
            'Photo': data_book[4],
            'Card': data_book[5],
            'Price': data_book[6],
            'Art_path': data_book[7]
        }
        data_urban_list.append(dict_by)
    return data_urban_list


def ranklist_dusi():
    """
    按都市月票的数量排名
    :return: 书籍全部信息
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql1 = "select * from app64_article where Art_path = '都市' order by card desc  "
    cursor.execute(sql1)
    data_urban1 = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_list1 = []
    for data_book1 in data_urban1:
        dict_by1 = {
            'name': data_book1[0],
            # 'B_Info': data_book[1],
            'Author': data_book1[2],
            'Catalog': data_book1[3],
            'Photo': data_book1[4],
            'Card': data_book1[5],
            'Price': data_book1[6],
            'Art_path': data_book1[7]
        }
        data_list1.append(dict_by1)
    return data_list1


def ranklist_all():
    """
    总的月票排行榜
    :return:
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_article order by card desc limit 5 "
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_urban_list = []
    for data_book in data_urban:
        dict_by = {
            'name': data_book[0],
            # 'B_Info': data_book[1],
            'Author': data_book[2],
            'Catalog': data_book[3],
            'Photo': data_book[4],
            'Card': data_book[5],
            'Price': data_book[6],
            'Art_path': data_book[7]
        }
        data_urban_list.append(dict_by)
    return data_urban_list


def article_app64_article(name):
    """
    书籍文章内容
    :param name:书名
    :return:
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_article where Book_name = '%s'" % name
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_urban_list = []
    for data_book in data_urban:
        dict_by = {
            'Book_name': data_book[0],
            'B_Info': data_book[1],
            'Author': data_book[2],
            'Catalog': data_book[3],
            'Photo': data_book[4],
            'Card': data_book[5],
            'Price': data_book[6]
        }
        data_urban_list.append(dict_by)
    return data_urban_list


def article_app64_book(name):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_book where B_name = '%s'" % name
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_art_list = []
    for data_book in data_urban:
        dict_by = {
            'B_name': data_book[0],
            'Art_path': data_book[1],
            'Number': data_book[2],
            'N_info': data_book[3],
            'Art_info': data_book[4],
            'Art_ID': data_book[5],
            'Art_time': data_book[6]
        }
        data_art_list.append(dict_by)
    return data_art_list


def article_app64_book1(name):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_book where B_name = '%s'" % name
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_art_list = []
    for data_book in data_urban:
        a = data_book[2]
        b = data_book[3]
        c = data_book[4]
        data_art_list.append(a)
        data_art_list.append(b)
        data_art_list.append(c)
    return data_art_list


def article_app64_word(bn, un, ph, word, b_time):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "insert into app64_word(book_name,user_name,photo,word,b_time)""VALUES ('" + bn + "', '" + un + "', '" + ph + "', '" + word + "', '" + b_time + "')"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()


def user_app64_money(un, name):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "update app64_user set Money=Money + '%s' where User_name = '%s'" % (un, name)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()


def article_app64_word_list(name):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_word where book_name = '%s'" % name
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_art_list = []
    for data_book in data_urban:
        dict_by = {
            'book_name': data_book[0],
            'user_name': data_book[1],
            'photo': data_book[2],
            'word': data_book[3],
            'b_time': data_book[4]
        }
        data_art_list.append(dict_by)
    return data_art_list

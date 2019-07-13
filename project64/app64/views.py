import os
import time

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.http import HttpResponse
from app64.form import LoginForm
from app64.until import *


def control(request):
    return render(request, 'control.html')


@auth
def web_index(request):
    """
    主界面
    :param request:
    :return:
    """
    user_data = request.COOKIES.get('un_pw')
    data_cookies_json = json.loads(user_data)
    user_name = data_cookies_json.get('un')
    book_sort = index_sort()
    ranklist1 = ranklist_all()
    ranklist2 = ranklist_dusi()
    return render(request, 'index.html', {"key4": book_sort, 'user': user_name, 'key7': ranklist1, 'key8': ranklist2})


def find(request):
    if request.method == 'GET':
        return render(request, 'find.html')
    else:
        book_find = request.POST.get('find')
        index_find1 = index_find(book_find)
        if index_find1:
            return render(request, 'find.html', {'find': index_find1})
        else:
            return HttpResponse('没有搜到作品')


def login(request):
    """
    登录界面，使用form表单
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():      # 判断该表单数据是否存在以及合法
            user_name = form.cleaned_data.get('UserName')  # 从form表单内获取对应的数据
            pass_word = form.cleaned_data.get('PassWord')
            if user_exist(user_name, pass_word):
                response = redirect('index')
                dict_cookie = {'un': user_name, 'pw': pass_word}
                response.set_cookie('un_pw', json.dumps(dict_cookie), max_age=60 * 60)
                return response
            else:
                return render(request, 'login.html', {'data': {'form': form, 'err': '用户名或密码错误!'}})
        else:
            return render(request, 'login.html', {'data': {'form': form}})
    else:
        form = LoginForm()  # 注意 需要加上()
        return render(request, 'login.html', {'data': {'form': form}})


def person(request):
    """
    个人中心
    :param request:
    :return:
    """
    user_data = request.COOKIES.get('un_pw')
    data_cookies_json = json.loads(user_data)
    user_name = data_cookies_json.get('un')
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_user where User_name = '%s'" % user_name
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_urban_list = []
    for data_book in data_urban:
        dict_by = {
            'name': data_book[0],
            'level': data_book[2],
            'Photo': data_book[3],
            'author': data_book[4],
            'Card': data_book[6],
            'money': data_book[5]
        }
        data_urban_list.append(dict_by)
    return render(request, 'person.html', {'user': user_name, 'user1': data_urban_list})


def register(request):
    """
    注册页面，创建cookie
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        re_password = request.POST.get('re_pwd')
        author = request.POST.get('author')
        up_file = request.FILES.get('file')
        if username and password and re_password:
            if password == re_password:
                if register_get_input_user_name_exist(username):
                    if str(up_file.name).split('.')[1] in ['png', 'jpg', 'pic']:
                        img_name = username + '.jpg'
                        file_path = os.path.join('static/img', img_name)
                        f = open(file_path, 'wb+')
                        for chunk in up_file.chunks():
                            f.write(chunk)
                        f.close()
                        register_data_insert_into_mysql(username, password, img_name)
                        if author == '是':
                            register_author_insert_into_mysql(username)
                        else:
                            pass
                        response = redirect('/app64/login')
                        dict_cookie = {'un': username, 'pw': password}
                        response.set_cookie('un_pw', json.dumps(dict_cookie), max_age=60 * 60)
                        return response
                    else:
                        return render(request, 'register.html', {'err': '图片上传有误'})
                else:
                    return render(request, 'register.html', {'err': 'sorry 参数有误! 请重新输入!'})
            else:
                return render(request, 'register.html', {'err': '用户已存在'})
        else:
            return render(request, 'register.html', {'err': 'sorry 参数有误! 请重新输入!'})


def sort(request):
    """
    全部作品
    :param request:
    :return:
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_article "
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_urban_list = []
    for data_book in data_urban:
        dict_by = {
            'name': data_book[0],
            'typle': data_book[7]
        }
        data_urban_list.append(dict_by)
    return render(request, 'sort.html', {'key5': data_urban_list})


def money(request):
    if request.method == 'GET':
        return render(request, 'money.html')
    else:
        money = request.POST.get('un')
        user_data = request.COOKIES.get('un_pw')
        data_cookies_json = json.loads(user_data)
        user_name = data_cookies_json.get('un')
        user_app64_money(money, user_name)
    return render(request, 'money.html', {'err': '充值成功'})


def urban(request):
    """
    书籍介绍，书名传参
    :param request:
    :return:
    """
    name2 = request.GET.get('p2')
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_article where Art_path = '%s'" % name2
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_urban_list = []
    for data_book in data_urban:
        dict_by = {
            'name': data_book[0],
            'B_Info': data_book[1],
            'Author': data_book[2],
            'Catalog': data_book[3],
            'Photo': data_book[4],
            'Card': data_book[5],
            'Price': data_book[6],
            'Art_path': data_book[7]
        }
        data_urban_list.append(dict_by)
    return render(request, 'urban.html', {'key': data_urban_list})


def word(request):
    """
    留言板块
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'word.html')
    else:
        book_word = request.POST.get('word')
        book_name = request.POST.get('book_name')
        user_data = request.COOKIES.get('un_pw')
        data_cookies_json = json.loads(user_data)
        user_name = data_cookies_json.get('un')
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        article_app64_word(book_name, user_name, user_name, book_word, now_time)
        data_word_list = article_app64_word_list(book_name)
        return render(request, 'word.html', {'key3': data_word_list})


def article(request):
    """
    书籍内容和章节
    :param request:
    :return:
    """
    name1 = request.GET.get('p1')
    data_urban_list = article_app64_article(name1)
    data_art_list = article_app64_book1(name1)
    data_word_list = article_app64_word_list(name1)
    p = Paginator(data_art_list, 2)
    paginator = Paginator(data_art_list, 3)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
    return render(request, 'article.html', {'key1': data_urban_list, "books": books, 'key3': data_word_list})


def Author(request):
    """
    作家专区
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_data = request.COOKIES.get('un_pw')
        data_cookies_json = json.loads(user_data)
        user_name = data_cookies_json.get('un')
        author_exit_if = author_exit(user_name)
        if author_exit_if != None:
            return render(request, 'Author.html')
        else:
            return HttpResponse('你不是作家')
    else:
        bookname = request.POST.get('bookname')
        typle = request.POST.get('Art_path')
        Number = request.POST.get('Number')
        N_info = request.POST.get('N_info')
        Art_info = request.POST.get('Art_info')
        article_file = request.FILES.get('file')
        if article_file != None:
            if str(article_file.name).split('.')[1] in ['png', 'jpg', 'pic']:
                img_name = bookname + '.jpg'
                file_path = os.path.join('static/img', img_name)
                f = open(file_path, 'wb+')
                for chunk in article_file.chunks():
                    f.write(chunk)
                f.close()
            else:
                return render(request, 'Author.html', {'err': '图片上传有误'})
        else:
            pass
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        author_book_insert_into_mysql(bookname, typle, Number, N_info, Art_info, now_time)
        response = redirect('/app64/Author')
        return response


def ranklist(request):
    """
    用户等级
    :param request:
    :return:
    """
    data_urban_list = ranklist_all()
    data_list1 = ranklist_dusi()
    return render(request, 'ranklist.html', {'key7': data_urban_list, 'key8': data_list1})


def addbook(request):
    """
    添加书籍到书架
    :param request:
    :return:
    """
    user_data = request.COOKIES.get('un_pw')
    data_cookies_json = json.loads(user_data)
    user_name = data_cookies_json.get('un')
    name = request.GET.get('t1')
    if name:
        conn = conn_mysql()
        cursor = conn.cursor()
        sql = "insert into app64_favorite(Use_name,Book_name)""VALUES ('" + user_name + "','" + name + "') "
        cursor.execute(sql)
        conn.commit()
        conn.close()
        cursor.close()
        return HttpResponse('添加成功')
    else:
        return HttpResponse('添加失败')


def my_addbook(request):
    """
    我的收藏
    :param request:
    :return:
    """
    if request.method == 'POST':
        return render(request, 'addbook.html')
    else:
        user_data = request.COOKIES.get('un_pw')
        data_cookies_json = json.loads(user_data)
        user_name = data_cookies_json.get('un')
        conn = conn_mysql()
        cursor = conn.cursor()
        sql = "select distinct Book_name from app64_favorite where Use_name = '%s'" % user_name
        cursor.execute(sql)
        data_urban = cursor.fetchall()
        conn.commit()
        conn.close()
        cursor.close()
        data_list = []
        for data_book in data_urban:
            dict_by = {
                'book_name': data_book[0]
            }
            data_list.append(dict_by)
        return render(request, 'addbook.html', {'key1': data_list})


def delete_my_addbook(request):
    name = request.GET.get('q1')
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "delete from app64_favorite where Book_name = '%s'" % name
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()
    return HttpResponse('删除成功')


def vote(request):
    """
    月票
    :param request:
    :return:
    """
    name = request.GET.get('t2')
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "update app64_article set Card=Card + '%s' where Book_name = '%s'" % (1, name)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()
    if name:
        return HttpResponse('投票成功')
    else:
        return HttpResponse('投票失败')


def reward(request):
    """
    打赏
    :param request:
    :return:
    """
    name = request.GET.get('t3')
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "update app64_article set Price=Price + '%s' where Book_name = '%s'" % (1, name)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()
    if name:
        return HttpResponse('打赏成功')
    else:
        return HttpResponse('打赏失败')


def make_author(request):
    """
    管理界面
    :param request:
    :return:
    """
    user_data = request.COOKIES.get('un_pw')
    data_cookies_json = json.loads(user_data)
    user_name = data_cookies_json.get('un')
    conn = conn_mysql()
    cursor = conn.cursor()
    sql1 = "select User_name from app64_user where User_name = '%s'" % user_name
    cursor.execute(sql1)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    a = data[0][0]
    if a == 'root':
        return render(request, 'make_author.html')
    else:
        return HttpResponse('你不是超级用户')


def catalog(request):
    """
    章节目录
    :param request:
    :return:
    """
    name = request.GET.get('t4')
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select * from app64_book where B_name = '%s'" % name
    cursor.execute(sql)
    data_urban = cursor.fetchall()
    conn.commit()
    conn.close()
    cursor.close()
    data_art_list9 = []
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
        data_art_list9.append(dict_by)
    return render(request, 'catalog.html', {"key2": data_art_list9})


def showBlogs(request):
    """
    文章分页
    :param request:
    :return:
    """
    name = '我的电影时代'
    data_art_list = article_app64_book1(name)
    paginator = Paginator(data_art_list, 3)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
    return render(request, 'loge.html', {'books': books})

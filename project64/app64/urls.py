from django.conf.urls import url

from app64 import views

urlpatterns = [
    url(r'^control/', views.control, name='control'),
    url(r'^index/', views.web_index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^person/', views.person, name='person'),
    url(r'^register/', views.register, name='register'),
    url(r'^sort/', views.sort, name='sort'),
    url(r'^money/', views.money, name='money'),
    url(r'^urban/', views.urban, name='urban'),
    url(r'^article/', views.article, name='article'),
    url(r'^Author/', views.Author, name='Author'),
    url(r'^find/', views.find, name='find'),
    url(r'^ranklist/', views.ranklist, name='ranklist'),
    url(r'^addbook/', views.addbook, name='addbook'),
    url(r'^my_addbook/', views.my_addbook, name='my_addbook'),
    url(r'^vote/', views.vote, name='vote'),
    url(r'^reward/', views.reward, name='reward'),
    url(r'^make_author/', views.make_author, name='make_author'),
    url(r'^catalog/', views.catalog, name='catalog'),
    url(r'^word/', views.word, name='word'),
    url(r'^delete_my_addbook/', views.delete_my_addbook, name='delete_my_addbook'),
    url(r'^loge/', views.showBlogs, name='loge'),
]

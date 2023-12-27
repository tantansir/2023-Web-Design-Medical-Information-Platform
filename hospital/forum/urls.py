from django.urls import path, include
from forum import views

app_name = 'forum'
urlpatterns = [
    path('', views.homepage),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.registerpage),
    path('user/', views.userpage),
    path('user/blog', views.usermyblogpage, name='my_blog'),
    path('user/collection', views.usermycollectionpage),
    path('user/modify', views.usermodifypage),
    path('info/', views.infopage),
    path('hospital_info/<int:hospital_id>/', views.hospitalinfo, name='hospital_info'),
    path('recommend/', views.recommendpage),
    path('blog/hot/<int:pg>', views.bloghomepage, name='hot'),  # 论坛主页 pg为页数
    path('blog/<int:pk>', views.blogindexpage, name='blog_page'),  # 帖子详情 pk为索引
    path('blog/create', views.blogcreatepage, name='blog_create'),  # 帖子创建
    path('blog/<int:pk>/delete', views.blogdelete, name='blog_delete'), # 帖子删除
    path('blog/<int:pk>/comment', views.commentdelete, name='comment_delete'),  # 评论删除
    path('blog/<int:pk>/modify', views.blogmodifypage, name='blog_modify'),  # 帖子修改 pk为索引
]

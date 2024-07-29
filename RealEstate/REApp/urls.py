from django.urls import path
from REApp import views

urlpatterns = [

    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('registration/', views.registration, name="registration"),
    path('save_registration/', views.save_registration, name="save_registration"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('add_property/', views.add_property, name="add_property"),
    path('save_property/', views.save_property, name="save_property"),
    path('property_list/', views.property_list, name="property_list"),
    path('my_post/', views.my_post, name="my_post"),
    path('view_post/<int:postId>/', views.view_post, name="view_post"),
    path('delete_post/<int:postId>/', views.delete_post, name="delete_post"),
    path('edit_post/<int:postId>/', views.edit_post, name="edit_post"),
    path('update_post/<int:postId>/', views.update_post, name="update_post"),
    path('search/',views.search,name='search'),
    path('fo/',views.Feed.as_view(),name="feedback")

]

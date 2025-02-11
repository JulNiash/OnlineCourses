from django.urls import path
from . import views

urlpatterns = [

    #Course views
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('create/', views.create_course, name='course_create'),
    path('<int:course_id>/update/', views.update_course, name='course_update'),
    path('<int:course_id>/delete/', views.delete_course, name='course_delete'),


    # CoursePart views
    path('<int:course_id>/parts/', views.course_part_list, name='course_part_list'),
    path('<int:course_id>/parts/<int:part_id>/', views.course_part_detail, name='course_part_detail'),
    path('<int:course_id>/parts/createpart/', views.create_course_part, name='course_part_create'),
    path('<int:course_id>/parts/<int:part_id>/updatepart/', views.update_course_part, name='course_part_update'),
    path('<int:course_id>/parts/<int:part_id>/deletepart/', views.delete_course_part, name='course_part_delete'),


    # CourseTopic views
    path('<int:course_id>/parts/<int:part_id>/topics', views.course_topic_list, name='course_topic_list'),
    path('<int:course_id>/parts/<int:part_id>/topics/<int:topic_id>/', views.course_topic_detail, name='course_topic_detail'),
    path('<int:course_id>/parts/<int:part_id>/topics/createtopic/', views.course_topic_create, name='course_topic_create'),
    path('<int:course_id>/parts/<int:part_id>/topics/<int:topic_id>/updatetopic/', views.course_topic_update, name='course_topic_update'),
    path('<int:course_id>/parts/<int:part_id>/topics/<int:topic_id>/deletetopic/', views.course_topic_delete, name='course_topic_delete'),


    #topic documents list
    path('document_list/', views.document_list, name='document_list'),
    path('update_document/<int:document_id>', views.update_document, name='update_document'),
    path('delete_document/<int:document_id>', views.delete_document, name='delete_document'),
]


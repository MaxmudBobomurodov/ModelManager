from django.urls import path
from page import views


app_name = 'page'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('<int:id>/edit/', views.edit_book , name='edit_book'),
    path('<int:id>/delete', views.delete_book, name='delete_book'),
]
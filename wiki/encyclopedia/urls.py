from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search_page, name="search_page"),
    path('entry/<str:name>/', views.entry_page, name='entry_page'),
    path('new/', views.new_page, name="new_page"),
    path('entry/<str:name>/edit/', views.edit_page, name='edit_page'),
    path('random/', views.random_page, name="random_page"),
]

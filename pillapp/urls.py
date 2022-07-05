from pillapp import views
from django.urls import path

urlpatterns = [
    path('', views.main, name='main'),
    path('choice/', views.choice, name='choice'),
    path('ocr/', views.ocr, name='ocr'),
    path('mypage/', views.mypage, name='mypage'),
    path('ocr_start/', views.ocr_start, name='ocr_start'),
]

from pillapp import views
from django.urls import path

urlpatterns = [
    path('', views.main, name='main'),
    path('choice/', views.choice, name='choice'),
    path('ocr/<int:pk>/', views.ocr, name='ocr'),
    path('mypage/', views.mypage, name='mypage'),
    path('ocr_start/', views.ocr_start, name='ocr_start'),
    path('registMedicine/', views.registMedicine, name='registMedicine'),
    path('prescription_view/<int:pk>/', views.prescription_view, name='prescription_view'),
    path('medicine_detail/', views.medicine_detail, name='medicine_detail'),
]

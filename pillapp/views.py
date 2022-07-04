from django.shortcuts import render
import requests

def main(request):
    return render(request, 'index.html')

def choice(request):
    return render(request, 'choice.html')

def ocr(request):
    return render(request, 'ocr.html')

def mypage(request):
    return render(request, 'mypage.html')
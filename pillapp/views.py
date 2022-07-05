from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
import json

def main(request):
    return render(request, 'index.html')

def choice(request):
    return render(request, 'choice.html')

def ocr(request):
    return render(request, 'ocr.html')

def mypage(request):
    return render(request, 'mypage.html')

def ocr_start(request):
    context = {}

    # =============== 처방전 및 알약 분석 =================
    items_name = ['종근당염산에페드린정', '타이레놀정500밀리그람(아세트아미노펜)']
    url = 'http://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService1/getMdcinPrductItem'
    api_key = f"NmIs7ngFqUyBQNtecDEtowyuctJEgVvLlRqU4ki/rukB+uBNnRNn3w+CqhYPd6HiH28HI9hyih5KppfWIC/N3w==";
    # http://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService1/getMdcinPrductItem?serviceKey=NmIs7ngFqUyBQNtecDEtowyuctJEgVvLlRqU4ki%2FrukB%2BuBNnRNn3w%2BCqhYPd6HiH28HI9hyih5KppfWIC%2FN3w%3D%3D&item_name=종근당염산에페드린정

    for item_name in items_name:
        params ={'serviceKey' : api_key, 'item_name' : item_name}

        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, "lxml-xml")

        items = soup.find_all("item")

        items = [
            {
                "약품명": item.find('ITEM_NAME').text.strip(),
                "약품 회사": item.find('ENTP_NAME').text.strip(),
                "효능효과": read_info(item.find('EE_DOC_DATA').find_all('ARTICLE'), 'title'),
                "용법용량": read_info(item.find('UD_DOC_DATA').find('ARTICLE').find_all('PARAGRAPH'), 'text'),
                "사용상주의사항": read_info(item.find('NB_DOC_DATA').find_all('ARTICLE'), 'warning'),
            }
            for item in items
        ]
        context[item_name] = items
    return HttpResponse(json.dumps(context), content_type="application/json")


def read_info(item, tag):
    # print(item)
    result = []
    if tag == 'title':
        for i in item:
            result.append(i[tag])
    elif tag == 'text':
        for i in item:
            result.append(i.text.strip())
    elif tag == 'warning':
        info_str = []
        for i in item:
            info_str.append(i['title'])
            texts = i.find_all('PARAGRAPH')
            for t in texts:
                info_str.append(t.text.strip())
                last_str = '\n'.join(info_str)
        result.append(last_str)
    return result
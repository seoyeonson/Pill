from django.shortcuts import redirect, render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
import json
from VisionAPI.visionAPI import visionAPI as VA
from pillapp.models import Prescription, User, medicine
from django.views.decorators.csrf import csrf_exempt
import os
from pill_project import settings
import base64

def main(request):
    return render(request, 'index.html')

def choice(request):
    return render(request, 'choice.html')

def ocr(request, pk):
    etc = True
    if pk == 1:
        title = '처방전 분석하기'
        content = '처방전이 잘보이도록 캡쳐해주세요.'
    elif pk == 2:
        title = '알약 분석하기'
        content = '알약의 문자가 보이도록 캡쳐해주세요.'
    elif pk == 3:
        getMedicineInfo()
        title = ''
        content = ''
        etc = False
        

    context = {
        'title' : title,
        'content' : content,
        'etc' : etc,
    }

    return render(request, 'ocr.html', context)

def mypage(request):
    prescriptions = Prescription.objects.filter(user_id=1)
    medicines = medicine.objects.all()

    context = {
        'prescriptions' : prescriptions,
        'medicines' : medicines
    }
    return render(request, 'mypage.html', context)

@csrf_exempt
def registMedicine(request):
    p_id = request.POST.get('p_id')
    names = request.POST.get('names')
    names = names.split(',')

    p_id = Prescription.objects.get(p_id=p_id)

    try:
        for name in names:
            medicine.objects.create(
                p_id = p_id,
                m_name = name
            )
    except Exception as e:
        print(e);

    return redirect('/mypage/')

@csrf_exempt
def ocr_start(request):
    print("들어옴")
    img_data = request.POST.__getitem__('data')
    basepath = str(os.path.join(settings.MEDIA_ROOT, 'Uploaded_files/'))

    print("1")
    try:
        p_last = Prescription.objects.all().order_by('-p_id')[0]
        file_name = str(p_last.p_id + 1)
    except Exception as e:
        file_name = "1"

    print("2")
    img_path = 'image'+ file_name +'.jpg'
    

    # img_data = base64.b64decode(img_data)
    # with open(basepath + img_path, 'wb') as f:
    #     f.write(img_data)

    # print("이미지저장")
    # Prescription.objects.create(
    #     p_imgpath = basepath+img_path,
    #     user_id = User.objects.get(pk=1), ## 임의로 첫번째 유저로 저장
    # )

    context = {}

    print("분석")
    va = VA(img_data)
    try:
        items_name = [i[2] for i in va.pills]
        items_name = list(set(items_name))
        print("분석된 약 이름")
        for item in items_name:
            print(item)
    except Exception as ex:
        context['message'] = '조회할 약품이 없습니다.'
        return HttpResponse(json.dumps(context), content_type="application/json")


    # 약 리스트 저장시 필요한 p_id (방금 저장한 처방전 이미지)
    p_last = Prescription.objects.all().order_by('-p_id')[0].p_id
    print(p_last)
    context['p_id'] = str(p_last)
    
    # =============== 처방전 및 알약 분석 =================
    getMedicine, names = getMedicineInfo(items_name)

    # 제대로 검색된 약 목록만 이미지에 바운딩
    search_list = list(getMedicine.keys())
    va.out_img(search_list)

    va.img_out.save(basepath + img_path)
    context['img_path'] = img_path

    Prescription.objects.create(
        p_imgpath = basepath+img_path,
        user_id = User.objects.get(pk=1), ## 임의로 첫번째 유저로 저장
    )


    context['names'] = names
    context.update(getMedicine)

    return HttpResponse(json.dumps(context), content_type="application/json")


# xml파일에서 가져오려는 정보의 형태에 따라 바뀌는 함수
def read_info(item, tag):
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
                last_str = '<br>'.join(info_str)

        result.append(last_str)
    return result

# 의약품 정보 가져오기.
def getMedicineInfo(items_name):
    context = {}
    names = []
    # http://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService1/getMdcinPrductItem?serviceKey=NmIs7ngFqUyBQNtecDEtowyuctJEgVvLlRqU4ki%2FrukB%2BuBNnRNn3w%2BCqhYPd6HiH28HI9hyih5KppfWIC%2FN3w%3D%3D&item_name=종근당염산에페드린정
    
    # 공공데이터포털 알약 정보
    url = 'http://apis.data.go.kr/1471057/MdcinPrductPrmisnInfoService1/getMdcinPrductItem'
    api_key = f"NmIs7ngFqUyBQNtecDEtowyuctJEgVvLlRqU4ki/rukB+uBNnRNn3w+CqhYPd6HiH28HI9hyih5KppfWIC/N3w==";

    # 인식된 알약명만큼 정보 가져오기.
    cnt = 0
    for item_name in items_name:
        if len(item_name) < 2:
            continue
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
        if items:
            context[item_name] = items
            # 약 저장시 필요한 분석된 약품명들을 함께 넘김
            names.append(items[0]['약품명'])
            cnt += 1
    if cnt == 0:
        context['message'] = '조회된 약품이 없습니다.'
        context['img_path'] = ''
    return context, names
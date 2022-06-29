from django.shortcuts import render

def main(request):
    return render(request, 'index.html')

def choice(request):
    return render(request, 'choice.html')

def ocr(request, pk):
    if pk==1:
        btn_opt = 1
    elif pk==2:
        btn_opt = 2
    elif pk==3:
        btn_opt = 3

    context = {
        'btn_opt' : btn_opt,
    }
    return render(request, 'ocr.html', context)

def mypage(request):
    return render(request, 'mypage.html')
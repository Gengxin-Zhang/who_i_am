#-*- coding:utf-8 -*-
from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
import base64
# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request,'index.html',{})

@csrf_exempt
def makeit(request):
    if request.method == "GET":
        text_one = request.GET.get('whoiam',u"我们是谁！")
        text_two = request.GET.get('name',u"甲方！")
        text_three = request.GET.get('whatwewant',u'我们要什么！')
        text_four = request.GET.get('idontknow',u'不知道！')
        text_five = request.GET.get('when',u'什么时候要！')
        text_six = request.GET.get('now',u'现在！')
        if text_one.strip() == "":
            text_one = u"我们是谁！"
        if text_two.strip() == "":
            text_two = u"甲方！"
        if text_three.strip() == "":
            text_three = u'我们要什么！'
        if text_four.strip() == "":
            text_four = u'不知道！'
        if text_five.strip() == "":
            text_five = u'什么时候要！'
        if text_six.strip() == "":
            text_six = u'现在！'
        one  = 30
        two  = 330
        three= 620
        base = Image.open("base.png")
        font = ImageFont.truetype('font.ttf', 40)
        d = ImageDraw.Draw(base)
        d.text((100-len(text_one)*10, one), text_one, font=font, fill=(0,0,0))
        d.text((400-len(text_two)*10, one),text_two, font=font, fill=(0,0,0))
        d.text((100-len(text_three)*10, two),text_three, font=font, fill=(0,0,0))
        d.text((400-len(text_four)*10, two),text_four, font=font, fill=(0,0,0))
        d.text((100-len(text_five)*10, three),text_five, font=font, fill=(0,0,0))
        d.text((400-len(text_six)*10, three),text_six, font=font, fill=(0,0,0))
        buf = BytesIO()
        base.save(buf,format="png")
        image_stream = buf.getvalue()
        response = HttpResponse(base64.b64encode(image_stream))
        return response

def about(request):
    return render(request, "about.html", {})
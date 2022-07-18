from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from users.models import User
from django.shortcuts import redirect
from django.urls import reverse
import re


def index(request):
    return render(request, 'users/index/index.html')

def login(request):
    return render(request, 'users/index/login.html')

def dologin(request):
    try:
        if request.POST['code'] != request.session['verifycode']:
            context = {"info":"Wrong Verification Code！"}
            return render(request, "users/index/login.html", context)
        user = User.objects.get(username=request.POST['username'])
        if user.status == 1:
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['pass'] + user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                request.session['adminuser'] = user.toDict()
                return redirect(reverse("users_index"))
            else:
                context = {"info":"Wrong Password！"}

        else:
            context = {"info":"Invalid User！"}
    except Exception as err:
        print(err)
        context = {"info":"Account Not Exists!"}
    return render(request, "users/index/login.html", context)

def logout(request):
    del request.session['adminuser']
    return redirect(reverse("users_login"))

def verify(request):
    import random
    from PIL import Image, ImageDraw, ImageFont
    bgcolor = (242,164,247)
    width = 100
    height = 25
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verifycode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')
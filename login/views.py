from captcha.models import CaptchaStore
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import models
# Create your views here.
from django.urls import reverse
from .forms import *
from hashlib import sha256
import datetime
from django.conf import settings
from django.utils import timezone
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
# import pytz

# utc = pytz.utc


def ajax_val(request):
    if request.is_ajax():
        response = request.GET.get('response', '')
        key = request.GET.get('hashkey', '')
        cs = CaptchaStore.objects.filter(response=response, hashkey=key)
        if cs:
            json_data = {'status': 1}
        else:
            json_data = {'status': 0}
        return JsonResponse(json_data)
    else:
        json_data = {'status':0}
        return JsonResponse(json_data)


def hash_code(string, salt='python'):
    h = sha256(string.encode()+salt.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives


    subject = "来自www.wangqiang.com的注册确认邮件"
    text_content = "感谢注册www.wangqiang.com，如果你看到"
    "这个信息，说明你的邮箱服务器不提供HTML连接功能，请联系管理员"
    html_content = '''
        <p>感谢注册<a href="http://{}/mysite/confirm/?code={}" target="_blank">www.wangqiang.com</a></p>
        <p>请点击链接完成注册确认</p><p>此连接有效期为{}天</p>
    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def index(request):
    pass
    return render(request, 'login/index.html')


# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username', "").strip()
#         password = request.POST.get('password', "").strip()
#         message = "所有字段都必须填写且不能为空格！"
#         if username and password:
#             print(username, password)
#             try:
#                 user = models.User.objects.get(name=username)
#                 if user.password == password:
#                     return redirect(reverse('login:index'))
#             except:
#                 message = "账号或密码错误！"
#         return render(request, 'login/login.html', {'message': message})
#     return render(request, 'login/login.html')

def login(request):
    hash_key = CaptchaStore.generate_key()
    image_url = captcha_image_url(hash_key)
    if request.session.get('is_login', ''):
        return redirect(reverse('login:index'))
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写内容"
        print(login_form.is_valid())
        # 判断登录信息是否合法
        if login_form.is_valid():
            # 获取form对象的表单信息
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirm:
                    message = '该账号还邮箱验证未确认，请确认后再登录'
                    return render(request, 'login/login.html', locals())
                # 判断用户密码是否正确
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect(reverse('login:index'))
                else:
                    message = "用户名或密码错误"
            # 不正确应该返回模糊回复
            except:
                message = "用户名或密码错误"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    hash_key = CaptchaStore.generate_key()
    image_url = captcha_image_url(hash_key)
    if request.session.get('is_login', ''):
        return redirect(reverse('login:index'))
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = '请检查填写内容是否齐全'
        # 判断表单内容是否合法
        if register_form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            name = register_form.cleaned_data['name']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            same_user_name = models.User.objects.filter(name=name)
            same_user_email = models.User.objects.filter(email=email)
            if same_user_name:
                message = '用户名已存在'
                return render(request, 'login/register.html', locals())
            if same_user_email:
                message = "该邮箱已注册"
                return render(request, 'login/register.html', locals())
            if password1 != password2:
                message = "两次输入密码不同"
                return render(request, 'login/register.html', locals())
            user = models.User.objects.create(
                name=name,
                password=hash_code(password1),
                email=email,
                sex=sex,
            )
            code = make_confirm_string(user)
            send_email(email, code)

            message = "请前往注册邮箱，进行邮件确认！"
            return render(request, 'login/confirm.html', locals())
        return render(request, 'login/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', ''):
        return redirect(reverse('login:index'))
    request.session.flush()
    return redirect(reverse('login:index'))


def user_confirm(request):
    code = request.GET.get('code', '')
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = "无效的确认请求"
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    # now = datetime.datetime.now(tz=utc)
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期!请重新注册'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirm = True
        confirm.user.save()
        confirm.delete()
        message = "感谢确认，请使用账户登录"
        return render(request, 'login/confirm.html', locals())


def captcha_view(request):
    if request.POST:
        form = TestCaptcha(request.POST)
        if form.is_valid():
            human = True
    else:
        form = TestCaptcha()
    return render(request, 'captcha.html', locals())
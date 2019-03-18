# author:Welisit Wang
# email:Welisit123@gmail.com
import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == "__main__":

    subject, from_email, to = '主题内容', 'welisit@qq.com', 'welisit123@gmail.com'
    text_content = '文本内容'
    html_content = '<h1>html内容</h1><a href="http://www.baidu.com">百度</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

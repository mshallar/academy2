# مشروع تطوير موقع أكاديمية تعليمية
الشيفرة المصدرية الخاصة بموقع أكاديمية تعليمية لبيع الدورات التعليمية المتوفرة على شكل فيديوهات باستخدام جانغو Django والمقدم كمشروع تخرج عن [دورة تطوير التطبيقات باستخدام لغة البرمجة بايثون Python](https://academy.hsoub.com/learn/python-application-development/) من أكاديمية حسوب

## موفع أكاديمية تعليمية
متجر إلكتروني كامل، يوفر خدمات الدفع عبر البطاقات البنكية باستخدام Stripe.
ويعمل الموقع باللغتين العربية والإنجليزية.
يمكن إضافة الدورات والدروس من قبل مدير الموقع.
كما يمكن إضافة التعليقات أسفل كل درس فيديو.
ستحتاج للتسجيل أولًا ومن ثم تسجيل الدخول ومن ثم شراء الدورة لتتمكن من تصفح الدروس.

### المتطلبات

+ Python >= 3.11
+ pip 22.3.1

## طريقة التثبيت

1. نسخ المستودع `git clone https://github.com/mshallar/academy2`
2. الانتقال إلى المجلد `cd academy2-main`
3. تثبيت المكتبات والتطبيقات اللازمة لعمل المشروع `pip install -r requirements.txt`
4. تشغيل ملفات التهجير `python manage.py migrate`
5. تشغيل المشروع `python manage.py runserver`
6. تجربة المشروع من خلال العنوان `http://127.0.0.1:8000`

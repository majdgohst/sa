# 🛡️ Device Control — دليل الرفع على Render.com

## خطوات الرفع (5 دقائق فقط)

### 1️⃣ ارفع الملفات على GitHub
1. اذهب إلى https://github.com وسجل دخول
2. انقر **New repository** → اسم: `device-control` → **Create**
3. انقر **uploading an existing file**
4. اسحب كل الملفات (app.py, requirements.txt, Procfile, وملف templates/) وانقر **Commit**

### 2️⃣ ارفع على Render.com
1. اذهب إلى https://render.com وسجل دخول بـ GitHub
2. انقر **New** → **Web Service**
3. اختر الـ repository اللي أنشأته
4. الإعدادات:
   - **Name**: device-control
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 app:app`
5. انقر **Create Web Service**

### 3️⃣ استخدام التطبيق
بعد 2-3 دقائق سيعطيك Render رابط مثل:
```
https://device-control-xxxx.onrender.com
```

- **الكمبيوتر (أنت)**: افتح الرابط مباشرة ← لوحة التحكم
- **الموبايل**: افتح `https://your-link.onrender.com/mobile` ← صفحة الاتصال

## الملفات
```
project/
├── app.py              ← السيرفر
├── requirements.txt    ← المكتبات
├── Procfile            ← إعدادات التشغيل
└── templates/
    ├── dashboard.html  ← لوحة التحكم (الكمبيوتر)
    └── mobile.html     ← صفحة الموبايل
```

## الأوامر المتاحة
| الأمر | الوظيفة |
|-------|---------|
| ping | اختبار الاتصال |
| vibrate | اهتزاز الموبايل |
| get_battery | نسبة البطارية |
| get_network | معلومات الشبكة |
| get_location | الموقع الجغرافي |
| get_screen | معلومات الشاشة |
| get_info | كل المعلومات |
| alert:رسالة | رسالة تظهر على الشاشة |

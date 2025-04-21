# PyroItaly

<p align="center">
  <img src="https://raw.githubusercontent.com/ItalyMusic/imagepyroitaly/main/pyroitaly.png" alt="PyroItaly Logo">
</p>

PyroItaly هي مكتبة واجهة برمجة تطبيقات MTProto لـ Telegram مكتوبة بلغة Python، وهي نسخة محسنة ومعاد تسميتها من pyrogram.

## الميزات

- **أداء محسن**: استخدام uvloop وorjson وتقنيات النسخ الصفري لتحسين الأداء
- **استقرار أفضل**: معالجة أفضل للأخطاء وإعادة الاتصال التلقائي
- **تجربة مطور محسنة**: توثيق شامل وتعليقات نمطية ونظام تسجيل متطور
- **نظام البرامج المساعدة**: دعم للبرامج المساعدة مع hooks/events
- **أدوات إدارة الجلسات**: تصدير واستيراد الجلسات بسهولة
- **أوامر مفيدة**: أوامر مدمجة مثل /ping و/status و/debug

## التثبيت

```bash
pip install pyroitaly
```

للحصول على أداء أفضل، قم بتثبيت الإضافات الاختيارية:

```bash
pip install "pyroitaly[speedup]"
```

## مثال سريع

### بوت تيليجرام

```python
from pyroitaly import Client, filters

app = Client(
    "my_bot",
    api_id=12345,
    api_hash="0123456789abcdef0123456789abcdef",
    bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(f"مرحباً {message.from_user.mention}!")

app.run()
```

### مستخدم عادي (Userbot)

```python
from pyroitaly import Client, filters

app = Client(
    "my_account",
    api_id=12345,
    api_hash="0123456789abcdef0123456789abcdef"
)

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_command(client, message):
    await message.edit_text("Pong!")

app.run()
```

## استخدام نظام البرامج المساعدة

```python
from pyroitaly import Client
from pyroitaly.plugins import PluginSystem

app = Client("my_bot")
plugin_system = PluginSystem(app)

# تسجيل برنامج مساعد
plugin = plugin_system.register_plugin(
    name="my_plugin",
    version="1.0.1",
    description="برنامج مساعد للتجربة",
    author="PyroItaly"
)

# تسجيل أمر
@plugin_system.register_command("my_plugin", "hello", description="يقول مرحباً")
async def hello_command(client, message):
    await message.reply_text("مرحباً بك!")

# تسجيل hook
@plugin_system.register_hook("bot_start")
async def on_bot_start():
    print("تم تشغيل البوت!")

app.run()
```

## استخدام إعادة الاتصال التلقائي

```python
from pyroitaly import Client
from pyroitaly.plugins import AutoReconnect

app = Client("my_bot")
auto_reconnect = AutoReconnect(app)

async def main():
    await app.start()
    await auto_reconnect.start()
    
    # البوت سيعيد الاتصال تلقائياً عند انقطاع الاتصال
    
    await app.idle()

app.run(main())
```

## إدارة الجلسات

```python
from pyroitaly import Client
from pyroitaly.plugins import SessionManager

async def export_session():
    app = Client("my_account")
    await app.start()
    
    # تصدير الجلسة
    session_str = await SessionManager.export_session(app)
    print(f"جلستك: {session_str}")
    
    # تصدير الجلسة مع كلمة مرور
    encrypted_session = await SessionManager.export_session(app, password="my_password")
    print(f"جلستك المشفرة: {encrypted_session}")
    
    await app.stop()

async def import_session(session_str):
    app = Client("imported_session")
    
    # استيراد الجلسة
    await SessionManager.import_session(app, session_str)
    
    await app.start()
    me = await app.get_me()
    print(f"تم تسجيل الدخول كـ {me.first_name}")
    await app.stop()
```

## المساهمة

المساهمات مرحب بها! يرجى اتباع هذه الخطوات:

1. قم بعمل fork للمستودع
2. قم بإنشاء فرع للميزة الخاصة بك (`git checkout -b feature/amazing-feature`)
3. قم بعمل commit للتغييرات (`git commit -m 'إضافة ميزة رائعة'`)
4. قم بدفع الفرع (`git push origin feature/amazing-feature`)
5. قم بفتح طلب سحب

## الترخيص

هذا المشروع مرخص بموجب ترخيص GNU Lesser General Public License v3.0 - انظر ملف [LICENSE](LICENSE) للحصول على التفاصيل.

## شكر وتقدير

- [Dan](https://github.com/delivrance) - مؤلف Pyrogram الأصلي
- [ItalyMusic](https://github.com/ItalyMusic) - مؤلف PyroItaly

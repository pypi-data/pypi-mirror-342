# مكتبة italymusic

مكتبة italymusic هي نسخة معدلة من مكتبة [pyutube](https://github.com/Hetari/pyutube) مع إضافة دعم لبوتات وحسابات التليجرام وتقنية بحث فريدة.

## المميزات

- تحميل فيديوهات يوتيوب كملفات فيديو أو صوت
- البحث في يوتيوب باستخدام تقنية بحث فريدة
- دعم كامل لبوتات وحسابات التليجرام باستخدام مكتبة Pyrogram
- خيارات للتحميل بجودة أقل لتسريع عملية التنزيل والرفع إلى تليجرام
- واجهة برمجة تطبيقات سهلة الاستخدام للتكامل مع تطبيقات أخرى

## التثبيت

يمكنك تثبيت المكتبة باستخدام pip:

```bash
pip install italymusic
```

أو يمكنك تثبيتها من المصدر:

```bash
git clone https://github.com/ItalyMusic/italymusic.git
cd italymusic
pip install -e .
```

## الاستخدام الأساسي

### البحث في يوتيوب

```python
import asyncio
from italymusic.services.SearchService import SearchService

async def search_example():
    # البحث في يوتيوب
    results = await SearchService.search_youtube("أغنية عربية", limit=5)
    
    # عرض النتائج
    for result in results:
        print(f"العنوان: {result['title']}")
        print(f"الرابط: {result['url']}")
        print(f"المدة: {result['duration_text']}")
        print(f"القناة: {result['channel']}")
        print()

# تشغيل المثال
asyncio.run(search_example())
```

### تحميل فيديو من يوتيوب

```python
from italymusic.services.DownloadService import DownloadService

# تحميل فيديو
download_service = DownloadService(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    path="/path/to/save",
    quality="best",  # يمكن استخدام "low" للجودة المنخفضة
    is_audio=False  # استخدم True لتحميل الصوت فقط
)

# تنفيذ التحميل
download_service.download()
```

### استخدام المكتبة مع تليجرام

```python
import asyncio
from italymusic.telegram.TelegramYoutubeBot import TelegramYoutubeBot

async def telegram_example():
    # إنشاء كائن البوت
    bot = TelegramYoutubeBot(
        api_id="YOUR_API_ID",
        api_hash="YOUR_API_HASH",
        bot_token="YOUR_BOT_TOKEN"
    )
    
    # تهيئة البوت
    await bot.initialize()
    
    try:
        # البحث في يوتيوب وإرسال النتائج إلى محادثة تليجرام
        await bot.search_youtube(
            chat_id=123456789,
            query="أغنية عربية",
            limit=5,
            low_quality=True  # استخدام جودة منخفضة لتسريع التحميل
        )
        
        # تحميل فيديو من يوتيوب وإرساله إلى محادثة تليجرام
        await bot.download_from_url(
            chat_id=123456789,
            youtube_url="https://www.youtube.com/watch?v=VIDEO_ID",
            is_audio=False,  # استخدم True لتحميل الصوت فقط
            low_quality=True  # استخدام جودة منخفضة لتسريع التحميل
        )
    finally:
        # إيقاف البوت
        await bot.stop()

# تشغيل المثال
asyncio.run(telegram_example())
```

## أمثلة إضافية

يمكنك العثور على أمثلة إضافية في مجلد `examples`:

- `simple_example.py`: مثال بسيط للبحث والتحميل من يوتيوب
- `telegram_bot_example.py`: مثال لبوت تليجرام كامل يستخدم المكتبة

## المتطلبات

- Python 3.6+
- pytubefix
- pyrogram
- tgcrypto
- asyncio
- وغيرها من المكتبات المذكورة في ملف requirements.txt

## الترخيص

هذا المشروع مرخص تحت رخصة MIT.

## الحقوق

جميع الحقوق محفوظة لدى Italy Music in Telegram https://t.me/italy_5

"""
هذا الملف يحتوي على واجهة برمجة تطبيقات تليجرام للبحث والتحميل من يوتيوب
"""

import os
import asyncio
import tempfile
from typing import Union, List, Dict, Optional, Any

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from italymusic.services.SearchService import SearchService
from italymusic.services.TelegramService import TelegramService


class TelegramYoutubeBot:
    """
    بوت تليجرام للبحث والتحميل من يوتيوب
    """
    
    def __init__(self, api_id: str = None, api_hash: str = None, bot_token: str = None):
        """
        تهيئة بوت تليجرام للبحث والتحميل من يوتيوب
        
        المعلمات:
            api_id (str): معرف API لتليجرام (اختياري)
            api_hash (str): مفتاح API لتليجرام (اختياري)
            bot_token (str): رمز البوت لتليجرام (اختياري)
        """
        self.telegram_service = TelegramService(api_id, api_hash, bot_token)
        self.client = None
        
    async def initialize(self, session_name: str = "italymusic_bot"):
        """
        تهيئة عميل تليجرام
        
        المعلمات:
            session_name (str): اسم الجلسة (اختياري)
        """
        await self.telegram_service.initialize(session_name)
        self.client = self.telegram_service.client
        
    async def stop(self):
        """
        إيقاف عميل تليجرام
        """
        await self.telegram_service.stop()
    
    async def search_youtube(
        self, 
        chat_id: Union[int, str], 
        query: str, 
        limit: int = 5,
        low_quality: bool = True
    ) -> Message:
        """
        البحث في يوتيوب وإرسال النتائج إلى محادثة تليجرام
        
        المعلمات:
            chat_id (Union[int, str]): معرف المحادثة
            query (str): استعلام البحث
            limit (int): الحد الأقصى لعدد النتائج (اختياري، افتراضي: 5)
            low_quality (bool): استخدام جودة منخفضة لتسريع التحميل (اختياري، افتراضي: True)
            
        العائد:
            Message: رسالة تليجرام المرسلة
        """
        if not self.client:
            raise ValueError("يجب تهيئة عميل تليجرام أولاً باستخدام initialize()")
        
        # البحث في يوتيوب
        results = await SearchService.search_youtube(query, limit, low_quality)
        
        if not results:
            return await self.client.send_message(
                chat_id=chat_id,
                text="❌ لم يتم العثور على نتائج للبحث."
            )
        
        # إنشاء نص النتائج
        text = f"🔍 نتائج البحث عن: **{query}**\n\n"
        
        # إنشاء أزرار لكل نتيجة
        buttons = []
        for i, result in enumerate(results):
            text += f"{i+1}. **{result['title']}**\n"
            text += f"   ⏱️ {result['duration_text']} | 👤 {result['channel']}\n\n"
            
            # إضافة أزرار للتحميل
            buttons.append([
                InlineKeyboardButton(
                    f"🎵 تحميل صوت {i+1}",
                    callback_data=f"audio_{result['video_id']}"
                ),
                InlineKeyboardButton(
                    f"🎬 تحميل فيديو {i+1}",
                    callback_data=f"video_{result['video_id']}"
                )
            ])
        
        # إرسال النتائج مع الأزرار
        return await self.client.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    async def handle_callback(self, callback_query, low_quality: bool = True):
        """
        معالجة استجابة الأزرار
        
        المعلمات:
            callback_query: استعلام الاستجابة
            low_quality (bool): استخدام جودة منخفضة لتسريع التحميل (اختياري، افتراضي: True)
        """
        if not self.client:
            raise ValueError("يجب تهيئة عميل تليجرام أولاً باستخدام initialize()")
        
        # استخراج نوع التحميل ومعرف الفيديو
        data = callback_query.data
        chat_id = callback_query.message.chat.id
        
        # إرسال رسالة انتظار
        await callback_query.answer("جاري التحميل...")
        status_message = await self.client.send_message(
            chat_id=chat_id,
            text="⏳ جاري تحميل الملف... يرجى الانتظار."
        )
        
        try:
            if data.startswith("audio_"):
                # تحميل الصوت
                video_id = data.replace("audio_", "")
                youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                
                await self.telegram_service.download_and_send_audio(
                    chat_id=chat_id,
                    youtube_url=youtube_url,
                    low_quality=low_quality
                )
                
            elif data.startswith("video_"):
                # تحميل الفيديو
                video_id = data.replace("video_", "")
                youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                
                await self.telegram_service.download_and_send_video(
                    chat_id=chat_id,
                    youtube_url=youtube_url,
                    low_quality=low_quality
                )
            
            # حذف رسالة الانتظار
            await status_message.delete()
            
        except Exception as e:
            # في حالة حدوث خطأ، تحديث رسالة الانتظار
            await status_message.edit_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}")
    
    async def download_from_url(
        self, 
        chat_id: Union[int, str], 
        youtube_url: str, 
        is_audio: bool = False,
        low_quality: bool = True
    ) -> Message:
        """
        تحميل فيديو أو صوت من رابط يوتيوب وإرساله إلى محادثة تليجرام
        
        المعلمات:
            chat_id (Union[int, str]): معرف المحادثة
            youtube_url (str): رابط يوتيوب
            is_audio (bool): تحميل كصوت (اختياري، افتراضي: False)
            low_quality (bool): استخدام جودة منخفضة لتسريع التحميل (اختياري، افتراضي: True)
            
        العائد:
            Message: رسالة تليجرام المرسلة
        """
        if not self.client:
            raise ValueError("يجب تهيئة عميل تليجرام أولاً باستخدام initialize()")
        
        # إرسال رسالة انتظار
        status_message = await self.client.send_message(
            chat_id=chat_id,
            text="⏳ جاري تحميل الملف... يرجى الانتظار."
        )
        
        try:
            if is_audio:
                # تحميل الصوت
                result = await self.telegram_service.download_and_send_audio(
                    chat_id=chat_id,
                    youtube_url=youtube_url,
                    low_quality=low_quality
                )
            else:
                # تحميل الفيديو
                result = await self.telegram_service.download_and_send_video(
                    chat_id=chat_id,
                    youtube_url=youtube_url,
                    low_quality=low_quality
                )
            
            # حذف رسالة الانتظار
            await status_message.delete()
            return result
            
        except Exception as e:
            # في حالة حدوث خطأ، تحديث رسالة الانتظار
            await status_message.edit_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}")
            return status_message

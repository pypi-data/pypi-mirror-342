"""
هذا الملف يحتوي على واجهة برمجة تطبيقات تليجرام للمكتبة
"""

import os
import asyncio
import tempfile
from typing import Union, List, Dict, Optional, BinaryIO

from pyrogram import Client
from pyrogram.types import Message

from italymusic.services.DownloadService import DownloadService


class TelegramService:
    """
    خدمة تليجرام للتكامل مع بوتات وحسابات تليجرام
    """
    
    def __init__(self, api_id: str = None, api_hash: str = None, bot_token: str = None):
        """
        تهيئة خدمة تليجرام
        
        المعلمات:
            api_id (str): معرف API لتليجرام (اختياري)
            api_hash (str): مفتاح API لتليجرام (اختياري)
            bot_token (str): رمز البوت لتليجرام (اختياري)
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.client = None
        
    async def initialize(self, session_name: str = "italymusic_bot"):
        """
        تهيئة عميل تليجرام
        
        المعلمات:
            session_name (str): اسم الجلسة (اختياري)
        """
        if self.bot_token:
            # إذا كان هناك رمز بوت، استخدم وضع البوت
            self.client = Client(
                session_name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                bot_token=self.bot_token
            )
        else:
            # وإلا استخدم وضع المستخدم
            self.client = Client(
                session_name,
                api_id=self.api_id,
                api_hash=self.api_hash
            )
        
        await self.client.start()
        
    async def stop(self):
        """
        إيقاف عميل تليجرام
        """
        if self.client:
            await self.client.stop()
    
    async def download_and_send_audio(
        self, 
        chat_id: Union[int, str], 
        youtube_url: str, 
        caption: str = None,
        low_quality: bool = True
    ) -> Message:
        """
        تحميل الصوت من يوتيوب وإرساله إلى محادثة تليجرام
        
        المعلمات:
            chat_id (Union[int, str]): معرف المحادثة
            youtube_url (str): رابط يوتيوب
            caption (str): نص الوصف (اختياري)
            low_quality (bool): استخدام جودة منخفضة لتسريع التحميل (اختياري، افتراضي: True)
            
        العائد:
            Message: رسالة تليجرام المرسلة
        """
        if not self.client:
            raise ValueError("يجب تهيئة عميل تليجرام أولاً باستخدام initialize()")
        
        # إنشاء مجلد مؤقت للتحميل
        temp_dir = tempfile.mkdtemp()
        
        try:
            # تحميل الصوت
            download_service = DownloadService(
                url=youtube_url,
                path=temp_dir,
                quality="low" if low_quality else "best",
                is_audio=True
            )
            
            # تنفيذ التحميل
            video, video_id, _, video_audio, _ = await asyncio.to_thread(download_service.download_preparing)
            audio_filename = await asyncio.to_thread(
                download_service.download_audio, 
                video, 
                video_audio, 
                video_id
            )
            
            # الحصول على المسار الكامل للملف
            audio_path = os.path.join(temp_dir, audio_filename)
            
            # إرسال الملف الصوتي إلى تليجرام
            if not caption:
                caption = f"🎵 {video.title}\n\nتم التحميل بواسطة @italy_5"
                
            return await self.client.send_audio(
                chat_id=chat_id,
                audio=audio_path,
                caption=caption,
                title=video.title,
                performer=video.author if hasattr(video, 'author') else "Unknown"
            )
            
        finally:
            # تنظيف الملفات المؤقتة
            for file in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass
    
    async def download_and_send_video(
        self, 
        chat_id: Union[int, str], 
        youtube_url: str, 
        caption: str = None,
        low_quality: bool = True
    ) -> Message:
        """
        تحميل الفيديو من يوتيوب وإرساله إلى محادثة تليجرام
        
        المعلمات:
            chat_id (Union[int, str]): معرف المحادثة
            youtube_url (str): رابط يوتيوب
            caption (str): نص الوصف (اختياري)
            low_quality (bool): استخدام جودة منخفضة لتسريع التحميل (اختياري، افتراضي: True)
            
        العائد:
            Message: رسالة تليجرام المرسلة
        """
        if not self.client:
            raise ValueError("يجب تهيئة عميل تليجرام أولاً باستخدام initialize()")
        
        # إنشاء مجلد مؤقت للتحميل
        temp_dir = tempfile.mkdtemp()
        
        try:
            # تحميل الفيديو
            download_service = DownloadService(
                url=youtube_url,
                path=temp_dir,
                quality="360p" if low_quality else "best",
                is_audio=False
            )
            
            # تنفيذ التحميل
            video, video_id, streams, video_audio, quality = await asyncio.to_thread(download_service.download_preparing)
            video_file = await asyncio.to_thread(download_service.video_service.get_video_streams, quality, streams)
            
            if not video_file:
                raise ValueError("فشل في الحصول على تدفق الفيديو")
                
            video_filename = await asyncio.to_thread(
                download_service.download_video, 
                video, 
                video_id, 
                video_file, 
                video_audio
            )
            
            # الحصول على المسار الكامل للملف
            for file in os.listdir(temp_dir):
                if file.endswith(".mp4"):
                    video_path = os.path.join(temp_dir, file)
                    break
            else:
                raise FileNotFoundError("لم يتم العثور على ملف الفيديو")
            
            # إرسال الفيديو إلى تليجرام
            if not caption:
                caption = f"🎬 {video.title}\n\nتم التحميل بواسطة @italy_5"
                
            return await self.client.send_video(
                chat_id=chat_id,
                video=video_path,
                caption=caption,
                supports_streaming=True
            )
            
        finally:
            # تنظيف الملفات المؤقتة
            for file in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass

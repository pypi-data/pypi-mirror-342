"""
هذا الملف يحتوي على واجهة برمجة تطبيقات البحث في يوتيوب
"""

import re
import asyncio
import tempfile
import requests
from typing import List, Dict, Optional, Any

from italymusic.services.DownloadService import DownloadService


class SearchService:
    """
    خدمة البحث في يوتيوب
    """
    
    @staticmethod
    async def search_youtube(query: str, limit: int = 5, low_quality: bool = True) -> List[Dict[str, Any]]:
        """
        البحث في يوتيوب باستخدام الطريقة الرسمية
        
        المعلمات:
            query (str): استعلام البحث
            limit (int): الحد الأقصى لعدد النتائج (اختياري، افتراضي: 5)
            low_quality (bool): استخدام جودة منخفضة لتسريع التحميل (اختياري، افتراضي: True)
            
        العائد:
            List[Dict[str, Any]]: قائمة بنتائج البحث
        """
        try:
            # استخدام الطريقة البديلة للبحث
            return await SearchService.search_youtube_alternative(query, limit, low_quality)
        except Exception as e:
            print(f"خطأ في البحث في يوتيوب: {str(e)}")
            return []
    
    @staticmethod
    async def search_youtube_alternative(query: str, limit: int = 5, low_quality: bool = True) -> List[Dict[str, Any]]:
        """
        دالة بديلة للبحث في يوتيوب باستخدام طلبات HTTP مباشرة
        
        المعلمات:
            query (str): استعلام البحث
            limit (int): الحد الأقصى لعدد النتائج (اختياري، افتراضي: 5)
            low_quality (bool): استخدام جودة منخفضة لتسريع التحميل (اختياري، افتراضي: True)
            
        العائد:
            List[Dict[str, Any]]: قائمة بنتائج البحث
        """
        try:
            # طريقة بديلة: استخدام واجهة برمجة تطبيقات غير رسمية
            search_term = query.replace(" ", "+")
            url = f"https://www.youtube.com/results?search_query={search_term}"
            
            response = requests.get(url)
            if response.status_code == 200:
                html = response.text
                video_ids = re.findall(r"watch\?v=(\S{11})", html)
                unique_video_ids = []
                
                # إزالة التكرارات والحصول على معرفات فريدة
                for video_id in video_ids:
                    if video_id not in unique_video_ids:
                        unique_video_ids.append(video_id)
                    if len(unique_video_ids) >= limit:
                        break
                
                videos = []
                for video_id in unique_video_ids:
                    # الحصول على معلومات الفيديو
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    # استخدام italymusic للحصول على معلومات الفيديو
                    try:
                        temp_dir = tempfile.mkdtemp()
                        download_service = DownloadService(
                            url=video_url,
                            path=temp_dir,
                            quality="low" if low_quality else "best",
                            is_audio=True
                        )
                        
                        # استخدام طريقة download_preparing للحصول على معلومات الفيديو فقط
                        video_info = await asyncio.to_thread(download_service.download_preparing)
                        
                        if video_info and len(video_info) >= 1:
                            video = video_info[0]  # الفيديو هو العنصر الأول في القائمة المرجعة
                            
                            title = video.title if hasattr(video, 'title') else f"YouTube Video {video_id}"
                            duration_seconds = video.length if hasattr(video, 'length') else 0
                            minutes = duration_seconds // 60
                            seconds = duration_seconds % 60
                            duration_text = f"{minutes}:{seconds:02d}"
                            
                            videos.append({
                                "title": title,
                                "url": video_url,
                                "duration": duration_seconds,
                                "duration_text": duration_text,
                                "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                                "channel": video.author if hasattr(video, 'author') else "Unknown Channel",
                                "views": "Unknown views",
                                "video_id": video_id
                            })
                    except Exception as e:
                        print(f"خطأ في الحصول على معلومات الفيديو {video_id}: {str(e)}")
                        # إضافة معلومات أساسية في حالة الفشل
                        videos.append({
                            "title": f"YouTube Video {video_id}",
                            "url": video_url,
                            "duration": 0,
                            "duration_text": "0:00",
                            "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                            "channel": "Unknown Channel",
                            "views": "Unknown views",
                            "video_id": video_id
                        })
                
                return videos
        except Exception as e:
            print(f"خطأ في البحث في يوتيوب: {str(e)}")
        
        # في حالة فشل جميع الطرق، إرجاع قائمة فارغة
        return []

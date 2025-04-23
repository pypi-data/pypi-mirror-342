import requests
import re
import json
from bs4 import BeautifulSoup

class YTSearch:
    '''يبحث عن مقاطع فيديو في يوتيوب باستخدام كلمات البحث أو رابط الفيديو مباشرة.

    المعلمات:
        query (str): يحدد استعلام البحث أو رابط الفيديو.
        limit (int, optional): يحدد الحد الأقصى لعدد النتائج عند البحث بكلمات. الافتراضي هو 20.
        language (str, optional): يحدد لغة النتائج. الافتراضي هو 'en'.
        region (str, optional): يحدد منطقة النتائج. الافتراضي هو 'US'.

    أمثلة:
        استدعاء طريقة `result` يعطي نتيجة البحث.

        # البحث باستخدام كلمات البحث
        >>> search = SearchVideo('Lege-Cy - Fel Gneena', limit = 1)
        >>> results = search.result()
        >>> if results['has_results']:
        ...     first_result = results['result'][0]
        ...     print(first_result['title'])
        ... else:
        ...     print("لم يتم العثور على نتائج")
        Lege-Cy - Fel Gneena | ليجي-سي - في الجنينه (Official Audio)

        # البحث باستخدام رابط الفيديو مباشرة (يدعم الروابط المختصرة أيضاً)
        >>> search = SearchVideo('https://youtu.be/ZdFZU5nmDxg')
        >>> results = search.result()
        >>> if results['has_results']:
        ...     video_info = results['result']
        ...     print(video_info['title'])
        ... else:
        ...     print("لم يتم العثور على معلومات للفيديو")
        Samar Tarik - TA5AREF [Part 4] | سمر طارق - تخاريف
    '''
    def __init__(self, query: str, limit: int = 20, language: str = 'en', region: str = 'US', timeout: int = None):
        self.query = query
        self.limit = limit
        self.language = language
        self.region = region
        self.timeout = timeout if timeout else 10
        self._results = {"result": []}
        self._is_url = False
        self._video_id = None
        self._error_message = None
        
        if self._is_youtube_url(query):
            self._is_url = True
            self._video_id = self._extract_video_id(query)
            self._results = {"result": None}
        

        try:
            if self._is_url and self._video_id:
                self._search_by_video_id()
            else:
                self._search()
        except Exception as e:
            error_msg = f"حدث خطأ أثناء البحث: {str(e)}"
            print(error_msg)
            self._error_message = error_msg
            if self._is_url:
                self._results = {"result": None}
            else:
                self._results = {"result": []}
    
    def _is_youtube_url(self, text: str) -> bool:
        """التحقق مما إذا كان النص رابط يوتيوب"""
        youtube_patterns = [
            r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|embed\/|v\/|shorts\/)?([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})'  # نمط خاص للروابط المختصرة
        ]
        
        for pattern in youtube_patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def _extract_video_id(self, url: str) -> str:
        """استخراج معرف الفيديو من رابط يوتيوب"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  
            r'(?:embed|v|vi|user)\/([^\/\?]+)', 
            r'(?:watch\?v=|youtu\.be\/)([^&\?\/]+)',  
            r'(?:shorts\/)([0-9A-Za-z_-]{11}).*', 
            r'youtu\.be\/([0-9A-Za-z_-]{11})'  
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _search(self):
        """البحث عن مقاطع فيديو باستخدام كلمات البحث"""
        search_url = "https://www.youtube.com/results"
        params = {
            "search_query": self.query,
            "sp": "EgIQAQ%3D%3D"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": f"{self.language}-{self.region},{self.language};q=0.9"
        }
        
        try:
            response = requests.get(search_url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
        
            data_re = re.search(r'var ytInitialData = ({.*?});', response.text)
            if not data_re:
                self._error_message = "لم يتم العثور على بيانات في صفحة البحث"
                return
            
            json_str = data_re.group(1)
            data = json.loads(json_str)
            videos = []
            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
            
            for content in contents:
                if 'itemSectionRenderer' in content:
                    items = content.get('itemSectionRenderer', {}).get('contents', [])
                    
                    for item in items:
                        if 'videoRenderer' in item:
                            video_data = item['videoRenderer']
                            video_id = video_data.get('videoId', '')
                            title = ''
                            title_runs = video_data.get('title', {}).get('runs', [])
                            if title_runs:
                                title = title_runs[0].get('text', '')
                            channel_name = ''
                            channel_id = ''
                            owner_text = video_data.get('ownerText', {}).get('runs', [])
                            if owner_text:
                                channel_name = owner_text[0].get('text', '')
                                channel_id = owner_text[0].get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId', '')
                            
                            duration = video_data.get('lengthText', {}).get('simpleText', '')
        
                            view_count_text = video_data.get('viewCountText', {}).get('simpleText', '0 views')
                            
    
                            published_time = video_data.get('publishedTimeText', {}).get('simpleText', '')
        
                            thumbnails = []
                            for thumbnail in video_data.get('thumbnail', {}).get('thumbnails', []):
                                thumbnails.append({
                                    'url': thumbnail.get('url', ''),
                                    'width': thumbnail.get('width', 0),
                                    'height': thumbnail.get('height', 0)
                                })
                            

                            video_result = {
                                'type': 'video',
                                'id': video_id,
                                'title': title,
                                'publishedTime': published_time,
                                'duration': duration,
                                'views': view_count_text, 
                                'viewCount': {
                                    'text': view_count_text,
                                    'short': self._format_view_count(view_count_text)
                                },
                                'thumbnails': thumbnails,
                                'channel': {
                                    'name': channel_name,
                                    'id': channel_id,
                                    'link': f'https://www.youtube.com/channel/{channel_id}'
                                },
                                'link': f'https://www.youtube.com/watch?v={video_id}'
                            }
                            
                            videos.append(video_result)
                            
                            if len(videos) >= self.limit:
                                break
                    
                    if len(videos) >= self.limit:
                        break
            
            if not videos:
                self._error_message = "لم يتم العثور على نتائج للبحث"
            
            self._results = {"result": videos[:self.limit]}
            
        except Exception as e:
            error_msg = f"خطأ في البحث: {str(e)}"
            print(error_msg)
            self._error_message = error_msg
            self._results = {"result": []}
    
    def _search_by_video_id(self):
        """البحث عن معلومات الفيديو باستخدام معرف الفيديو"""
        search_url = "https://www.youtube.com/results"
        params = {
            "search_query": self._video_id,
            "sp": "EgIQAQ%3D%3D" 
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": f"{self.language}-{self.region},{self.language};q=0.9"
        }
        
        try:
            response = requests.get(search_url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            data_re = re.search(r'var ytInitialData = ({.*?});', response.text)
            if not data_re:
                self._error_message = "لم يتم العثور على بيانات في صفحة البحث"
                return
            
            json_str = data_re.group(1)
            data = json.loads(json_str)
            
            video_result = None
            
            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
            
            for content in contents:
                if 'itemSectionRenderer' in content:
                    items = content.get('itemSectionRenderer', {}).get('contents', [])
                    
                    for item in items:
                        if 'videoRenderer' in item:
                            video_data = item['videoRenderer']
                            
            
                            video_id = video_data.get('videoId', '')
                            
                       
                            if video_id == self._video_id:
                         
                                title = ''
                                title_runs = video_data.get('title', {}).get('runs', [])
                                if title_runs:
                                    title = title_runs[0].get('text', '')
                                
         
                                channel_name = ''
                                channel_id = ''
                                owner_text = video_data.get('ownerText', {}).get('runs', [])
                                if owner_text:
                                    channel_name = owner_text[0].get('text', '')
                                    channel_id = owner_text[0].get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId', '')
                                
                                duration = video_data.get('lengthText', {}).get('simpleText', '')                                
                                view_count_text = video_data.get('viewCountText', {}).get('simpleText', '0 views')
                                

                                published_time = video_data.get('publishedTimeText', {}).get('simpleText', '')
                                
                    
                                thumbnails = []
                                for thumbnail in video_data.get('thumbnail', {}).get('thumbnails', []):
                                    thumbnails.append({
                                        'url': thumbnail.get('url', ''),
                                        'width': thumbnail.get('width', 0),
                                        'height': thumbnail.get('height', 0)
                                    })
                                
                   
                                video_result = {
                                    'type': 'video',
                                    'id': video_id,
                                    'title': title,
                                    'publishedTime': published_time,
                                    'duration': duration,
                                    'views': view_count_text,
                                    'viewCount': {
                                        'text': view_count_text,
                                        'short': self._format_view_count(view_count_text)
                                    },
                                    'thumbnails': thumbnails,
                                    'channel': {
                                        'name': channel_name,
                                        'id': channel_id,
                                        'link': f'https://www.youtube.com/channel/{channel_id}'
                                    },
                                    'link': f'https://www.youtube.com/watch?v={video_id}'
                                }
                                break
                    
                    if video_result:
                        break
            
            if not video_result:
                for content in contents:
                    if 'itemSectionRenderer' in content:
                        items = content.get('itemSectionRenderer', {}).get('contents', [])
                        
                        for item in items:
                            if 'videoRenderer' in item:
                                video_data = item['videoRenderer']
        
                                video_id = video_data.get('videoId', '')

                                title = ''
                                title_runs = video_data.get('title', {}).get('runs', [])
                                if title_runs:
                                    title = title_runs[0].get('text', '')
                                

                                channel_name = ''
                                channel_id = ''
                                owner_text = video_data.get('ownerText', {}).get('runs', [])
                                if owner_text:
                                    channel_name = owner_text[0].get('text', '')
                                    channel_id = owner_text[0].get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId', '')
                                
                
                                duration = video_data.get('lengthText', {}).get('simpleText', '')

                                view_count_text = video_data.get('viewCountText', {}).get('simpleText', '0 views')

                                published_time = video_data.get('publishedTimeText', {}).get('simpleText', '')

                                thumbnails = []
                                for thumbnail in video_data.get('thumbnail', {}).get('thumbnails', []):
                                    thumbnails.append({
                                        'url': thumbnail.get('url', ''),
                                        'width': thumbnail.get('width', 0),
                                        'height': thumbnail.get('height', 0)
                                    })
                                
      
                                video_result = {
                                    'type': 'video',
                                    'id': video_id,
                                    'title': title,
                                    'publishedTime': published_time,
                                    'duration': duration,
                                    'views': view_count_text,
                                    'viewCount': {
                                        'text': view_count_text,
                                        'short': self._format_view_count(view_count_text)
                                    },
                                    'thumbnails': thumbnails,
                                    'channel': {
                                        'name': channel_name,
                                        'id': channel_id,
                                        'link': f'https://www.youtube.com/channel/{channel_id}'
                                    },
                                    'link': f'https://www.youtube.com/watch?v={video_id}'
                                }
                                break
                        
                        if video_result:
                            break
            if not video_result:
                self._fallback_video_info()
            else:
                self._results = {"result": video_result}
            
        except Exception as e:
            error_msg = f"خطأ في البحث عن معلومات الفيديو: {str(e)}"
            print(error_msg)
            self._error_message = error_msg
            self._fallback_video_info()
    
    def _fallback_video_info(self):
        """طريقة احتياطية للحصول على معلومات أساسية عن الفيديو"""
        try:
            thumbnails = [
                {
                    'url': f"https://i.ytimg.com/vi/{self._video_id}/maxresdefault.jpg",
                    'width': 1280,
                    'height': 720
                },
                {
                    'url': f"https://i.ytimg.com/vi/{self._video_id}/hqdefault.jpg",
                    'width': 480,
                    'height': 360
                }
            ]
            
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={self._video_id}&format=json"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(oembed_url, headers=headers, timeout=self.timeout)
            
            title = ""
            channel_name = ""
            
            if response.status_code == 200:
                try:
                    oembed_data = response.json()
                    title = oembed_data.get('title', '')
                    channel_name = oembed_data.get('author_name', '')
                except json.JSONDecodeError:
                    pass
            
            if not title or not channel_name:
                video_url = f"https://www.youtube.com/watch?v={self._video_id}"
                try:
                    response = requests.get(video_url, headers=headers, timeout=self.timeout)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        if not title:
                            title_tag = soup.find('meta', {'property': 'og:title'})
                            if title_tag and 'content' in title_tag.attrs:
                                title = title_tag['content']
                        
                        if not channel_name:
                            channel_tag = soup.find('link', {'itemprop': 'name'})
                            if channel_tag and 'content' in channel_tag.attrs:
                                channel_name = channel_tag['content']
                except Exception:
                    pass
            
            video_result = {
                'type': 'video',
                'id': self._video_id,
                'title': title,
                'publishedTime': '',
                'duration': '0:00',
                'views': '0 views',
                'viewCount': {
                    'text': '0 views',
                    'short': '0 views'
                },
                'thumbnails': thumbnails,
                'channel': {
                    'name': channel_name,
                    'id': '',
                    'link': ''
                },
                'link': f'https://www.youtube.com/watch?v={self._video_id}'
            }
            
            self._results = {"result": video_result}
        
        except Exception as e:
            error_msg = f"خطأ في الطريقة الاحتياطية: {str(e)}"
            print(error_msg)
            self._error_message = error_msg
            self._results = {"result": {
                'type': 'video',
                'id': self._video_id,
                'title': '',
                'publishedTime': '',
                'duration': '0:00',
                'views': '0 views',
                'viewCount': {
                    'text': '0 views',
                    'short': '0 views'
                },
                'thumbnails': [
                    {
                        'url': f"https://i.ytimg.com/vi/{self._video_id}/hqdefault.jpg",
                        'width': 480,
                        'height': 360
                    }
                ],
                'channel': {
                    'name': '',
                    'id': '',
                    'link': ''
                },
                'link': f'https://www.youtube.com/watch?v={self._video_id}'
            }}
    
    def _format_view_count(self, view_count_text):
        """تحويل عدد المشاهدات إلى صيغة مختصرة"""
        if not view_count_text or 'views' not in view_count_text:
            return '0 views'
        
        count = view_count_text.split(' ')[0]
        
        if ',' in count:
            count = count.replace(',', '')
        
        try:
            count_num = int(count)
            
            if count_num >= 1000000000:
                return f'{count_num/1000000000:.1f}B views'
            elif count_num >= 1000000:
                return f'{count_num/1000000:.1f}M views'
            elif count_num >= 1000:
                return f'{count_num/1000:.1f}K views'
            else:
                return f'{count_num} views'
        except ValueError:
            return view_count_text
    
    def result(self):
        """الحصول على نتائج البحث"""
        result_dict = self._results.copy()
    
        if self._error_message:
            result_dict['error'] = self._error_message
        
        result_dict['is_url'] = self._is_url
        
        if self._is_url:
            result_dict['has_results'] = result_dict['result'] is not None
        else:
            result_dict['has_results'] = len(result_dict['result']) > 0
        
        return result_dict
    
    def has_results(self):
        """التحقق مما إذا كان هناك نتائج للبحث"""
        if self._is_url:
            return self._results['result'] is not None
        else:
            return len(self._results['result']) > 0
    
    def get_first_result(self):
        """الحصول على النتيجة الأولى من البحث بشكل آمن"""
        if not self._is_url and self._results['result'] and len(self._results['result']) > 0:
            return self._results['result'][0]
        elif self._is_url and self._results['result']:
            return self._results['result']
        else:
            return None
    
    def get_error(self):
        """الحصول على رسالة الخطأ إذا كانت متوفرة"""
        return self._error_message
    
    def next(self):
        """الانتقال إلى الصفحة التالية من النتائج (غير مدعوم حالياً)"""
        return False

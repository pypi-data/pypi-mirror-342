# YTeva

<p align="center">
  <img src="https://raw.githubusercontent.com/ItalyMusic/ytevalogo/main/ytevalogo.png" alt="YTeva Logo">
</p>

YTeva is a Python library that fetches and downloads audio files using Pyrogram.

## Installation

```bash
pip install yteva
```

## Usage
This is for Pyrogram users.

```python
from pyrogram import Client
from yteva import YTeva

app = Client("my_bot", api_id=123456, api_hash="your_api_hash", bot_token="your_bot_token")
yteva = YTeva(api_key="your_api_key", bot_app=app)

async async def main():
    await app.start()
    result = await yteva.download_audio("your_video_id")
    print("Downloaded:", result)
    await app.stop()
```
If you are using any program you can extract the link
```python
from yteva import YTeva_direct


async def main():
    yd = YTeva_direct(api_key="API_KEY")
    test = await yd.play_audio_direct("VIDEO_ID") 
    print(test)

if __name__ == "__main__":
    asyncio.run(main())  
```

### Search for videos 

```python
from yteva import YTSearch

search1 = YTSearch('Abo El Anwar - Scoo Scoo| ابو الانوار - سكو سكو', limit=1)
results1 = search1.result()

if results1['has_results']:
    first_result = results1['result'][0]
    print("Title:", first_result['title'])
    print("Link:", first_result['link'])
    print("Thumbnails:", first_result['thumbnails'][0]['url'])
    print("Channel Name:", first_result['channel']['name'])
    print("Duration:", first_result['duration'])
    print("Views:", first_result['views'])
else:
    print("No information found for the video")
    if 'error' in results1:
        print("The Reason:", results1['error'])

search2 = YTSearch('https://www.youtube.com/watch?v=u7QhfjHhnaA')
result2 = search2.result()

if result2['has_results']:
    video_info = result2['result']
    print("Title:", video_info['title'])
    print("Link:", video_info['link'])
    print("Thumbnails:", video_info['thumbnails'][0]['url'])
    print("Channel Name:", video_info['channel']['name'])
    print("Duration:", video_info['duration'])
    print("Views:", video_info['views'])
else:
    print("No information found for the video")
    if 'error' in result2:
        print("The Reason:", result2['error'])

search3 = YTSearch('https://youtu.be/u7QhfjHhnaA')
result3 = search3.result()

if result3['has_results']:
    video_info = result3['result']
    print("Title:", video_info['title'])
    print("Link:", video_info['link'])
    print("Thumbnails:", video_info['thumbnails'][0]['url'])
    print("Channel Name:", video_info['channel']['name'])
    print("Duration:", video_info['duration'])
    print("Views:", video_info['views'])
else:
    print("No information found for the video.")
    if 'error' in result3:
        print("The Reason:", result3['error'])
```




## Developers of this project

- [𝙴𝚜𝚕𝚊𝚖 𝙼𝚘𝚑𝚊𝚖𝚎𝚍](https://github.com/source-eva) - Original YTeva Author 
- [𝙸𝚃𝙰𝙻𝚈 𝙼𝚄𝚂𝙸𝙲](https://github.com/ItalyMusic) - YTeva Co-Author

## Join A Channel Telegram 🔻

- Channel Eslam

[![Telegram Channel](https://img.shields.io/badge/Telegram%20Channel-Join%20Now-blue?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/yteva_lib)  

- Channel italy 

[![Telegram Channel](https://img.shields.io/badge/Telegram%20Channel-Join%20Now-blue?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/italy_5)  


## License

MIT License

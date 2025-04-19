<h1 align="center">
  Reels Downloader
</h1>
<p align="center">
    <em><b>Помогает получить прямую ссылку на reels в разных разрешениях</b></em>
</p>

## Установка

Установить новейшую версию можно командой:

```shell
pip install instagram-reels
```

## Пример работы

Скачивание reels с авторизацией:

```python
import asyncio
import requests
from instagram_reels.main.InstagramAPIClientImpl import InstagramAPIClientImpl

SESSION_ID = "your_session"


async def init_client():
    # С авторизацией
    
    # С SESSION_ID
    client = await InstagramAPIClientImpl().login_with_sessionid(sessionid=SESSION_ID).reels()
    # Или с логином и паролем
    client = await InstagramAPIClientImpl().login_with_credentials(username="", password="").reels()
    
    # Или без авторизации
    client = await InstagramAPIClientImpl().reels()
    return client


async def download_reels(clip_name: str, reel_id: str):
    client = await init_client()
    info = await client.get(reel_id)
    with open(clip_name, "wb+") as out_file:
        out_file.write((requests.get(info.videos[0].url)).content)


asyncio.run(download_reels("example.mp4", "1234"))
```

## Примечание

Используется два разных апи. В зависимости от того авторизованный клиент используется или нет. От этого завсит логика получения данных о рилсе. 

В случае если пользователь не авторизован можно получить видео рилса только в одном разрешении.


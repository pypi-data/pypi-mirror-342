import os
import time
import requests

from mcp.server import FastMCP
from mcp.types import TextContent

from .write_xiaohongshu import XiaohongshuPoster

mcp = FastMCP("xhs")
phone = os.getenv("phone", "")
path= os.getenv("json_path","/Users/bruce/")
def login():
    poster = XiaohongshuPoster(path)
    poster.login(phone)
    time.sleep(1)
    poster.close()

@mcp.tool()
def create_note(title: str, content: str, images: list) -> list[TextContent]:
    """Create a note (post) to xiaohongshu (rednote) with title, description, and images

    Args:
        title: the title of the note (post), which should not exceed 20 words
        content: the description of the note (post).
        images: the list of image paths or URLs to be included in the note (post)
    """
    poster = XiaohongshuPoster(path)
    poster.login(phone)
    res = ""
    try:
        # 下载网络图片到本地缓存地址
        local_images = []
        for image in images:
            if image.startswith("http"):
                local_path = download_image(image)
                local_images.append(local_path)
            else:
                local_images.append(image)
        
        poster.post_article(title, content, local_images)
        poster.close()
        res = "success"
    except Exception as e:
        res = "error:" + str(e)

    return [TextContent(type="text", text=res)]


@mcp.tool()
def create_video_note(title: str, content: str, videos: list) -> list[TextContent]:
    """Create a note (post) to xiaohongshu (rednote) with title, description, and videos

    Args:
        title: the title of the note (post), which should not exceed 20 words
        content: the description of the note (post).
        videos: the list of video paths or URLs to be included in the note (post)
    """
    poster = XiaohongshuPoster(path)
    poster.login(phone)
    res = ""
    try:
        # 下载网络图片到本地缓存地址
        local_images = []
        for video in videos:
            if video.startswith("http"):
                local_path = download_image(video)
                local_images.append(local_path)
            else:
                local_images.append(video)

        poster.post_video_article(title, content, local_images)
        poster.close()
        res = "success"
    except Exception as e:
        res = "error:" + str(e)

    return [TextContent(type="text", text=res)]


def download_image(url):
    local_filename = url.split('/')[-1]
    local_path = os.path.join("/tmp", local_filename)  # 假设缓存地址为/tmp
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path

def main():
    mcp.run()

if __name__ == "__main__":
    main()
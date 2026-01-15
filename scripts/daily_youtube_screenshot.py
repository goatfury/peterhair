#!/usr/bin/env python3
import datetime
import pathlib
import shutil
import urllib.request
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCsy9I56PY3IngCf_VGjunMQ"
OUTPUT_DIR = pathlib.Path("output")


def fetch_latest_video_id() -> str:
    with urllib.request.urlopen(RSS_URL) as response:
        feed_xml = response.read()

    root = ET.fromstring(feed_xml)
    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }
    entry = root.find("atom:entry", namespaces)
    if entry is None:
        raise RuntimeError("No entries found in the YouTube RSS feed.")

    video_id = entry.findtext("yt:videoId", namespaces=namespaces)
    if not video_id:
        raise RuntimeError("Latest entry missing yt:videoId.")

    return video_id


def download_thumbnail(video_id: str) -> bytes:
    urls = [
        f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
        f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
    ]
    for index, url in enumerate(urls):
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except HTTPError as exc:
            if exc.code == 404 and index < len(urls) - 1:
                continue
            raise

    raise RuntimeError("Unable to download thumbnail image.")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    latest_path = OUTPUT_DIR / "latest.jpg"
    dated_path = OUTPUT_DIR / f"{datetime.datetime.utcnow().date().isoformat()}.jpg"

    video_id = fetch_latest_video_id()
    thumbnail_bytes = download_thumbnail(video_id)
    latest_path.write_bytes(thumbnail_bytes)

    shutil.copyfile(latest_path, dated_path)


if __name__ == "__main__":
    main()

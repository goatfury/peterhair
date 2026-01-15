#!/usr/bin/env python3
import datetime
import pathlib
import shutil
import subprocess
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCsy9I56PY3IngCf_VGjunMQ"
TIMESTAMP = "00:00:12"
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


def download_video(video_id: str, destination_dir: pathlib.Path) -> pathlib.Path:
    output_template = str(destination_dir / "video.%(ext)s")
    command = [
        "yt-dlp",
        "-f",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o",
        output_template,
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    subprocess.run(command, check=True)

    matches = list(destination_dir.glob("video.*"))
    if not matches:
        raise RuntimeError("yt-dlp did not produce a video file.")

    return matches[0]


def extract_frame(video_path: pathlib.Path, output_path: pathlib.Path) -> None:
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        TIMESTAMP,
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        str(output_path),
    ]
    subprocess.run(command, check=True)


def main() -> None:
    if shutil.which("yt-dlp") is None:
        raise RuntimeError("yt-dlp is required but not found in PATH.")
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required but not found in PATH.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    latest_path = OUTPUT_DIR / "latest.jpg"
    dated_path = OUTPUT_DIR / f"{datetime.datetime.utcnow().date().isoformat()}.jpg"

    video_id = fetch_latest_video_id()
    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_path = pathlib.Path(tmp_dir)
        video_path = download_video(video_id, temp_path)
        extract_frame(video_path, latest_path)

    shutil.copyfile(latest_path, dated_path)


if __name__ == "__main__":
    main()

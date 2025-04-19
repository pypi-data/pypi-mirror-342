import os
import requests

from pathlib import Path

from knowledge_devourer.core.instagram_client import init_reels_client
from loguru import logger


async def download_reels(clip_path: Path, reel_id: str):
    logger.info("Starting download for reel id: %s", reel_id)
    client = await init_reels_client()

    logger.info("Fetching reel data…")
    info = await client.get(reel_id)
    logger.debug(f"Reel info received: {info}")

    if not info.videos or not info.videos[0].url:
        logger.error("No video URL found in reel data; skipping.")
        return info

    video_url = info.videos[0].url
    logger.info(f"Downloading video from {video_url}")
    resp = requests.get(video_url, stream=True)
    resp.raise_for_status()

    os.makedirs(os.path.dirname(clip_path), exist_ok=True)
    total = 0
    with open(clip_path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
            total += len(chunk)
    logger.info(f"Saved video to {clip_path} ({total} bytes)")

    return info


def download_preview_image(url: str, dest: Path):
    logger.info("Downloading preview image from %s", url)
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)

import os
import time
import json
import random
import asyncio
import subprocess

from subwhisperer.cli import process_video
from knowledge_devourer.core.config import Config
from knowledge_devourer.core.instagram_client import get_instagram_client
from knowledge_devourer.core.utils import to_dict_recursively, extract_content_type_and_content_id_from_link
from knowledge_devourer.core.downloader import download_reels, download_preview_image
from loguru import logger


def process_posts(
    links: list[str],
    config: Config,
):
    ig = get_instagram_client()
    for idx, link in enumerate(links, 1):
        content_type, content_id = extract_content_type_and_content_id_from_link(link)
        if content_type != "post":
            continue

        desc_path = config.posts_meta_data_dir_full_path / f"{content_id}.json"

        if desc_path.exists():
            logger.info(f"Skipping post {content_id}; already downloaded.")
            continue

        post = ig.post(content_id)

        with open(desc_path, "w", encoding="utf-8") as fh:
            logger.info(f"Saving post meta data to {desc_path}...")
            json_data = to_dict_recursively(post)
            fh.write(json.dumps(json_data, indent=2, ensure_ascii=False))

        for i, media in enumerate(ig.download(post, parallel=4), 1):
            ext = media.content_type.split("/")[-1].lower()
            filename = config.posts_dir_full_path / f"{content_id}_{i:02d}.{ext}"
            logger.info(f"Saving post media data to {filename}...")
            media.save(filename)

        if idx % 1 == 0:
            delay = random.randint(config.min_delay, config.max_delay)
            logger.info(f"Sleeping {delay} seconds to avoid rate limit...")
            time.sleep(delay)


def process_reels(
    links: list[str],
    config: Config,
):
    for idx, link in enumerate(links, 1):
        content_type, content_id = extract_content_type_and_content_id_from_link(link)
        if content_type != "reel":
            continue

        video_path = config.reels_dir_full_path / f"{content_id}.mp4"
        audio_path = config.reels_audio_dir_full_path / f"{content_id}.flac"
        desc_path = config.reels_meta_data_dir_full_path / f"{content_id}.json"
        preview_path = config.reels_previews_dir_full_path / f"{content_id}.jpg"
        subtitle_path = config.subwhisperer_output_dir_full_path / f"{content_id}.srt"
        transcript_path = config.subwhisperer_output_dir_full_path / f"{content_id}.txt"
        random_delay = random.randint(config.min_delay, config.max_delay)

        logger.info(f"Processing {idx}/{len(links)}: {content_id}")

        ig_request_made = False
        try:
            # only fetch if we don't already have both video + description
            if not os.path.exists(video_path) or not os.path.exists(desc_path):
                info = asyncio.run(download_reels(video_path, content_id))
                ig_request_made = True

                # dump out the JSON of the metadata
                with open(desc_path, "w", encoding="utf-8") as fh:
                    logger.info(f"Saving reel meta data to {desc_path}...")
                    json.dump(to_dict_recursively(info), fh, indent=2, ensure_ascii=False)

                # pick highest‐res preview and download it
                if hasattr(info, "previews") and info.previews:
                    best = max(info.previews, key=lambda p: getattr(p, "width", 0))
                    if not os.path.exists(preview_path):
                        logger.info(f"Downloading reel preview to {preview_path}...")
                        download_preview_image(best.url, preview_path)

            # extract audio if needed
            if not os.path.exists(audio_path) and os.path.exists(video_path):
                logger.info(f"Extracting reel audio from {video_path} to {audio_path}...")
                subprocess.run(
                    ["ffmpeg", "-i", video_path, "-ar", "16000", "-ac", "1",
                     "-map", "0:a", "-c:a", "flac", audio_path],
                    check=False
                )

            if not os.path.exists(transcript_path) or not os.path.exists(subtitle_path):
                logger.info(f"Extracting text transcription and subtitle transcription from {video_path} "
                            f"to {subtitle_path} and {transcript_path}...")
                process_video(
                    video_file_full_path=video_path,
                    subtitle_file_full_path=subtitle_path,
                    txt_file_full_path=transcript_path,
                    output_directory_full_path=config.subwhisperer_output_dir_full_path
                )

            # throttle if we actually hit the API
            if ig_request_made:
                logger.info(f"Sleeping for {random_delay} seconds to avoid rate‐limit...")
                time.sleep(random_delay)
                ig_request_made = False
            else:
                logger.info(f"Already have everything for {content_id}, skipping.")

        except Exception as exc:
            logger.error(f"Error processing {content_id}: {exc}")
            logger.info(f"Sleeping for {random_delay} seconds before continuing...")
            time.sleep(random_delay)
            continue

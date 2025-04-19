import os
from pathlib import Path


class Config:
    def __init__(self, base_dir: Path = None):
        # Directory structure
        if base_dir is None:
            self.base_dir: Path = Path(__file__).parent.parent
        else:
            self.base_dir: Path = base_dir
            os.makedirs(self.base_dir, exist_ok=True)

        self.posts_dir_full_path: Path = self.base_dir / "posts"
        os.makedirs(self.posts_dir_full_path, exist_ok=True)

        self.posts_meta_data_dir_full_path: Path = self.base_dir / "posts_meta_data"
        os.makedirs(self.posts_meta_data_dir_full_path, exist_ok=True)

        self.reels_dir_full_path: Path = self.base_dir / "reels"
        os.makedirs(self.reels_dir_full_path, exist_ok=True)

        self.reels_audio_dir_full_path: Path = self.base_dir / "reels_audio"
        os.makedirs(self.reels_audio_dir_full_path, exist_ok=True)

        self.reels_meta_data_dir_full_path: Path = self.base_dir / "reels_meta_data"
        os.makedirs(self.reels_meta_data_dir_full_path, exist_ok=True)

        self.reels_previews_dir_full_path: Path = self.base_dir / "reels_previews"
        os.makedirs(self.reels_previews_dir_full_path, exist_ok=True)

        self.subwhisperer_output_dir_full_path: Path = self.base_dir / "subwhisperer_output"
        os.makedirs(self.subwhisperer_output_dir_full_path, exist_ok=True)

        # Rate limiting
        self.min_delay = 5
        self.max_delay = 20

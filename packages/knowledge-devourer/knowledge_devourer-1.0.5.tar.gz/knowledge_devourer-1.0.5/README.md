# Installation

pip install knowledge-devourer

# Dependencies
- ffmpeg
- Subwhisperer https://github.com/Smarandii/subwhisperer

# CUDA
```commandline
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

## Check if CUDA is available:

```commandline
python -c "import torch; print(torch.cuda.is_available())"
```
"""Module for applying vector algorithms using OpenAI CLIP"""

from pathlib import Path
import numpy
import torch
import clip
from PIL.Image import Image


def get_vectors(image: Image) -> numpy.ndarray:
    """Generates vectors for a pillow image"""
    device = "cpu"
    model, preprocess = clip.load(
        str(Path(__file__).parent.parent / "resources" / "models" / "ViT-B-32.pt"),
        device=device,
    )
    image = (
        preprocess(image)
        .unsqueeze(0)  # pyright: ignore [reportAttributeAccessIssue] clip has no static typing
        .to(device)
    )
    with torch.no_grad():
        image_features = model.encode_image(image)
        return image_features.softmax(dim=-1).cpu().numpy()

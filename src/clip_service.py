import torch

import clip
from PIL.Image import Image


def get_vectors(image: Image):
    device = "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    image = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        return image_features.softmax(dim=-1).cpu().numpy()
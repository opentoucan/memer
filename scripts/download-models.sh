#!/bin/sh

curl -sL https://openaipublic.azureedge.net/clip/models/40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af/ViT-B-32.pt \
    --create-dirs \
    -o ./resources/models/ViT-B-32.pt

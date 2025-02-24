#!/bin/sh

model=$(yq -oy '.app.model.name' pyproject.toml)

AVAILABLE_MODELS=$(curl -sL https://raw.githubusercontent.com/openai/CLIP/refs/heads/main/clip/clip.py | sed -n '/https:\/\/openaipublic.azureedge.net/p' | tr -d '\n')
echo "{${AVAILABLE_MODELS%,*}}" | jq --arg m "$model" -r '.[$m]' | xargs -I n1 curl -SL n1 --create-dirs -o ./resources/models/model.pt

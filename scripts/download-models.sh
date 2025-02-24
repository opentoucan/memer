#!/bin/sh

model=$0

AVAILABLE_MODELS=$(curl -sL https://raw.githubusercontent.com/openai/CLIP/refs/heads/main/clip/clip.py | sed -n '/https:\/\/openaipublic.azureedge.net/p' | tr -d '\n')
filename=$(echo $model | tr / -)
echo "{${AVAILABLE_MODELS%,*}}" | jq --arg m "$model" -r '.[$m]' | xargs -I n1 curl -SL n1 --create-dirs -o ./resources/models/$filename.pt

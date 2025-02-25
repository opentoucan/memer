#!/bin/sh

if ! command -v yq 2>&1 >/dev/null
then
    echo "yq could not be found"
    exit 1
fi

if ! command -v jq 2>&1 >/dev/null
then
    echo "jq could not be found"
    exit 1
fi

model=$(yq -oy '.app.model.name' pyproject.toml)

AVAILABLE_MODELS=$(curl -sL https://raw.githubusercontent.com/openai/CLIP/refs/heads/main/clip/clip.py | sed -n '/https:\/\/openaipublic.azureedge.net/p' | tr -d '\n')
echo "{${AVAILABLE_MODELS%,*}}" | jq --arg m "$model" -r '.[$m]' | xargs -I n1 curl -SL n1 --create-dirs -o ./resources/models/model.pt

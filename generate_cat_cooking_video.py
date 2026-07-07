"""
Gemini API (Veo) を使って「猫が料理を作っている」動画を生成するスクリプト。
複数シーンを個別に生成し、ffmpeg(imageio-ffmpeg同梱)で結合して長尺化する。
リアルな質感に近づけるため、プロンプトとnegative_promptで「AI感」を抑制する。

事前準備:
    pip install google-genai imageio-ffmpeg
    export GEMINI_API_KEY="あなたのAPIキー"

実行:
    python3 generate_cat_cooking_video.py
"""

import os
import subprocess
import sys
import tempfile
import time

import imageio_ffmpeg
from google import genai
from google.genai import types

REALISTIC_STYLE = (
    "photorealistic, shot on a real camera with natural handheld movement, "
    "documentary-style candid footage, real fur texture and natural cat behavior, "
    "real kitchen with natural window light, shallow depth of field, film grain, "
    "no cartoon style, no CGI render, no plastic or glossy skin, not anime"
)

NEGATIVE_PROMPT = (
    "cartoon, CGI, 3D render, anime, plastic skin, glossy artificial look, "
    "uncanny valley, distorted face, extra limbs, deformed paws, text, watermark, "
    "low quality, blurry, overexposed, unrealistic motion"
)

SCENES = [
    (
        "A fluffy orange tabby cat wearing a small chef apron, standing on its hind "
        "legs at a kitchen counter, picking up fresh vegetables from a wicker basket "
        "and placing them on a wooden cutting board, curious and focused expression. "
        + REALISTIC_STYLE
    ),
    (
        "The same fluffy orange tabby cat in a chef apron, carefully chopping "
        "vegetables on a wooden cutting board with a small kitchen knife, then "
        "sweeping them into a sizzling pan on the stove, steam and light smoke "
        "rising, warm kitchen light. " + REALISTIC_STYLE
    ),
    (
        "The same fluffy orange tabby cat stirring a pot with a wooden spoon, "
        "lifting the spoon to taste the sauce, reacting with a satisfied happy "
        "expression, whiskers twitching. " + REALISTIC_STYLE
    ),
    (
        "The same fluffy orange tabby cat plating the finished dish onto a small "
        "plate, garnishing it neatly, then turning to look at the camera and "
        "tilting its head proudly as if presenting the dish. " + REALISTIC_STYLE
    ),
]


def generate_clip(client, prompt: str, index: int) -> str:
    print(f"[{index + 1}/{len(SCENES)}] 動画生成を開始します...")
    operation = client.models.generate_videos(
        model="veo-3.0-generate-001",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            aspect_ratio="9:16",  # TikTok向け縦動画
            negative_prompt=NEGATIVE_PROMPT,
        ),
    )

    while not operation.done:
        print(f"[{index + 1}/{len(SCENES)}] 生成中... (10秒待機)")
        time.sleep(10)
        operation = client.operations.get(operation)

    video = operation.response.generated_videos[0]
    output_path = f"cat_cooking_part{index + 1}.mp4"
    client.files.download(file=video.video)
    video.video.save(output_path)
    print(f"[{index + 1}/{len(SCENES)}] 保存しました: {output_path}")
    return output_path


def concat_clips(clip_paths: list[str], output_path: str) -> None:
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as list_file:
        for path in clip_paths:
            list_file.write(f"file '{os.path.abspath(path)}'\n")
        list_file_path = list_file.name

    try:
        subprocess.run(
            [
                ffmpeg_exe,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_file_path,
                "-c",
                "copy",
                output_path,
            ],
            check=True,
        )
    finally:
        os.remove(list_file_path)


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("環境変数 GEMINI_API_KEY が設定されていません。")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    clip_paths = []
    for i, prompt in enumerate(SCENES):
        path = f"cat_cooking_part{i + 1}.mp4"
        if os.path.exists(path):
            print(f"[{i + 1}/{len(SCENES)}] 既存ファイルを再利用します: {path}")
            clip_paths.append(path)
        else:
            clip_paths.append(generate_clip(client, prompt, i))

    output_path = "cat_cooking.mp4"
    print("クリップを結合しています...")
    concat_clips(clip_paths, output_path)

    print(f"完成した動画を保存しました: {output_path}")


if __name__ == "__main__":
    main()

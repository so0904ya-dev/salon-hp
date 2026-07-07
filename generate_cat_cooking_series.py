"""
「猫シェフ」シリーズの動画を、料理名を指定して生成するスクリプト。
同じ猫キャラクター(オレンジ色のキジトラ、シェフエプロン)を使い、
3シーン(準備→調理→盛り付け)を生成してffmpegで結合する(合計20〜25秒程度)。

事前準備:
    pip install google-genai imageio-ffmpeg
    export GEMINI_API_KEY="あなたのAPIキー"

実行:
    python3 generate_cat_cooking_series.py "パンケーキ"
    python3 generate_cat_cooking_series.py "ステーキ"
"""

import os
import subprocess
import sys
import tempfile
import time

import imageio_ffmpeg
from google import genai
from google.genai import types

CAT_CHARACTER = (
    "the same fluffy orange tabby cat wearing a small chef apron, "
    "consistent character design across shots"
)

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


def build_scenes(dish: str) -> list[str]:
    return [
        (
            f"{CAT_CHARACTER}, standing on its hind legs at a kitchen counter, "
            f"gathering ingredients for {dish} and arranging them neatly on the "
            f"counter, curious and focused expression. " + REALISTIC_STYLE
        ),
        (
            f"{CAT_CHARACTER}, actively preparing and cooking {dish} with its "
            f"paws, using small kitchen tools, steam or sizzling visible, "
            f"concentrating with cute determined expression. " + REALISTIC_STYLE
        ),
        (
            f"{CAT_CHARACTER}, plating the finished {dish} neatly on a small "
            f"plate, garnishing it, then turning to look at the camera and "
            f"tilting its head proudly as if presenting the dish. " + REALISTIC_STYLE
        ),
    ]


def generate_clip(client, prompt: str, index: int, total: int, output_path: str) -> str:
    print(f"[{index + 1}/{total}] 動画生成を開始します...")
    operation = client.models.generate_videos(
        model="veo-3.0-generate-001",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            aspect_ratio="9:16",
            negative_prompt=NEGATIVE_PROMPT,
        ),
    )

    while not operation.done:
        print(f"[{index + 1}/{total}] 生成中... (10秒待機)")
        time.sleep(10)
        operation = client.operations.get(operation)

    video = operation.response.generated_videos[0]
    client.files.download(file=video.video)
    video.video.save(output_path)
    print(f"[{index + 1}/{total}] 保存しました: {output_path}")
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
    if len(sys.argv) < 2:
        print('使い方: python3 generate_cat_cooking_series.py "料理名"')
        sys.exit(1)

    dish = sys.argv[1]
    slug = "".join(c if c.isalnum() else "_" for c in dish)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("環境変数 GEMINI_API_KEY が設定されていません。")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    scenes = build_scenes(dish)

    clip_paths = []
    for i, prompt in enumerate(scenes):
        part_path = f"cat_cooking_{slug}_part{i + 1}.mp4"
        if os.path.exists(part_path):
            print(f"[{i + 1}/{len(scenes)}] 既存ファイルを再利用します: {part_path}")
            clip_paths.append(part_path)
        else:
            clip_paths.append(
                generate_clip(client, prompt, i, len(scenes), part_path)
            )

    output_path = f"cat_cooking_{slug}.mp4"
    print("クリップを結合しています...")
    concat_clips(clip_paths, output_path)
    print(f"完成した動画を保存しました: {output_path}")


if __name__ == "__main__":
    main()

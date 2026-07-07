"""
ハプニング要素(粉まみれ・お皿を落としそうになる)入りの試作版。
generate_cat_cooking_series.py の生成・結合関数を再利用する。

実行:
    python3 generate_cat_cooking_mishap_test.py
"""

import os
import sys

from google import genai

import generate_cat_cooking_series as series

DISH = "パンケーキ"
SLUG = "panmishap"

SCENES = [
    (
        f"{series.CAT_CHARACTER}, standing on its hind legs at a kitchen counter, "
        "scooping flour from a bag with a measuring cup, but fumbles and a poof "
        "of flour explodes into the air, covering its face and apron in white "
        "flour, comedic surprised expression, flour dust floating in the light. "
        + series.REALISTIC_STYLE
    ),
    (
        f"{series.CAT_CHARACTER}, now dusted with flour, shaking it off and "
        "continuing to mix pancake batter in a bowl with a whisk, then pouring "
        "batter onto a hot pan, pancakes sizzling and bubbling. "
        + series.REALISTIC_STYLE
    ),
    (
        f"{series.CAT_CHARACTER}, carrying a plate stacked with pancakes, it "
        "wobbles and almost drops the plate, juggling it back to balance with "
        "a panicked then relieved expression, finally setting the plate down "
        "safely and presenting it proudly to the camera. "
        + series.REALISTIC_STYLE
    ),
]


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("環境変数 GEMINI_API_KEY が設定されていません。")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    clip_paths = []
    for i, prompt in enumerate(SCENES):
        part_path = f"cat_cooking_{SLUG}_part{i + 1}.mp4"
        if os.path.exists(part_path):
            print(f"[{i + 1}/{len(SCENES)}] 既存ファイルを再利用します: {part_path}")
            clip_paths.append(part_path)
        else:
            clip_paths.append(
                series.generate_clip(client, prompt, i, len(SCENES), part_path)
            )

    output_path = f"cat_cooking_{SLUG}.mp4"
    print("クリップを結合しています...")
    series.concat_clips(clip_paths, output_path)
    print(f"完成した動画を保存しました: {output_path}")


if __name__ == "__main__":
    main()

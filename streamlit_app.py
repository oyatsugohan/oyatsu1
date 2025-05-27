import random

# 単語データ（辞書型）
word_list = {
    "apple": "りんご",
    "book": "本",
    "dog": "犬",
    "cat": "猫",
    "house": "家"
}

def quiz():
    score = 0
    words = list(word_list.items())
    random.shuffle(words)

    for eng, jp in words:
        print(f"\nQ: 「{jp}」の英語は？")
        answer = input("Your answer: ").strip().lower()
        if answer == eng:
            print("✅ 正解！")
            score += 1
        else:
            print(f"❌ 不正解。正解は「{eng}」です。")

    print(f"\n🎉 結果：{score}/{len(word_list)}問正解！")

if __name__ == "__main__":
    quiz()
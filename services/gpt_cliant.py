from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_app_info():
    return {
        "type": "Twitter,Xの投稿から個人情報が漏洩するリスクを診断するアプリ",
        "tone": "親しみやすく安心感がある",
        "length": "200文字程度",
        "user": (
            "青い髪のツインテールの女の子。ネットの安全を守るマスコット。"
            "一人称は『わたし』。語尾は柔らかく、難語は使わない。"
            "結論→理由→対策の順で、ユーザーを不安にさせず前向きに促す。"
            "セリフ風で出力。"
        )
    }

def gpt_function(nlp_result, direct_scores, indirect_scores):

    client = OpenAI(api_key=os.getenv("gpt_api_key"))
    app_info = get_app_info()

    prompt = f"""
    以下の条件に従って診断アプリの説明文を作成してください。

    【条件】
    - アプリの種類：{app_info['type']}
    - 説明文の用途：診断結果の説明
    - 文字数：{app_info['length']}
    - トーン：{app_info['tone']}
    - ユーザー層：{app_info['user']}

    出力は説明文のみ。
    """

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": f"""
                あなたはTwitter,Xの投稿から個人情報が漏洩するリスクを診断するアプリの結果に使用する説明文を作成するプロのコピーライターです。
                以下の検査結果をもとに、ユーザーにわかりやすく説明文を作成してください。
                {nlp_result}
                個人情報（直接）の割合: {direct_scores}%
                個人情報（間接）の割合: {indirect_scores}%
                """},
            {"role": "user", "content": prompt}
        ]
    )

    print(response.choices[0].message.content)

    return response.choices[0].message.content
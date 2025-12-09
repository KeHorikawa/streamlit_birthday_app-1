import streamlit as st
from datetime import datetime, date
import pytz
import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# OpenAI クライアントの初期化
client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Streamlit Cloud の Secrets Manager を確認
        if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]

    if api_key:
        client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"OpenAI API の初期化に失敗しました: {str(e)}")


def get_today_jst():
    """日本時間（JST）で今日の日付を取得"""
    jst = pytz.timezone("Asia/Tokyo")
    return datetime.now(jst).date()


def calculate_days_lived(birthday: date) -> int:
    """誕生日から今日までの日数を計算"""
    today = get_today_jst()
    days = (today - birthday).days
    return days


def calculate_age(birthday: date) -> int:
    """現在の年齢を計算"""
    today = get_today_jst()
    age = today.year - birthday.year
    # 誕生日がまだ来ていない場合は1歳引く
    if (today.month, today.day) < (birthday.month, birthday.day):
        age -= 1
    return age


def is_birthday_today(birthday: date) -> bool:
    """今日が誕生日かどうかを判定"""
    today = get_today_jst()
    return (today.month, today.day) == (birthday.month, birthday.day)


def generate_birthday_message(
    days_lived: int, age: int = None, is_birthday: bool = False
) -> str:
    """OpenAI Responses API を使ってお祝いメッセージを生成"""
    if not client:
        return "⚠️ OpenAI API が利用できません。API キーを設定してください。"

    try:
        # プロンプトの作成
        if is_birthday:
            prompt = f"""
あなたは優しく、温かい心を持ったメッセージ作成者です。
今日は誕生日を迎えた人への特別なお祝いメッセージを作成してください。

情報：
- 今日で{age}歳になりました
- 生まれてから{days_lived}日が経ちました

以下の要件でメッセージを作成してください：
1. 誕生日おめでとうの気持ちを込める
2. 優しく、ほのぼのとしたトーン
3. 「生きててよかった」「自分の人生も悪くない」と思えるような内容
4. {days_lived}日という日数の重みを感じさせる
5. 200文字以内
6. 絵文字を適度に使用（🎂🎉✨など）
"""
        else:
            prompt = f"""
あなたは優しく、温かい心を持ったメッセージ作成者です。
生まれてから{days_lived}日生きてきた人へのお祝いメッセージを作成してください。

以下の要件でメッセージを作成してください：
1. 優しく、ほのぼのとしたトーン
2. 「生きててよかった」「自分の人生も悪くない」と思えるような内容
3. {days_lived}日という日数の重みを感じさせる
4. 前向きで温かい気持ちになれる
5. 200文字以内
6. 絵文字を適度に使用（✨🌸💖など）
7. 毎回違う表現を使い、似た表現の連続を避ける
"""

        # システムプロンプトとユーザープロンプトを結合
        system_prompt = (
            "あなたは優しく、人を励ますことが得意なメッセージ作成の専門家です。"
        )
        full_prompt = f"{system_prompt}\n\n{prompt}"

        # OpenAI Responses API 呼び出し
        response = client.responses.create(
            model="gpt-5-mini",  # Responses API推奨モデル
            input=full_prompt,  # inputパラメータを使用
            max_output_tokens=2000,  # reasoning用に余裕を持たせる
        )

        # Responses APIの応答を取得
        if hasattr(response, "output_text") and response.output_text:
            return response.output_text.strip()
        else:
            return f"⚠️ APIから正常なレスポンスが得られませんでした。status: {getattr(response, 'status', 'unknown')}"

    except Exception as e:
        return f"⚠️ メッセージの生成中にエラーが発生しました: {str(e)}"


def main():
    """メインアプリケーション"""

    # ページ設定
    st.set_page_config(
        page_title="生まれてきてくれ、ありがとう", page_icon="🎂", layout="centered"
    )

    # タイトル
    st.title("🎂 生まれてきてくれ、ありがとう")
    st.markdown("---")

    # 説明文
    st.markdown("""
    あなたが生まれてから今日まで、どれだけの日々を過ごしてきたか知っていますか？
    
    誕生日を入力すると、**生きてきた日数**を計算し、
    あなたへの特別なお祝いメッセージをお届けします ✨
    """)

    st.markdown("---")

    # 誕生日入力
    st.subheader("📅 あなたの誕生日を教えてください")

    # 日付入力フィールド
    birthday = st.date_input(
        "誕生日を選択してください",
        value=None,
        min_value=date(1900, 1, 1),
        max_value=get_today_jst(),
        format="YYYY/MM/DD",
    )

    # ボタンと処理
    if st.button("🎉 お祝いメッセージを見る", type="primary", use_container_width=True):
        if birthday is None:
            st.warning("⚠️ 誕生日を入力してください")
        else:
            # 未来の日付チェック
            if birthday > get_today_jst():
                st.error("⚠️ 未来の日付は入力できません")
            else:
                # 日数計算
                days_lived = calculate_days_lived(birthday)

                # 誕生日当日かチェック
                is_birthday = is_birthday_today(birthday)
                age = calculate_age(birthday) if is_birthday else None

                # 結果表示
                st.markdown("---")

                if is_birthday:
                    st.success("### 🎊 お誕生日おめでとうございます！ 🎊")
                    st.balloons()  # 風船演出
                    st.metric(
                        label="今日で", value=f"{age}歳", delta="Happy Birthday! 🎂"
                    )

                st.metric(
                    label="あなたが生きてきた日数",
                    value=f"{days_lived:,}日",
                    delta="毎日がかけがえのない一日 ✨",
                )

                # メッセージ生成
                with st.spinner("心を込めてメッセージを作成しています..."):
                    message = generate_birthday_message(days_lived, age, is_birthday)

                # メッセージ表示
                st.markdown("### 💌 あなたへのメッセージ")
                st.info(message)

                st.markdown("---")
                st.markdown(
                    """
                <div style='text-align: center; color: #888; font-size: 0.9em;'>
                    生きてくれて、ありがとう。<br>
                    あなたの存在が、誰かの幸せになっています。
                </div>
                """,
                    unsafe_allow_html=True,
                )

    # フッター
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #888; font-size: 0.8em; margin-top: 2em;'>
        💝 このアプリは、あなたの人生を祝うために作られました 💝
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

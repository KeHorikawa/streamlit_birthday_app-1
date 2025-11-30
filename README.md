# !製作中（まだ動きません）

# 🎂 生まれてきてくれ、ありがとう

あなたが生まれてから今日まで生きてきた日数を計算し、心温まるお祝いメッセージをお届けするStreamlitアプリです。

## ✨ 機能

- 📅 誕生日から今日までの日数を計算（日本時間基準）
- 🎊 誕生日当日は特別なお祝いメッセージと演出
- 💌 OpenAI GPT による優しくてほのぼのしたメッセージ生成
- 🌸 毎回違う表現でメッセージを作成

## 🚀 セットアップ方法

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd streamlit_birthday_app-1
```

### 2. 必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. OpenAI API キーの設定

#### ローカル環境の場合

プロジェクトルートに `.env` ファイルを作成し、以下を記述：

```
OPENAI_API_KEY=your_openai_api_key_here
```

**API キーの取得方法：**
1. [OpenAI Platform](https://platform.openai.com/api-keys) にアクセス
2. アカウント作成/ログイン
3. API Keys セクションで新しいキーを作成

#### Streamlit Cloud の場合

1. Streamlit Cloud のダッシュボードでアプリを選択
2. Settings → Secrets に移動
3. 以下の内容を追加：

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

### 4. アプリの起動

```bash
streamlit run main.py
```

ブラウザが自動的に開き、アプリが表示されます（通常は http://localhost:8501）

## 📖 使い方

1. アプリを開く
2. 誕生日を入力（YYYY/MM/DD形式）
3. 「🎉 お祝いメッセージを見る」ボタンをクリック
4. 生きてきた日数とお祝いメッセージが表示されます
5. 誕生日当日なら特別な演出も！🎊

## 🛠️ 技術スタック

- **フロントエンド/UI**: Streamlit
- **AI メッセージ生成**: OpenAI GPT-4 Turbo
- **日時処理**: pytz（日本時間対応）
- **環境変数管理**: python-dotenv

## 📋 要件

- Python 3.8 以上
- OpenAI API キー（有料）

## 🔒 セキュリティ

- API キーは `.env` ファイルまたは Streamlit Secrets で管理
- `.env` ファイルは `.gitignore` に含まれているため、Git にコミットされません

## 🌟 将来の拡張予定

- 誕生日の保存機能
- メッセージトーンの選択（元気系、落ち着き系など）
- メッセージ履歴の表示
- 多言語対応（英語、中国語など）

## 📝 詳細ドキュメント

詳しい要件定義は [requirements.md](Documents/requirements.md) を参照してください。

## 💝 コンセプト

このアプリは、使う人が

> 「生きててよかったな」  
> 「自分の人生も悪くないな」

と、少しでも幸せな気持ちになれることを目的として作られました。

---

生きてくれて、ありがとう。✨

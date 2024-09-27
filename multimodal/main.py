import boto3
import json
import base64

session = boto3.Session(profile_name="private", region_name="us-east-1")

# 実行するのはbedrockではなく、bedrock-runtime
bedrock_runtime = session.client("bedrock-runtime")

# バイナリ読み込みモードで開く rb: read binary
with open("./image.png", "rb") as f:
    # バイナリをbase64にエンコードする。この時点だと、base64のバイナリに変換されただけ
    b64 = base64.b64encode(f.read())
    # base64のバイナリをutf-8で文字列に変換する
    data = b64.decode("utf-8")


body = json.dumps(
    {
        "anthropic_version": "bedrock-2023-05-31",
        # 生成するトークンの上限
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "この画像は何か、日本語で説明してください",
                    },
                ],
            },
        ],
    }
)

modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"
# acceptヘッダは、こういう形式のデータを返してください、というリクエストヘッダ
accept = "application/json"
# contentTypeは、こういう形式のデータを返しますよ、というレスポンスヘッダ

response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept)
response_body = json.loads(response.get("body").read())
answer = response_body.get("content")[0].get("text")

print(answer)

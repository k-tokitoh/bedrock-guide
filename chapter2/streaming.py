import boto3
import json

session = boto3.Session(profile_name="private", region_name="us-east-1")

# 実行するのはbedrockではなく、bedrock-runtime
bedrock_runtime = session.client("bedrock-runtime")

body = json.dumps(
    {
        "anthropic_version": "bedrock-2023-05-31",
        # 生成するトークンの上限
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": "いろは歌を教えてください"}],
    }
)

modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"
# acceptヘッダは、こういう形式のデータを返してください、というリクエストヘッダ
accept = "application/json"
# contentTypeは、こういう形式のデータを返しますよ、というレスポンスヘッダ

# ストリームを返す専用のメソッドがある
response = bedrock_runtime.invoke_model_with_response_stream(
    body=body, modelId=modelId, accept=accept
)

for event in response.get("body"):
    # json.load()はファイルの読み込み、json.loads()は文字列の読み込み
    chunk = json.loads(event["chunk"]["bytes"])
    if (
        chunk["type"] == "content_block_delta"
        and chunk["delta"]["type"] == "text_delta"
    ):
        # endを指定しないと改行になってしまう
        print(chunk["delta"]["text"], end="")

# 最後に改行
print()

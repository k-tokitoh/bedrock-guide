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
        "messages": [{"role": "user", "content": "bedrockってどういう意味ですか？"}],
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

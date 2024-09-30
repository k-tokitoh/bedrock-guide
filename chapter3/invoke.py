from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.globals import set_debug

set_debug(True)

# テキストは1 input 1 output
# チャットはn input n output（最初にシステムプロンプトも与えられる）
# boto3を直接つかうのではなく、langchainが提供するwrapperを利用する
chat = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_kwargs={"max_tokens": 1000},
    region_name="us-east-1",
    credentials_profile_name="private",
)

messages = [
    SystemMessage(content="あなたのタスクはユーザーの質問に正確に回答することです。"),
    HumanMessage(content="空が青いのはなぜですか？"),
]

response = chat.invoke(messages)

print(response.content)

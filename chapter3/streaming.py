from gc import disable
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
    # たぶんだけど、streamingはinvokeしたときにstreamingで処理するかどうかを決めるもの。
    # streamingがどちらであれ、明示的にstream()を呼ぶとstreamingで処理される
    # defaultはFalse
    streaming=False,
    # disable_streamingがTrueだと、明示的にstream()を呼んだ場合にもstreamingで処理されない
    # defaultはFalse
    disable_streaming=False,
)

messages = [
    SystemMessage(content="あなたのタスクはユーザーの質問に正確に回答することです。"),
    HumanMessage(content="空が青いのはなぜですか？"),
]

# ここより前は同じ。invoke()をstream()に変更
for chunk in chat.stream(messages):
    # flushがFalseだと、バッファに一定以上溜まってから出力される
    # 実際、1行ずつくらいで出力された
    print(chunk.content, end="", flush=True)

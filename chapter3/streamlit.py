import streamlit as st
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from langchain.globals import set_debug

set_debug(False)


print("top")
# streamlitでは、inputやbutton押下などのユーザーアクションがあるたびにpython全体が再実行される
st.title("Chat with LangChain")
st.button("push me")

# テキストは1 input 1 output
# チャットはn input n output（最初にシステムプロンプトも与えられる）
# boto3を直接つかうのではなく、langchainが提供するwrapperを利用する
chat = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_kwargs={"max_tokens": 1000},
    region_name="us-east-1",
    credentials_profile_name="private",
)

# 変数は毎回初期化されるが、session_stateは再実行されても保持される
if "messages" not in st.session_state:
    messages: list[BaseMessage] = [
        SystemMessage(
            content="あなたのタスクはユーザーの質問に正確に回答することです。"
        ),
    ]
    st.session_state.messages = messages

print(st.session_state.messages)

# 前回までのやりとり全体を表示
for message in st.session_state.messages:
    if message.type != "system":
        with st.chat_message(message.type):
            st.markdown(message.content)


# chat_inputでUIが作成されるとともに、ユーザーの入力が戻り値となってpromptに代入される
# このブロックはinputが確定したときに1回だけ実行される
if prompt := st.chat_input("何でも聞いてください"):
    print("if")
    st.session_state.messages.append(HumanMessage(content=prompt))

    # chat_message()の引数によってアバターの表示が変わる
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 毎回、会話の履歴全体を送る、最後がuser promptだと、それに対する返答が返ってくる、ということらしい。
        response = st.write_stream(chat.stream(st.session_state.messages))

    st.session_state.messages.append(AIMessage(content=response))

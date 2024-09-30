from mailbox import Message
import streamlit as st
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain.globals import set_debug
from boto3 import Session

set_debug(False)


# streamlitでは、inputやbutton押下などのユーザーアクションがあるたびにpython全体が再実行される
st.title("Chat with LangChain")

if "session_id" not in st.session_state:
    st.session_state.session_id = "123"


# historyはdynamodbへの永続化も含む、会話の履歴
if "history" not in st.session_state:
    session = Session(profile_name="private", region_name="us-east-1")
    st.session_state.history = DynamoDBChatMessageHistory(
        table_name="BedrockChatSessionTable",
        session_id=st.session_state.session_id,
        boto3_session=session,
        # config={"region": "us-east-1"},
    )

# chainは、
if "chain" not in st.session_state:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたのタスクはユーザーの質問に正確に回答することです。"),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="human_message"),
        ]
    )

    chat = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_kwargs={"max_tokens": 1000},
        region_name="us-east-1",
        credentials_profile_name="private",
    )

    # promptをchatに渡すchainを定義する
    chain = prompt | chat
    # chainも毎回つくったら困るのでsession_stateに入れる
    st.session_state.chain = chain

if st.button("履歴クリア"):
    st.session_state.history.clear()


# 前回までのやりとり全体を表示
# 今回はsystemはhistoryに入れないので除外のためのifは必要なし
for message in st.session_state.history.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)


# chat_inputでUIが作成されるとともに、ユーザーの入力が戻り値となってpromptに代入される
# このブロックはinputが確定したときに1回だけ実行される
if prompt := st.chat_input("何でも聞いてください"):
    # chat_message()の引数によってアバターの表示が変わる
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 毎回、会話の履歴全体を送る、最後がuser promptだと、それに対する返答が返ってくる、ということらしい。
        response = st.write_stream(
            st.session_state.chain.stream(
                {
                    "messages": st.session_state.history.messages,
                    "human_message": [HumanMessage(content=prompt)],
                },
                # これが何のための指定なのかは不明。historyの管理はこれがなくても実現できている気がする。ログとかのためだろうか
                config={"configurable": {"session_id": st.session_state.session_id}},
            )
        )

    st.session_state.history.add_user_message(prompt)
    st.session_state.history.add_ai_message(response)

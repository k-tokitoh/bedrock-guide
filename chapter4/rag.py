import streamlit as st
from langchain_aws import ChatBedrock

# retrieverは文書を取得する？
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="AOEFQ9GT3G",
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 10}},
    # 型としてはclassインスタンスを求めるのでdictだとエラーになるよう。しかしclassをimportすることができない（理由は不明）
    # retrieval_config=RetrievalConfig(
    #     vectorSearchConfiguration=VectorSearchConfig(numberOfResults=10)
    # ),
    credentials_profile_name="private",
    region_name="us-east-1",
    min_score_confidence=None,
    client=None,
)

# promptはModelに渡す入力
# from_template() は引数に文字列を受け取る（f-stringじゃないし、jinjaでもないのかな）
prompt = ChatPromptTemplate.from_template(
    # 文字列ではなくて、retrieverみたいなobjectを入れ込むことができるのか
    "以下のcontextに基づいて回答してください: {context} / 質問: {question}"
)

model = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_kwargs={"max_tokens": 1000},
    credentials_profile_name="private",
    region_name="us-east-1",
)

chain = (
    # 変数をdict形式でpromptに渡す
    # questionはさらに上流の入力をそのまま流用するため、RunnablePassthrough
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

st.title("おしえてwedding")
question = st.text_input("質問を入力")
button = st.button("質問する")

# ボタンが押下されたら
if button:
    st.write(chain.invoke(question))

from typing import List

# langchain の代わりに langchain-community (および必要に応じて関連パッケージ) を使用
# 注意: 以下のコードは、langchain-community とその関連パッケージが
# langchain と同様のモジュールやクラスを提供していることを前提としています。
# 実際のコードを更新する前に、適切なパッケージ名とクラス名を確認してください。

# from langchain.agents import AgentType, initialize_agent
# 上記の代わりに、langchain-community またはその他の関連パッケージから適切なモジュールをインポート
# 以下は仮のコードであり、実際のパッケージ構造に基づいて適切に更新する必要があります。
import langchain
from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits import VectorStoreInfo, VectorStoreToolkit
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.tools import BaseTool
# Before
# from langchain_community.embeddings.openai import OpenAIEmbeddings

# After



langchain.verbose = True


def create_index() -> VectorStoreIndexWrapper:
    loader = DirectoryLoader("./src/", glob="**/*.py")
    return VectorstoreIndexCreator().from_loaders([loader])


def create_tools(index: VectorStoreIndexWrapper, llm) -> List[BaseTool]:
    vectorstore_info = VectorStoreInfo(
        vectorstore=index.vectorstore,
        name="udemy-langchain source code",
        description="Source code of application named udemy-langchain",
    )
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info, llm=llm)
    return toolkit.get_tools()


def chat(
    message: str, history: ChatMessageHistory, index: VectorStoreIndexWrapper
) -> str:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    tools = create_tools(index, llm)

    memory = ConversationBufferMemory(
        chat_memory=history, memory_key="chat_history", return_messages=True
    )

    agent_chain = initialize_agent(
        tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory
    )

    return agent_chain.run(input=message)

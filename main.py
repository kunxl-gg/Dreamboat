from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationalRetrievalChain

# LLM
llm = OpenAI()

# Document loader
loader = TextLoader('./state_of_the_union.txt', encoding="utf-8")
data = loader.load()

# Text splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
all_splits = splitter.split_documents(data)

# Vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings)
retriever = vectorstore.as_retriever()

# Memory
memory = ConversationSummaryMemory(llm=llm, return_messages=True, memory_key="chat_history")

# Prompt
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot having a conversation with a human."
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

# final Chain
chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

while True:
    question = input("Ask a question: ")
    if(question == "quit"):
        break
    response = chain(question)
    print(response["answer"])



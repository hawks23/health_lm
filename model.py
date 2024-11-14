import os
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

llm = ChatGroq(temperature=0, model="llama-3.1-70b-versatile")

search_tool = TavilySearchResults(search_depth="basic", max_results=3)
tools = [search_tool]
memory = ConversationBufferWindowMemory(memory_key="chat_history",return_messages=True,k=3, output_key="output")
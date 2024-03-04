import streamlit as st
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings 
from llama_index.core import load_index_from_storage
import os
from huggingface_hub import login
HF_TOKEN = "Enter Your HF_TOKEN here"
login(token=HF_TOKEN)

PERSIST_DIR = "./db"


llm = HuggingFaceInferenceAPI(model_name = "HuggingFaceH4/zephyr-7b-alpha", api_key = HF_TOKEN)
embed_model = LangchainEmbedding(HuggingFaceInferenceAPIEmbeddings(model_name="thenlper/gte-large", api_key=HF_TOKEN))



if not os.path.exists(PERSIST_DIR):
    #Create the new index
    document = SimpleDirectoryReader("PDF").load_data() 
    #parse docs into node
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(document)
    #service context    
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model, chunk_size=1024)
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex(nodes, service_context=service_context, storage_context=storage_context)
    index.storage_context.persist(persist_dir=PERSIST_DIR)   
else:
    #Load index
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model, chunk_size=1024)
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(service_context=service_context, storage_context=storage_context)

#Query Engine
#user_prompt = "Give some Examples of Agriculture"
query_engine = index.as_query_engine()







st.title("Syllabus ChatBOT")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your questions about Regulation or Syllabus of AI&DS and CSE R2017 "):
    st.session_state["messages"].append({"role":"user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    #print(st.session_state["messages"])
    #print(chat_input)
    with st.chat_message("assistant"):
        response = query_engine.query(prompt)
        message = response
        st.markdown(message)
        st.session_state["messages"].append({"role":"assistant", "content":message})
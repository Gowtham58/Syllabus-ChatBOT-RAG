# Syllabus-ChatBOT-RAG
## Description
A ChatBOT that can answer any questions related to the Anna University Regulation - 2017 and Syllabus of the Departments of CSE and AI&DS.

## Working
The App uses a Large Language Model and an Embedding model. This is accomplished using the Retrieval Augmented Generation (RAG) method. The PDF is first converted to vector embeddings where similar details are grouped together and stored in a vector store. This is done using a Embedding Model from HugginFace **thenlper/gte-large** which creates the embeddings through HuggingFace Inference API. 
Then we use a LLM model - **HuggingFaceH4/zephyr-7b-alpha** that can through the same HugginFace Inference API. It will get the prompt and outputs the relevant information to the user through the web app.
The Web App is build using StreamLit. It has a Simple UI that can be used by anyone.

## TechStack
- llama_index
- Streamlit
- HuggingFace Inference API
- Langchain
## To Run the Application Locally
- Clone the Repository
- Replace your HuggingFace token in chat_app.py
- run using ```streamlit run chat_app.py```
- You can also replace the PDFs with you own PDFs and ask questions from it.

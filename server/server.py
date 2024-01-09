from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chains import RetrievalQA
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_community.document_loaders import JSONLoader
import warnings
import json
from datetime import datetime
import os

                
warnings.filterwarnings("ignore", category=DeprecationWarning)
app = Flask(__name__)
CORS(app)

loader = JSONLoader(file_path='history.json',jq_schema='.',text_content=False)
data = loader.load()
vectorstore = Chroma.from_documents(documents=data, embedding=GPT4AllEmbeddings())

llm = Ollama(model="ava-3.1", callbacks=([StreamingStdOutCallbackHandler()]))

qa = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), chain_type="stuff", callbacks=([StreamingStdOutCallbackHandler()]))

@app.route('/api/query', methods=['POST'])
def query():
    query = request.json.get("query")
    
    # with open("history.json", 'r') as file:
    #     jsonFile = json.load(file)
    # jsonFile["messages"].append({
    #     "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     "User": "Kishore",
    #     "Content": query
    # })
    # with open("history.json", 'w') as file:
    #     json.dump(jsonFile, file, indent=2)

    res = qa("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"+ query)
    answer = res['result']
    
    # jsonFile["messages"].append({
    #     "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     "User": "Ava",
    #     "Content": answer
    # })
    # with open("history.json", 'w') as file:
    #     json.dump(jsonFile, file, indent=2)
    return jsonify({"result": answer})  #POST

if __name__ == '__main__':
    app.run(debug=True, port=8080)
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
import uuid
                
warnings.filterwarnings("ignore", category=DeprecationWarning)
app = Flask(__name__)
CORS(app)

llm = Ollama(model="ava-3.1", callbacks=([StreamingStdOutCallbackHandler()]))

@app.route('/api/query', methods=['POST'])
def query():
    loader = JSONLoader(file_path='../assets/history.json',jq_schema='.',text_content=False)
    data = loader.load()
    vectorstore = Chroma.from_documents(documents=data, embedding=GPT4AllEmbeddings())
    qa = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), chain_type="stuff", callbacks=([StreamingStdOutCallbackHandler()]))
    
    sessionId = request.json.get("sessionID")
    query = request.json.get("query")

    with open("../assets/history.json", 'r') as file:
        jsonFile = json.load(file)

    if sessionId == "NEWCHAT":
        sessionId = uuid.uuid4()
        jsonFile["sessions"].append({
                "sessionID": sessionId,
                "messages": [],
            })
    
    for session in jsonFile['sessions']:
        if session['sessionID'] == sessionId:
            session["messages"].append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "User": "Kishore",
                "Content": query
            })
        
    with open("../assets/history.json", 'w') as file:
        json.dump(jsonFile, file, indent=2)

    res = qa("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"+ query)
    answer = res['result']
    
    for session in jsonFile['sessions']:
        if session['sessionID'] == sessionId:
            session["messages"].append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "User": "Ava",
                "Content": answer
            })
    
    with open("../assets/history.json", 'w') as file:
        json.dump(jsonFile, file, indent=2)
    
    return jsonify({"result": answer, "sessionID": sessionId})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
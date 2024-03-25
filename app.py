import os
from flask import Flask, request, jsonify, render_template_string
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

app = Flask(__name__)

HUGGINGFACEHUB_API_TOKEN = "YOUR_API_TOKEN"

def set_custom_prompt():
    template = """
    Use the following pieces of context to answer the question at the end. If the context is relevant and provides enough information, provide a clear, creative, and informative answer based on the context.
    If the context is empty or does not provide enough information to answer the question, simply say "I'm sorry, I don't have enough information related to {question} in my knowledge base."
    Use complete sentences and keep the answer concise yet thorough.
    Avoid repetition and aim for a natural, conversational tone.
    {context}
    Question: {question}
    Helpful Answer:"""
    return PromptTemplate(template=template, input_variables=["context", "question"])

def load_model():
    repo_id = "tiiuae/falcon-7b-instruct"
    llm = HuggingFaceEndpoint(
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        repo_id=repo_id,
        temperature=0.7
    )
    return llm

def create_retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_type="similarity",search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa_chain

def create_retrieval_qa_bot():
    persist_dir = "./dbase"
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

    llm = load_model()
    qa_prompt = set_custom_prompt()
    qa = create_retrieval_qa_chain(llm=llm, prompt=qa_prompt, db=db)

    return qa

QA_CHAIN = create_retrieval_qa_bot()


@app.route('/')
def home():
    return render_template_string("""
    <!doctype html>
    <html>
    <head>
        <title>QA Bot</title>
        <style>
            body{
                background-color: #222831;
                color: white;
                font-family: Verdana, Geneva, Tahoma, sans-serif;
            }
            .heading{
                background-color:#31363F;
                margin-top: -49px;
                margin-left: -5px;
                margin-right: -5px;
                text-align: center;
                margin-bottom: 15px;
            }
            .qa{
                font-size: 50px;
                font-weight: 500;
            }
            .clr{
                background-color:#80669d;
                color:white;
                float: right;
                border: 10px solid #80669d;
                border-radius: 8px;
                margin-top: -102px;
                margin-right: 88px;
                font-size: 15px;
                cursor:pointer
                
            }
            .clr:hover
            {
                background-color: #a881af;
                border-radius: 8px;
                border:10px solid #a881af;
                cursor:pointer
            }
            #chatbox {
                height: 455px;
                overflow-y: scroll;
                padding: 10px;
                margin-bottom: 10px;
                margin-left: 75px;
                margin-right: 75px;
                color: white;
                font-size: 15px;
                margin-top:20px;
            }

            #userInput {
                width: 80%;
                padding: 10px;
                box-sizing: border-box;
                margin-left: 75px;
                margin-right: 75px;
                background-color: #31363F;
                color:white;
                font-size: 15px;
                margin-top: 30px;
                margin-bottom:15px
            }
            .submit{
                background-color:#80669d;
                color:white;
                float: right;
                border: 12px solid #80669d;
                border-radius: 8px;
                margin-top: -81px;
                margin-right: 62px;
                font-size: 17px;
                cursor:pointer
            }
            .submit:hover
            {
                background-color: #a881af;
                border-radius: 8px;
                border:12px solid #a881af;
                cursor:pointer
            }

            .javabot{
                border:1px solid white;
                margin-left: 100px;
                margin-right: 100px;
                margin-bottom:-50px;
                margin-top:-15px;
            }
            .chats{
                                  
            }
        </style>
    </head>
    <body>
        <div class="heading"> 
            <p class="qa" >JAVA QA Bot </p><button class="clr"  onclick="clearHistory()">CLEAR HISTORY</button> 
            </div>
        <div class="javabot">
        <div id="chatbox">
        </div>
        <div class="chats">
        <textarea id="userInput" rows="4" placeholder="Enter your question here..."></textarea>
        <button class="submit" onclick="sendQuestion()">SUBMIT</button>
        </div>
        </div>
        <script>
            function sendQuestion() {
                var userInput = document.getElementById('userInput');
                var chatbox = document.getElementById('chatbox');
                var question = userInput.value;
                userInput.value = ''; // clear the input after sending

                chatbox.innerHTML += "<div style='margin-top: 5px;'>User: " + question + "</div>";

                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({query: question})
                })
                .then(response => response.json())
                .then(data => {
                    chatbox.innerHTML += "<div style='margin-top: 5px;'>Bot: " + data.answer + "</div>";
                    chatbox.scrollTop = chatbox.scrollHeight; // scroll to the bottom
                })
                .catch((error) => {
                    console.error('Error:', error);
                    chatbox.innerHTML += "<div style='margin-top: 5px;'>Error: " + error + "</div>";
                });
            }
            function clearHistory() {
            var chatbox = document.getElementById('chatbox');
            chatbox.innerHTML = ''; // clear the chatbox
        }
        </script>
    </body>
    </html>
    
    """)

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    if not query:
        return jsonify({"error": "No query provided"}), 400
    try:
        response = QA_CHAIN({"query": query})
        return jsonify({"answer": response['result'] if 'result' in response else "No answer found"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()


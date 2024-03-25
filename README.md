# QA Chatbot Using Retrieval-Based Approach

![Screenshot (60)](https://github.com/sai-annadi/FAQ-Chatbot-Using-Retrieval-Based-Approach/assets/111168434/2967605f-6166-40ea-a6e9-75bc0f8c8b10)

![Screenshot (57)](https://github.com/sai-annadi/FAQ-Chatbot-Using-Retrieval-Based-Approach/assets/111168434/040e0ea0-f2d2-4e45-afc9-3475b5f83211)


### Description:

This GitHub repository contains the source code for a QA Chatbot Using Retrieval-Based Approach is an intelligent system designed to provide accurate and contextually relevant answers to user queries. Leveraging a Chroma vector database for efficient document retrieval and Hugging Face's Falcon 7B Instruct model for response generation, the chatbot ensures that users receive informative answers tailored to their questions. The chatbot's intuitive interface allows users to interact seamlessly, making it a valuable tool for research, learning, and information retrieval.

Built on Flask, the chatbot offers a user-friendly experience, with a clear focus on providing accurate and insightful responses. By combining document retrieval with response generation techniques, the chatbot is able to understand the context of user queries and provide answers that are both accurate and relevant.

![Screenshot (59)](https://github.com/sai-annadi/FAQ-Chatbot-Using-Retrieval-Based-Approach/assets/111168434/b4bc0150-9e2b-4e81-ba30-2ec93f0ca970)

### Key Components:

Chroma Vector Database: The chatbot uses a Chroma vector database for storing and retrieving documents based on user queries.

Hugging Face's Falcon 7B Instruct Model: The chatbot integrates with the Falcon 7B Instruct model for generating responses based on the retrieved documents.

Flask Application: The main application is built using Flask, providing a web-based interface for users to interact with the chatbot.

Prompt Template: A prompt template is used to structure user queries and generate appropriate responses based on the context.

RetrievalQA Chain: This component manages the interaction between the prompt template and the Falcon 7B Instruct model, handling the generation of responses.

### Features:
1.Interactive Chat Interface: Users can enter their questions in the chat interface and receive accurate answers based on the retrieval-based approach.
2.Contextual Understanding: The chatbot uses a combination of document retrieval and response generation techniques to provide contextually relevant answers.
3.Clear Chat History: Users have the option to clear the chat history using a dedicated button in the interface.
4.Getting Started

### Prerequisites:
Python 3.7 or later
pip (package installer for Python)

### Installation:

1.Clone the repository:

```bash
git clone https://github.com/your_username/qa-chatbot.git
```
2.Navigate to the project directory:
```bash
cd qa-chatbot
```
### Usage:
1.set up a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```
2.Install the required dependencies:
```bash
pip install -r requirements.txt
```
3.Initialize the Chroma vector database by running data.py:
```bash
python data.py
```
4.Start the Flask application (main bot) by running main.py:
```bash
python main.py
```
5.Access the chatbot interface by opening a web browser and navigating to http://localhost:5000/. You can now interact with the chatbot by entering questions in the input field and receiving answers based on the retrieval-based approach.


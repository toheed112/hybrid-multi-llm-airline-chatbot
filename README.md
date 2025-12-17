# Hybrid Multi-LLM Airline Customer Support Chatbot

A hybrid multi-LLM airline customer support chatbot that combines **local large language models (LLMs)** with **cloud-based embeddings** and **Retrieval-Augmented Generation (RAG)** to deliver **cost-efficient, intelligent, and scalable AI assistance**.

The system is capable of handling airline-related customer queries such as flight search, hotel recommendations, car rentals, excursions, and policy-based FAQs through a modular, tool-driven workflow.

---

## 🚀 Key Features

### Hybrid Multi-LLM Architecture
- Local inference using **Ollama + DeepSeek**
- Cloud-based **OpenAI embeddings** for semantic search

### Retrieval-Augmented Generation (RAG)
- Policy and FAQ retrieval using **FAISS vector indexing**

### Tool-Oriented Workflow
- Dedicated tools for flights, hotels, cars, excursions, and policy queries

### LangChain & LangGraph Orchestration
- Structured decision-based workflow management

### Interactive Streamlit Interface
- Simple, clean, and responsive chat UI

### Cost-Efficient Design
- Minimizes API usage by prioritizing local LLM execution

---

## 🧠 System Architecture Overview

The chatbot follows a modular processing pipeline:

1. User interacts via the **Streamlit UI**
2. Query is sent to the **workflow engine**
3. Intent classification is performed (policy, travel data, or general chat)
4. Relevant tools or RAG pipeline are executed
5. Final response is generated using a local LLM
6. Response is displayed to the user

---

## 🖥️ Screenshots

### Chat Interface
<!-- Drag<img width="1919" height="1020" alt="Screenshot 2025-12-17 234112" src="https://github.com/user-attachments/assets/2e11b58c-42ad-4241-a781-692a1228fcff" />
 & drop chat UI screenshot here -->

### Example Response
<!-- Drag & d<img width="1911" height="966" alt="Screenshot 2025-11-26 210051" src="https://github.com/user-attachments/assets/925dbf58-304d-4e95-a303-39ed147f6e32" />
rop example response screenshot here -->
<img width="1918" height="1013" alt="Screenshot 2025-12-11 020030" src="https://github.com/user-attachments/assets/bf978730-5827-4381-bc88-edf224c4c34d" />
<img width="1917" height="1018" alt="Screenshot 2025-12-11 034647" src="https://github.com/user-attachments/assets/ad8498a7-deaf-4b0b-85c7-9c68474168a5" />
<img width="1908" height="1007" alt="Screenshot 2025-12-11 035218" src="https://github.com/user-attachments/assets/0705cc0d-ae23-4b5a-8692-db99543a05a8" />
<img width="1915" height="1074" alt="Screenshot 2025-12-11 040755" src="https://github.com/user-attachments/assets/25755c90-da4d-42ca-9888-7b7621e8a2d9" />
<img width="1483" height="756" alt="Screenshot 2025-12-11 013922" src="https://github.com/user-attachments/assets/97a09433-249f-4a6a-be50-cd47bda4ccee" />

---

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **LLMs:** DeepSeek (via Ollama)
- **Embeddings:** OpenAI Embeddings
- **Frameworks:** LangChain, LangGraph
- **Vector Store:** FAISS
- **Database:** SQLite
- **Version Control:** Git & GitHub

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/toheed112/hybrid-multi-llm-airline-chatbot.git
cd hybrid-multi-llm-airline-chatbot
## ⚙️ Installation & Setup

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file (not committed to GitHub):

env
Copy code
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
▶️ Running the Application
Start the Ollama server:

bash
Copy code
ollama serve
Run the chatbot:

bash
Copy code
streamlit run frontend/app.py
Open the provided localhost URL in your browser.

📊 Example Use Cases
Airline policy and baggage queries

Flight search between airports

Hotel and car rental recommendations

Excursion and travel activity suggestions

General airline customer support queries

🔮 Future Enhancements
Most important enhance and try to update code to call tools by open ai because deepseek is sometime incapable and let deepseek generate resposne after the tool calling it would cost you cheap in cents from open ai api
And more important if you have powerful gpu still recommend dont use your own machine instead rent a cloud gpu would be more better  like i am thinking currently to rent on renpost service

User authentication and profiles

Multi-language support

Real-time flight status APIs

Cloud and Docker-based deployment

Conversation analytics and logging

📜 License
This project is licensed under the MIT License.

👨‍💻 Author
Toheed Mehmood
GitHub: https://github.com/toheed112

markdown
Copy code



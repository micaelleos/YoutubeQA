# **YoutubeQA**  

This repository contains the code for a question-and-answer (QA) bot for YouTube videos, built using Python, Streamlit, LangGraph, and Chroma. The bot allows users to ask questions related to YouTube videos and receive accurate answers based on the video content.  

---

## **Features**  

- **Automatic Video Analysis:** Extracts textual content from YouTube videos.  
- **Intelligent Responses:** Uses LangGraph to process and answer questions about videos.  
- **User-Friendly Interface:** Simple and interactive UI developed with Streamlit.  
- **Data Management:** Uses Chroma for efficient data storage and retrieval.  

---

## **Technologies Used**  

- **[Python](https://www.python.org/):** Main programming language.  
- **[Streamlit](https://streamlit.io/):** Framework for building interactive web applications.  
- **[LangGraph](https://github.com/langgraph/langgraph):** Tool for creating and managing language processing workflows.  
- **[Chroma](https://www.trychroma.com/):** Platform for vector storage and data retrieval.  

---

## **Requirements**  

Make sure you have the following installed on your environment:  

- Python 3.8 or higher  
- Pip (Python package manager)  

---

## **Installation**  

1. Clone this repository:  

   ```bash
   git clone https://github.com/micaelleos/YoutubeQA.git
   cd YoutubeQA
   ```  

2. Install the required dependencies:  

   ```bash
   pip install -r requirements.txt
   ```  

3. Set up the required environment variables (such as API keys for YouTube, LangGraph, and Chroma):  

   ```bash
   export OPEN_API_KEY="your_api_key_here"
   ```  

4. Run the Streamlit application:  

   ```bash
   streamlit run app.py
   ```  

5. Access the application in your browser at: [http://localhost:8501](http://localhost:8501)  

---

## **How to Use**  

1. Paste a YouTube video URL into the input field.  
2. Wait for the content extraction and indexing process.  
3. Enter your questions in the appropriate field.  
4. Receive answers based on the video content.  

---

## **Project Structure**  

```
├── main.py             # Main Streamlit application file
├── README.md           # Project documentation
├── prompt.py
├── requirements.txt
├── tools.py
└── youtubeqa.py
```  

---

## **Contributions**  

Contributions are welcome! Follow the steps below to contribute:  

1. Fork this repository.  
2. Create a branch for your feature or bug fix:  

   ```bash
   git checkout -b my-new-feature
   ```  

3. Commit your changes:  

   ```bash
   git commit -m "Add new feature"
   ```  

4. Push to GitHub:  

   ```bash
   git push origin my-new-feature
   ```  

5. Open a Pull Request.  

---

## **License**  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.  

---

Developed by **Micaelle Souza**.  

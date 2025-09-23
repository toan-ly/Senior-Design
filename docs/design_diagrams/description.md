# Design Diagram Descriptions

## D0
This diagram covers the high-level features our chatbot web application will support. End users can send messages typed into the chatbot and view chatbot options to modify their experience (delete history, edit message, etc.). The mental chatbot will then output responses to any messages received, offer suggestions based on how it has analyzed the user's mood, and provide visual health charts/trends for the user to track their progress.

Users can also input personal notes into a journal to look back on their progress or reflect on their experience by inserting comments. Users are also capable of interacting with the system interface to submit questions for system users/administrators if they require help understanding certain features or wish to leave feedback. They can modify their account information from this system interface as well. System users are capable of responding to end user questions and query the system to retrieve system statuses as well as the current number of active users.

![D0](D0.drawio.svg)


## D1
In this diagram, we break the chatbot into major sub-components. The Web UI handles conversation via chat window and user status (profile/health checkins). Then the agent will route the user input to the right components, call the right tools, integrate LLM, database, and RAG retrieval. The LLM will generate empathetic replies. RAG Documents will store provided mental related docs as embeddings and support search retrieval. Database will store user information, chat logs (histories), and mood time series. Finally, the analytics component will convert those into trends, scores, and charts for the user and evaluation metrics for system admins.

![D1](D1.svg)


## D2
In this diagram, we'll take a look inside the Agent Component. It will load prior chat histories from the Database in order to continue the conversation, then fetch relevant documents, and prepare the structured request to the LLM. Some of the tools the Agent can access are Query Engine and Progress Tracker. Query Engine will first search the index in vector storage using the user's question, then select the most relevant nodes (small chunks of text or knowledge). This step prepares the best possible context for answering each user question. The selected nodes are then combined and passed into the LLM. The Progress Tracker will store scores and mood check-ins into the Database for long term analytics. 

The RAG pipeline component receives unprocessed/raw documents and executes the following preprocessing steps: 
1. Split longer texts into chunks via the Token Splitter
2. Generate a brief summary of the metadata
3. Embed the chunked text and metadata summary into vectors
   
Structured chunks of knowledge (nodes) are then stored in the database to allow the system to quickly find semantically similar context to a user's query. Most frequently used nodes are stored in a cache for fast retrieval, reducing computation time and increasing overall efficiency.

![D2](D2.svg)

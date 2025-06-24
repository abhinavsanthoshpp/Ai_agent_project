# My Personal AI Assistant Prototype

## Project Overview
This project involves building an intelligent AI agent capable of understanding natural language, making decisions, and performing tasks autonomously. [cite_start]Developed as part of the Accelerate Career Accelerator Program, this prototype functions as a personal digital assistant, designed to help users accomplish their goals through conversational interactions. 

[cite_start]Unlike simple chatbots, this AI agent is designed to perceive user input, reason about information, act to achieve specific goals, learn over time (in principle, through user preferences), and communicate naturally. 

## Key Features

* **Natural Language Understanding (NLU):**
    * [cite_start]**Intent Recognition:** Identifies the user's goal (e.g., "get weather," "schedule meeting," "greet") using keyword-based matching with `spaCy`. 
    * [cite_start]**Entity Extraction:** Pulls out crucial information (like city names, dates, times) from user queries using `spaCy`'s Named Entity Recognition (NER). 
    * [cite_start]**Context Management:** Maintains conversation state and history, allowing for multi-turn interactions (e.g., asking for a city after a general weather request, or collecting date/time for scheduling). 

* **Knowledge Base & Memory System:**
    * [cite_start]**Static Knowledge:** Contains predefined facts and responses the agent knows about itself and its capabilities. 
    * [cite_start]**Persistent User Preferences:** Stores user-specific data (e.g., a preferred weather city) in a local JSON file, allowing the agent to remember information across different runs. 

* **Action & Integration Layer:**
    * [cite_start]**External API Connection:** Integrates with the OpenWeatherMap API to fetch real-time weather information for specified cities. 
    * [cite_start]**Task Execution:** Performs actions based on user requests (e.g., retrieves weather, simulates meeting scheduling). 
    * [cite_start]**Error Handling:** Implements basic error management for API failures and unexpected situations. 

* **Decision-Making & User Experience:**
    * [cite_start]**Rule-Based Logic:** Uses `if-elif-else` structures to make decisions based on recognized intents and extracted entities. 
    * [cite_start]**Basic Confidence Scoring:** Provides more nuanced responses when the agent is uncertain about user input. 
    * [cite_start]**Conversation Flow Design:** Manages natural transitions, clarifies missing information, and asks for user confirmation for actions. 
    * [cite_start]**User Guidance & Onboarding:** Provides a structured welcome for new users and offers "help" to guide interactions. 

## Technologies Used

* **Python:** The core programming language for the agent's logic.
* **`spaCy`:** A powerful library for Natural Language Processing (NLP), used for tokenization, intent recognition, and named entity extraction.
* **`requests`:** A Python library for making HTTP requests to external APIs (like OpenWeatherMap).
* **`json`:** Used for handling structured data, specifically for persistent storage of user preferences.
* **`datetime`:** For retrieving current year information.
* **`random`:** For providing varied greetings and responses.

## How to Run the Agent

Follow these steps to set up and run the AI Assistant on your local machine.

### Prerequisites

* Python 3.7+ installed on your system.
* `pip` (Python package installer), usually comes with Python.
* An active internet connection for the weather API.

### Setup Instructions

1.  **Clone the Repository (or navigate to your project folder):**
    If you're setting this up on a new machine, you would clone it:
    ```bash
    git clone [https://github.com/abhinavsanthoshpp/Ai_agent_project.git](https://github.com/abhinavsanthoshpp/Ai_agent_project.git)
    cd Ai_agent_project
    ```
    If you already have your local project folder, just open your terminal in that directory.

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install Required Libraries:**
    With your virtual environment activated, install the necessary Python packages:
    ```bash
    pip install spacy requests
    ```

4.  **Download the spaCy Language Model:**
    Your agent needs a specific English language model for NLP.
    ```bash
    python -m spacy download en_core_web_sm
    ```

5.  **Obtain an OpenWeatherMap API Key:**
    * Go to [https://openweathermap.org/api](https://openweathermap.org/api).
    * Sign up for a free account.
    * Navigate to your "API keys" tab (`https://home.openweathermap.org/api_keys`) after logging in.
    * Copy your default API key. **Note:** It can take up to 10-15 minutes (sometimes longer) for a new API key to become active.

6.  **Configure Your API Key:**
    * Open the `agent.py` file in your code editor (e.g., VS Code).
    * Find the line:
        ```python
        OPENWEATHERMAP_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY" # Replace this!
        ```
    * **Replace `"YOUR_OPENWEATHERMAP_API_KEY"` with the actual API key you copied from OpenWeatherMap, ensuring it remains inside the double quotes.**
        Example: `OPENWEATHERMAP_API_KEY = "2f63df4ee626ff5667b0f2939c3c33ee"`

### Running the Agent

1.  **Ensure your virtual environment is active.**
2.  **Run the Python script:**
    ```bash
    python agent.py
    ```
3.  The agent will start in your terminal, greet you, and prompt for input.

## How to Interact with the Agent (Examples)

Try these commands to see your AI Assistant in action:

* **Greetings:**
    * `Hello`
    * `Hi there!`
* **About the Agent:**
    * `Who are you?`
    * `What can you do?`
    * `What year is it?`
* **Weather Information:**
    * `What's the weather in London?`
    * `Tell me the forecast for Delhi.`
    * `Weather in New York.`
    * `What's the weather?` (If no city is given, it will ask for one or use your preferred city).
* **Set Preferred City (Persistent Memory):**
    * `Set my city to Paris.`
    * `Remember my city as Tokyo.`
    * (After setting, try `What's the weather?` and then restart the script and try `What's the weather?` again to see persistence!)
* **Scheduling (Mock):**
    * `Schedule a meeting.` (Multi-turn example)
    * `Schedule an appointment for tomorrow at 3 PM.` (Single-turn example)
    * (After it asks for confirmation, try `Yes` or `No`).
* **Getting Help:**
    * `help`
    * `Guide me`
* **Ending Conversation:**
    * `bye`
    * `exit`
    * `goodbye`

## Limitations & Future Enhancements

This prototype demonstrates fundamental AI agent capabilities, but there's always room for growth!

### Current Limitations

* **Keyword-based Intent Recognition:** The current intent recognition relies on simple keyword matching. This can be rigid and prone to misinterpretations if the user's phrasing doesn't contain the exact keywords.
* **Limited Entity Types:** Entity extraction is currently focused on cities, dates, and times. More complex entities or custom entities are not handled.
* **Mock Scheduling:** The scheduling feature is a simulation; it does not integrate with real calendar services (e.g., Google Calendar, Outlook Calendar).
* **Basic Memory:** Persistent memory is limited to a single preferred weather city.
* **No Machine Learning Training:** The agent's "learning" is currently limited to remembering preferences; it doesn't improve its NLP or decision-making through training data over time.

### Future Enhancements

* **Advanced NLU:** Integrate more sophisticated Natural Language Understanding models (e.g., using libraries like Rasa, or fine-tuning pre-trained models from Hugging Face Transformers) for more accurate and flexible intent recognition and entity extraction.
* **Real Calendar Integration:** Connect the scheduling feature to actual calendar APIs (like Google Calendar API) to create, modify, and manage events.
* **More Comprehensive Persistent Memory:** Store a wider range of user preferences, historical interactions, or frequently asked questions to provide a more personalized experience.
* **New Capabilities:** Expand the agent's functionality to include:
    * Reminders and Alarms
    * News summaries (integrating with news APIs)
    * Basic task list management
    * Simple factual question answering (by connecting to knowledge graph APIs or internal databases)
* **Multi-Modal Interaction:** Add voice input/output capabilities using Python's speech recognition and text-to-speech libraries.
* **Error Recovery Strategies:** Implement more robust ways to guide the user when inputs are unclear or external services fail.
* **User Interface:** Develop a simple web-based (using Flask/FastAPI) or GUI interface instead of just the command line.

## Acknowledgements
This project was developed as part of the Accelerate Career Accelerator Program. [cite_start]The learning guide provided a structured approach to building foundational AI agent concepts.

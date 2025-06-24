import spacy
import datetime
import requests
import random
import json

OPENWEATHERMAP_API_KEY = "2f63df4ee626ff5667b0f2939c3c33ee" # YOUR API KEY
BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
USER_DATA_FILE = "user_data.json"

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm' for the first time...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def get_current_weather(city):
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_WEATHER_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()

        if weather_data.get("cod") == 200:
            temp = weather_data["main"]["temp"]
            conditions = weather_data["weather"][0]["description"]
            city_name = weather_data["name"]
            return {"city": city_name, "temperature": f"{temp}°C", "conditions": conditions}
        else:
            print(f"OpenWeatherMap API error for {city}: {weather_data.get('message', 'Unknown error')}")
            return {"city": city, "temperature": "N/A", "conditions": "unknown"}
    except requests.exceptions.RequestException as e:
        print(f"Network or API Key Error fetching weather data for {city}: {e}")
        return {"city": city, "temperature": "N/A", "conditions": "error"}

def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Warning: {USER_DATA_FILE} is corrupted or empty. Starting with fresh data.")
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


static_knowledge = {
    "agent_name": "AI Assistant Prototype",
    "agent_purpose": "I am designed to help with basic tasks like weather information and scheduling.",
    "developer_info": "I was created as an internship project following the Accelerate Career Accelerator Program guide.",
    "current_year": str(datetime.datetime.now().year),
    "greetings_info": [
        "Hello there! How can I assist you today?",
        "Hi! What can I do for you?",
        "Greetings! How may I help you today?",
        "Hey! Nice to hear from you. What's up?"
    ],
    "unknown_response": "I'm not sure how to help with that yet. You can ask me about the weather, scheduling, or general info about myself. Try saying 'help' for a list of things I can do.",
    "low_confidence_response": "I'm having a bit of trouble understanding that request. Could you try rephrasing it, or type 'help' for things I can do?",
    "api_error_message": "I'm having trouble connecting to the external service right now. Please try again later.",
    "thank_you_response": "You're welcome! Is there anything else I can do?",
    "goodbye_response": "Goodbye! Have a great day.",
    "weather_prompt": "Sure, what city would you like the weather for?",
    "scheduling_prompt": "I can help with that. What is the proposed date and time for the meeting?",
    "help_response": "I can help you with weather updates, scheduling meetings, and answering general questions about myself. Try asking 'What's the weather in London?' or 'Schedule a meeting for tomorrow.' You can also ask 'who are you?'",
    "set_preferred_city_prompt": "What city would you like to set as your preferred weather city?",
    "preferred_city_set_confirm": "Okay, I've set your preferred weather city to {city}.",
}

intent_keywords = {
    "get_weather": ["weather", "forecast", "raining", "sunny", "temperature"],
    "schedule_meeting": ["schedule", "meeting", "appointment", "calendar", "book"],
    "greet": ["hello", "hi", "hey", "greetings"],
    "thank_you": ["thank you", "thanks", "appreciate"],
    "exit": ["bye", "exit", "quit", "goodbye"],
    "about_agent": ["who are you", "what are you", "your name"],
    "agent_capabilities": ["what can you do", "help me"],
    "get_current_year": ["what year is it", "current year", "year now"],
    "help": ["help", "what can I ask", "guide me"],
    "set_preferred_city": ["set my city", "my city is", "remember my city"]
}

def recognize_intent_spacy(user_input):
    doc = nlp(user_input.lower())
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in doc.text:
                return intent, 1.0
    return "unknown", 0.5

def extract_entities(user_input, intent):
    doc = nlp(user_input)
    entities = {}

    if intent == "get_weather":
        for ent in doc.ents:
            if ent.label_ == "GPE":
                entities["city"] = ent.text
                break
    elif intent == "schedule_meeting":
        for ent in doc.ents:
            if ent.label_ == "DATE":
                entities["date"] = ent.text
            if ent.label_ == "TIME":
                entities["time"] = ent.text
    return entities

conversation_context = {
    "unknown_count": 0
}

def generate_response(user_input, intent, entities=None, user_prefs=None, confidence=1.0):
    global conversation_context

    if entities is None:
        entities = {}
    if user_prefs is None:
        user_prefs = {}

    if conversation_context.get("awaiting_confirmation") == "schedule_meeting":
        user_input_lower = user_input.lower()
        if "yes" in user_input_lower or "yup" in user_input_lower or "confirm" in user_input_lower:
            date = conversation_context.get("pending_schedule_date")
            time = conversation_context.get("pending_schedule_time")
            response = f"Great! The meeting has been confirmed for {date} at {time}."
            conversation_context.clear()
            conversation_context["unknown_count"] = 0
            return response
        elif "no" in user_input_lower or "nope" in user_input_lower or "cancel" in user_input_lower:
            response = "Okay, I've cancelled that scheduling request. Is there something else I can help with?"
            conversation_context.clear()
            conversation_context["unknown_count"] = 0
            return response
        else:
            response = "I'm still waiting for your confirmation (Yes/No) for the meeting. Or do you want to cancel?"
            return response

    if intent == "unknown":
        conversation_context["unknown_count"] = conversation_context.get("unknown_count", 0) + 1
        if confidence < 0.8 and conversation_context["unknown_count"] < 3:
            response = static_knowledge["low_confidence_response"]
        elif confidence < 0.8 and conversation_context["unknown_count"] >= 3:
            response = "It seems I'm having a lot of trouble understanding you. Perhaps you could try asking one of my main capabilities? " + static_knowledge["help_response"]
            conversation_context.clear()
            conversation_context["unknown_count"] = 0
        else:
            response = static_knowledge["unknown_response"]
    else:
        conversation_context["unknown_count"] = 0


    if intent == "get_weather":
        city = entities.get("city") or conversation_context.get("last_weather_city")
        if not city and user_prefs.get("preferred_weather_city"):
            city = user_prefs["preferred_weather_city"]
        
        if city:
            weather_data = get_current_weather(city)
            if weather_data["temperature"] != "N/A":
                conversation_context["last_weather_city"] = weather_data["city"]
                response = f"The current weather in {weather_data['city']} is {weather_data['temperature']} and {weather_data['conditions']}."
                conversation_context.pop("awaiting_city_for_weather", None)
            elif weather_data["conditions"] == "error":
                response = static_knowledge["api_error_message"]
            else:
                response = f"Sorry, I couldn't get the weather for {weather_data['city']}. Is there another city you'd like to check?"
        else:
            response = static_knowledge["weather_prompt"]
            conversation_context["awaiting_city_for_weather"] = True

    elif intent == "schedule_meeting":
        date = entities.get("date")
        time = entities.get("time")

        conversation_context["meeting_date"] = date if date else conversation_context.get("meeting_date")
        conversation_context["meeting_time"] = time if time else conversation_context.get("meeting_time")

        final_date = conversation_context.get("meeting_date")
        final_time = conversation_context.get("meeting_time")

        if final_date and final_time:
            response = f"I will schedule a meeting for {final_date} at {final_time}. Does that sound correct? (Yes/No)"
            conversation_context["awaiting_confirmation"] = "schedule_meeting"
            conversation_context["pending_schedule_date"] = final_date
            conversation_context["pending_schedule_time"] = final_time
        else:
            conversation_context["awaiting_meeting_details"] = True
            missing_info = []
            if not final_date: missing_info.append("date")
            if not final_time: missing_info.append("time")

            if "date" in missing_info and "time" in missing_info:
                response = static_knowledge["scheduling_prompt"]
            elif "date" in missing_info:
                response = f"Got it for {final_time}. What date would the meeting be on?"
            elif "time" in missing_info:
                response = f"Got it for {final_date}. What time should the meeting be?"

    elif intent == "greet":
        response = random.choice(static_knowledge["greetings_info"])
        conversation_context.clear()
        conversation_context["unknown_count"] = 0

    elif intent == "thank_you":
        response = static_knowledge["thank_you_response"]

    elif intent == "exit":
        response = static_knowledge["goodbye_response"]
        conversation_context.clear()
        conversation_context["unknown_count"] = 0

    elif intent == "about_agent":
        response = static_knowledge["agent_name"] + ". " + static_knowledge["agent_purpose"] + " " + static_knowledge["developer_info"]

    elif intent == "agent_capabilities":
        response = static_knowledge["agent_purpose"] + " I can also recognize greetings and thank yous, and tell you the current year!"

    elif intent == "get_current_year":
        response = f"The current year is {static_knowledge['current_year']}."

    elif intent == "help":
        response = static_knowledge["help_response"]
        conversation_context.clear()
        conversation_context["unknown_count"] = 0

    elif intent == "set_preferred_city":
        city = entities.get("city")
        if city:
            user_prefs["preferred_weather_city"] = city
            response = static_knowledge["preferred_city_set_confirm"].format(city=city)
            conversation_context.pop("awaiting_preferred_city", None)
        else:
            response = static_knowledge["set_preferred_city_prompt"]
            conversation_context["awaiting_preferred_city"] = True

    if intent == "unknown":
        if conversation_context.get("awaiting_city_for_weather"):
            new_doc = nlp(user_input)
            for ent in new_doc.ents:
                if ent.label_ == "GPE":
                    city = ent.text
                    conversation_context["last_weather_city"] = city
                    conversation_context.pop("awaiting_city_for_weather")
                    weather_data = get_current_weather(city)
                    if weather_data["temperature"] != "N/A":
                        response = f"Got it, the weather in {weather_data['city']} is {weather_data['temperature']} and {weather_data['conditions']}."
                    elif weather_data["conditions"] == "error":
                        response = static_knowledge["api_error_message"]
                    else:
                        response = f"Sorry, I couldn't get the weather for {weather_data['city']}. Is there another city you'd like to check?"
                    conversation_context["unknown_count"] = 0
                    return response
            else:
                pass

        elif conversation_context.get("awaiting_preferred_city"):
            new_doc = nlp(user_input)
            for ent in new_doc.ents:
                if ent.label_ == "GPE":
                    city = ent.text
                    user_prefs["preferred_weather_city"] = city
                    conversation_context.pop("awaiting_preferred_city")
                    response = static_knowledge["preferred_city_set_confirm"].format(city=city)
                    conversation_context["unknown_count"] = 0
                    return response
            else:
                pass

        elif conversation_context.get("awaiting_meeting_details"):
            new_doc = nlp(user_input)
            new_date = None
            new_time = None
            for ent in new_doc.ents:
                if ent.label_ == "DATE":
                    new_date = ent.text
                if ent.label_ == "TIME":
                    new_time = ent.text

            current_date = conversation_context.get("meeting_date")
            current_time = conversation_context.get("meeting_time")

            final_date = new_date if new_date else current_date
            final_time = new_time if new_time else current_time

            if final_date and final_time:
                response = f"I will schedule a meeting for {final_date} at {final_time}. Does that sound correct? (Yes/No)"
                conversation_context["awaiting_confirmation"] = "schedule_meeting"
                conversation_context["pending_schedule_date"] = final_date
                conversation_context["pending_schedule_time"] = final_time
                conversation_context["unknown_count"] = 0
                return response
            else:
                conversation_context["meeting_date"] = final_date
                conversation_context["meeting_time"] = final_time
                missing_info = []
                if not final_date: missing_info.append("date")
                if not final_time: missing_info.append("time")
                response = f"I still need the {' and '.join(missing_info)} for the meeting. What is it?"
                conversation_context["unknown_count"] = 0
                return response

    return response


if __name__ == "__main__":
    user_preferences = load_user_data()
    print(f"Loaded user preferences: {user_preferences}")

    if not user_preferences.get("has_been_welcomed", False):
        print("\nAgent: Hello! I'm your AI Assistant Prototype. I'm here to help you with some tasks.")
        print("Agent: I can get you weather updates, help schedule meetings, and answer some general questions about myself.")
        print("Agent: Type 'help' if you want to see a list of things I can do.")
        print("Agent: Let's get started!")
        user_preferences["has_been_welcomed"] = True
        save_user_data(user_preferences)
    else:
        print(random.choice(static_knowledge["greetings_info"]))
        print("Agent: What can I do for you today? (Type 'help' for options)")

    print("\nType 'bye' or 'exit' to quit.")

    while True:
        user_message = input("You: ")

        intent_name, confidence = recognize_intent_spacy(user_message)
        extracted_entities = extract_entities(user_message, intent_name)

        agent_response = generate_response(user_message, intent_name, extracted_entities, user_preferences, confidence)

        print(f"Agent: {agent_response}")

        if intent_name == "exit":
            save_user_data(user_preferences)
            print("User data saved. Goodbye!")
            break
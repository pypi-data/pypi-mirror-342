#Only for Research work & not relevant for app execution
import os
import re
from typing import Optional
import openai
from dotenv import load_dotenv
from groq import Groq

if not os.path.exists(".env"):
    raise FileNotFoundError("⚠️ Missing .env file! Please create one with API keys. Refer to the README.")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")  #'openai' , 'groq' etc
MODEL_NAME = os.getenv("MODEL_NAME")  # gpt-3.5-turbo, gemma2-9b-it 

def clean_string(s: str) -> str:
    return re.sub(r'\\n|\n|\\|"', '', s)

def intelligence_profiler(user_content: str, role: str, model_provider: str = MODEL_PROVIDER, model_name: str = MODEL_NAME) -> str:
    
    system_message = """
    You are an AI Intelligence Profiler. Your task is to analyze a user's request and determine the optimal intelligence parameters needed for an effective response. The parameters to be evaluated are:
    - **reasoning** (0.1 to 1.0): The level of logical depth required.
    - **creativity** (0.1 to 1.0): The degree of imaginative variation required.
    - **precision** (0.1 to 1.0): The specificity level required.
    - **temperature** (0.1 to 1.0): A value derived from the above parameters that influences overall output variability.

    **Instructions:**
    1. Analyze the user's request and consider the specified role.
    2. Adjust the intelligence parameters based on the query's complexity and the typical expertise required for that role.
    3. **Return ONLY a JSON object** in the exact format below with no extra text or explanation:
    { "reasoning": <value>, "creativity": <value>, "precision": <value>, "temperature": <value> }
    """
    user_message = f"""
    User Request: "{user_content}"
    Role: "{role}"

    Please evaluate the above information and return the intelligence parameters in the specified JSON format.
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    # Choose model provider
    if model_provider == "openai":
        openai.api_key = OPENAI_API_KEY
        response = openai.Client().chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3
        )
        content = response.choices[0].message.content
        usage = response.usage  # Extract token usage
        return {"response": content, "usage": usage}  # Return both content and usage
    elif model_provider == "groq":
        client = Groq(api_key=GROQ_API_KEY) 
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=0.2 #temperature if temperature is not None else (1.0 - reasoning if manual_mode else 0.7)            
        )       
        content = response.choices[0].message.content  # Extract response
        usage = response.usage  # Extract token usage
        return {"response": content, "usage": usage}  # Return both content and usage
        #return clean_string(response_text)
def normal_prompt(user_content: str, role: str, model_provider: str = MODEL_PROVIDER, model_name: str = MODEL_NAME, temperature: float = 0.3):
    """  Sends a normal prompt to the selected LLM (OpenAI or Groq) without intelligence parameters.
    """
    system_message = f"""
    You are a {role}. Respond to query: {user_content} based on your expertise.
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_content}
    ]

    response = call_llm(model_provider, model_name, messages, temperature)
    #content = response.choi  ## Extract response
    #usage = response.usage  # Extract token usage
    return response #{"response": content, "usage": usage}  # Return both content and usage

def normal_prompt_with_intelligence(user_content: str, role: str, reasoning: float, creativity: float, precision: float, temperature: float, model_provider: str = MODEL_PROVIDER, model_name: str = MODEL_NAME):
    """
    Sends a prompt to the selected LLM with intelligence parameters.
    """
    system_message = f"""
    You are a {role}. Respond to {user_content}.Adjust the response style dynamically based on intelligence parameters:
    - Reasoning: {reasoning} (0.1 = simple, 1.0 = deep and structured)
    - Creativity: {creativity} (0.1 = factual, 1.0 = imaginative)
    - Precision: {precision} (0.1 = broad, 1.0 = highly detailed)
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_content}
    ]

    response = call_llm(model_provider, model_name, messages, temperature)
    #content = response.choices[0].message.content  # Extract response
    #usage = response.usage  # Extract token usage
    return response # Return both content and usage

def call_llm(model_provider: str, model_name: str, messages: list, temperature: float):
    """
    Handles communication with OpenAI or Groq models.
    """
    if model_provider == "openai":
        response = openai.Client().chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature
        )
        content = response.choices[0].message.content
        usage = response.usage  # Extract token usage
        return {"response": content, "usage": usage}  # Return both content and usage


    elif model_provider == "groq":
        # Implement Groq API call (replace with actual implementation)
        client = Groq(api_key=GROQ_API_KEY) 
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=temperature #temperature if temperature is not None else (1.0 - reasoning if manual_mode else 0.7)            
        )
        content = chat_completion.choices[0].message.content  # Extract response
        usage = chat_completion.usage  # Extract token usage
        return {"response": content, "usage": usage}  # Return both content and usage

    else:
        raise ValueError("Invalid model provider. Choose 'openai' or 'groq'.")

def call_llm_without_temp(model_provider: str, model_name: str, messages: list):
    """  Calls OpenAI or Groq API without specifying temperature, so it defaults to the model's own value.
    """
    if model_provider == "openai":
        response = openai.Client().chat.completions.create(
            model=model_name,
            messages=messages
        )
        content = response.choices[0].message.content  # Extract response
        usage = response.usage  # Extract token usage
        return {"response": content, "usage": usage}  # Return both content and usage


    elif model_provider == "groq":
        client = Groq(api_key=GROQ_API_KEY) 
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_name,
        )
        content = chat_completion.choices[0].message.content  # Extract response
        usage = chat_completion.usage  # Extract token usage
        return {"response": content, "usage": usage}  # Return both content and usage

    else:
        raise ValueError("Invalid model provider. Choose 'openai' or 'groq'.")


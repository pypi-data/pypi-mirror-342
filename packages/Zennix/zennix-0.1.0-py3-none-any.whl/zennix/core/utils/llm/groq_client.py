import os
from groq import Groq

def generate_response(system_prompt='You are a standup comedian', user_prompt='Tell me a joke.', llm_model="llama-3.3-70b-versatile", **kwargs):
    # Set up the API key
    api_key = os.environ.get('GROQ_API_KEY')

    client = Groq(api_key=api_key)

    # Create a message with the prompt
    message = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    # Set up the completion parameters
    completion_params = {
        "model": llm_model,
        "messages": message,
        "max_tokens": kwargs.get("max_tokens", 1024),
        "temperature": kwargs.get("temperature", 0.5),
        "top_p": kwargs.get("top_p", 0.9),
        "stop": kwargs.get("stop", None),
        "stream": kwargs.get("stream", False)
    }

    # Use the LLM to generate a response
    response = client.chat.completions.create(**completion_params)

    # Extract the response text
    response_text = response.choices[0].message.content

    return response_text
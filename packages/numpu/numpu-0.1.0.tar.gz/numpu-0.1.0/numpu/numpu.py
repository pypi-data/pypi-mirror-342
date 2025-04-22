from g4f.client import Client

# initialize the client once
_client = Client()

def np(prompt: str, model: str = "gpt-4o-mini", web_search: bool = False) -> None:
    """
    Send a prompt to the chat client and print the response.

    Args:
        prompt (str): The user prompt to send.
        model (str): Model name (default: 'gpt-4o-mini').
        web_search (bool): Whether to enable web search (default: False).
    """
    response = _client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        web_search=web_search
    )
    print(response.choices[0].message.content)

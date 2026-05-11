import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


# Baad me Gemma 4 available ho to isko update kar denge.
MODEL_NAME = "gemma4:31b-cloud"


def ask_gemma(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        data = response.json()
        return data.get("response", "No response generated.")

    except requests.exceptions.ConnectionError:
        return (
            "Gemma model connection failed. "
            "Please make sure Ollama is installed and running."
        )

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again with a shorter question."

    except Exception as e:
        return f"Error: {e}"
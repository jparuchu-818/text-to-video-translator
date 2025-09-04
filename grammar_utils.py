import requests

def fix_grammar_with_ollama(text: str, model: str = "llama3") -> str:
    print("[INFO] Sending text to Ollama for grammar correction...")

    prompt = f"""
Correct the grammar and improve clarity in the following text.
Return only the corrected version, no explanation or formatting:

\"\"\"
{text.strip()}
\"\"\"
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"].strip()

    except requests.RequestException as e:
        print("[ERROR] Ollama request failed:", e)
        return text.strip()


def split_into_scenes_with_ollama(text: str, model: str = "llama3") -> list[str]:
    print("[INFO] Asking Ollama to split corrected text into scenes...")

    prompt = f"""
Take the following well-written text and break it into clear SCENES.
Each scene should be 1 to 3 sentences and describe a self-contained idea.
Return the list with one scene per line, without numbering or extra formatting.

\"\"\"
{text.strip()}
\"\"\"
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        lines = response.json()["response"].strip().split('\n')
        return [line.strip() for line in lines if line.strip()]

    except requests.RequestException as e:
        print("[ERROR] Ollama request failed:", e)
        return [text.strip()]

#similar prompt version as fix_grammar_with_ollama(), lightweight grammar correction using ollama
def correct_grammar(text: str) -> str:
    """
    Corrects grammar using Ollama LLaMA model.
    You can modify this to use your local API call if needed.
    """
    prompt = f"Fix the grammar of this sentence while preserving its meaning: \"{text}\""
    
    response = requests.post(
        "http://localhost:11434/api/generate",  
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    
    if response.status_code == 200:
        return response.json()['response'].strip()
    else:
        raise Exception(f"Grammar correction failed: {response.text}")
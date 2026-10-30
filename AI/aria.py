import json
import threading
from llama_cpp import Llama

SYSTEM = "You are ARIA, the AI of Screamaze. You only answer questions about the game."

llm = Llama(model_path="AI/game-q4_k_m.gguf", n_ctx=2048, verbose=False)

with open("AI/lore.json", encoding="utf-8") as f:
    lore = json.load(f)


def find_lore(question):
    question = " " + question.lower() + " "
    found = ""
    count = 0
    for entry in lore:
        for keyword in entry["keywords"]:
            if keyword in question and count < 6:
                found = found + entry["fact"] + "\n"
                count = count + 1
                break
    return found


def ask(question, on_text):
    system = SYSTEM + "\nKnowledge:\n" + find_lore(question)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ]
    for part in llm.create_chat_completion(messages=messages, max_tokens=150, stream=True):
        text = part["choices"][0]["delta"].get("content", "")
        on_text(text)


def ask_in_background(question, on_text):
    threading.Thread(target=ask, args=(question, on_text), daemon=True).start()
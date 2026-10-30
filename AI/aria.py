import glob
import json
import threading
import traceback
from llama_cpp import Llama

SYSTEM = "You are ARIA, the AI of Screamaze. You only answer questions about the game."

llm = None      # loaded the first time somebody asks, so the game also starts without the model (the start screen downloads it)
NO_MODEL = "The AI is not installed yet. Use Download AI and Open AI folder on the start screen."
ERROR = "ARIA could not answer this one: "

lock = threading.Lock()     # the model can only answer one question at a time, a second question waits here until the first answer is done

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


def getModel():
    global llm
    if llm is None:
        # the full model is the standard, the 4-bit one is the smaller brother used when it is the only one
        files = sorted(glob.glob("AI/*.gguf"), key=lambda f: "f16" not in f)
        if not files:
            return None
        llm = Llama(model_path=files[0], n_ctx=2048, verbose=False)
    return llm


def ask(question, on_text):
    with lock:
        try:
            model = getModel()
            if model is None:
                on_text(NO_MODEL)
                return
            system = SYSTEM + "\nKnowledge:\n" + find_lore(question)
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": question},
            ]
            for part in model.create_chat_completion(messages=messages, max_tokens=150, stream=True):
                text = part["choices"][0]["delta"].get("content", "")
                on_text(text)
        except Exception as e:      # an error in the thread would be lost, so the player sees it in the chat
            traceback.print_exc()
            on_text(ERROR + str(e)[:120])


def ask_in_background(question, on_text):
    threading.Thread(target=ask, args=(question, on_text), daemon=True).start()
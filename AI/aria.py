import glob
import json
import threading
import traceback

TOP_FACTS = 3       # the model was trained with exactly 3 facts per question

with open("AI/aria_knowledge.json", encoding="utf-8") as f:
    knowledge = json.load(f)
SYSTEM = knowledge["system"]        # the line the model was trained with, it is not shown to the player

llm = None      # loaded the first time somebody asks, so the game also starts without the model (the start screen downloads it)
formatter = None
NO_MODEL = "The AI is not installed yet. Use Download AI and Open AI folder on the start screen."
NO_LLAMA = "The AI needs llama-cpp-python: pip install llama-cpp-python"
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
            if keyword in question and count < TOP_FACTS:
                found = found + entry["fact"] + "\n"
                count = count + 1
                break
    return found


def getModel():
    global llm, formatter
    if llm is None:
        # the full model is the standard, the 4-bit one is the smaller brother used when it is the only one
        files = sorted(glob.glob("AI/*.gguf"), key=lambda f: "f16" not in f)
        if not files:
            return None
        from llama_cpp import Llama     # here and not at the top, so the game also starts without the package
        from llama_cpp.llama_chat_format import Jinja2ChatFormatter
        llm = Llama(model_path=files[0], n_ctx=2048, verbose=False)
        template = llm.metadata["tokenizer.chat_template"]
        formatter = Jinja2ChatFormatter(template=template, eos_token=llm._model.token_get_text(llm.token_eos()), bos_token="")
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
            # thinking is turned off in the template, otherwise the model writes its reasoning instead of an answer
            prompt = formatter(messages=messages, enable_thinking=False).prompt
            for part in model.create_completion(prompt, max_tokens=150, temperature=0, stop=["<|im_end|>"], stream=True):
                on_text(part["choices"][0]["text"])
        except ImportError:
            on_text(NO_LLAMA)
        except Exception as e:      # an error in the thread would be lost, so the player sees it in the chat
            traceback.print_exc()
            on_text(ERROR + str(e)[:120])


# loads the model while the player is still in the menus, so the first question doesn't have to wait for it
def preload():
    def load():
        with lock:
            try:
                getModel()
            except Exception:       # the first question tries again and shows the error in the chat
                traceback.print_exc()
    threading.Thread(target=load, daemon=True).start()


def ask_in_background(question, on_text):
    threading.Thread(target=ask, args=(question, on_text), daemon=True).start()

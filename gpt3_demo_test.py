import argparse
import json
import random

import os
import openai
openai.organization = "<Your Organization ID>"
openai.api_key = "Your API Key"

MODEL_NAME = "davinci:ft-yoo-2023-04-26-06-42-10"

PROMPT_DICT = {
    "first_turn_prompt": (
        "{persona}\n."
        "Engage in a conversation about {topic} by showcasing your personas. Share interesting anecdotes, facts, and experiences related to {topic}\n\n"
        "### Input:\n{input}\n\n### Response:\n"
    ),
    "other_turn_prompt": (
        "### Input:\n{input}\n\n### Response:\n"
    )
}

MAX_HISTORY = 10

class RandomElementSelector:
    _instance = None

    def __new__(cls, persona_file_path=None, topic_file_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if persona_file_path is None or topic_file_path is None:
                raise ValueError("persona_file_path and topic_file_path must be provided during the first instantiation")
            cls._instance.persona_file_path = persona_file_path
            cls._instance.topic_file_path = topic_file_path
            cls._instance.persona_list = []
            cls._instance.topic_list = []
            cls._instance._initialize_elements()
        return cls._instance

    def _initialize_elements(self):
        with open(self.persona_file_path, 'r') as file:
            self.persona_list = json.load(file)
        with open(self.topic_file_path, 'r') as file:
            self.topic_list = json.load(file)

    def get_random_persona(self):
        return random.choice(self.persona_list)
    
    def get_random_topic(self):
        return random.choice(self.topic_list)

def getFirstTurnPrompt(persona, topic, user_text):
    return PROMPT_DICT["first_turn_prompt"].format(persona=persona, topic=topic, input=user_text)

def join_history(history):
    first_item = history[0]
    last_items = history[-MAX_HISTORY:] if len(history) > MAX_HISTORY else history[1:]

    result = first_item + ' ' + ' '.join(last_items)
    return result

def getOtherTurnPrompt(history, user_text):
    prompt = join_history(history)
    prompt = prompt + PROMPT_DICT["other_turn_prompt"].format(input=user_text)
    return prompt

def getAPIBotResponse(persona, topic, history, user_text):
    if history is None or len(history) == 0:
        selector = RandomElementSelector()
        persona = selector.get_random_persona()
        topic = selector.get_random_topic()
        first_prompt = getFirstTurnPrompt(persona, topic, user_text)
        output = getModelOutput(first_prompt).strip()
        history.append(first_prompt)
        history.append(output)
        return persona, topic, history, output
    else:
        prompt = getOtherTurnPrompt(history, user_text)
        output = getModelOutput(prompt).strip()
        history.append(user_text)
        history.append(output)
        return persona, topic, history, output

def getModelOutput(prompt):
    global MODEL_NAME
    output = openai.Completion.create(
        model=MODEL_NAME,
        prompt=prompt,
        max_tokens=150,
        stop=["\n", "###"])
    output = output["choices"][0]["text"].strip()
    return output

def main(args):
    # Initialize the selector
    selector = RandomElementSelector(args.persona_file, args.topic_file)

    # Start the conversation
    history = []
    persona = ""
    topic = ""
    user_text = "[Start]"
    persona, topic, history, output = getAPIBotResponse(persona, topic, history, user_text)
    print(f"Bot: {output}")

    while True:
        user_text = input("You: ")
        if user_text == "quit":
            break
        persona, topic, history, output = getAPIBotResponse(persona, topic, history, user_text)
        print(f"Bot: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona-file", type=str, default="personas.json",
        help="persona json file.")
    parser.add_argument("--topic-file", type=str, default="topics.json",
        help="topic json file.")
    args = parser.parse_args()
    main(args)

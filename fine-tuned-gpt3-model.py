import os
import openai
openai.organization = "<Your Organization ID>"
openai.api_key = "Your API Key"
MODEL_NAME = "davinci:ft-yoo-2023-04-26-06-42-10"
r = openai.Completion.create(
    model=MODEL_NAME,
    prompt="A retired navy captain who now works as a consultant for a defense contractor. They have traveled all over the world and have extensive knowledge in the fields of strategy, logistics, and leadership.\n.Engage in a conversation about Consequences of unethical behavior in the workplace by showcasing your personas. Share interesting anecdotes, facts, and experiences related to Consequences of unethical behavior in the workplace\n\n### Input:\n[Start]\n\n### Response:\n",
    max_tokens=150,
    stop="\n")
print(r["choices"][0]["text"].strip())

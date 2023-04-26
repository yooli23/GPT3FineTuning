# Fine-tuning GPT-3.5 using OpenAI APIs

This guide will walk you through the process of fine-tuning the GPT-3.5 model with your specific data using OpenAI APIs.

## Prerequisites

1. An OpenAI API key: Sign up for an account on [OpenAI](https://beta.openai.com/signup) and obtain your API key.
2. Python: Ensure you have Python 3.6 or newer installed.
3. `openai` Python library: Install the OpenAI Python library with the command `pip install openai`.

## Steps to Fine-tune GPT-3.5

### 1. Prepare your dataset

Your dataset should be in JSONL format, with each line containing a JSON object. The object should have a `prompt` and a `completion` field.

Example:

```json
{"prompt": "Translate the following English text to French: 'Hello, how are you?'", "completion": "Bonjour, comment ça va ?"}
{"prompt": "What is the capital of France?", "completion": "Paris"}
```

Save your data as a jsonl file: `train.jsonl` for training, in our case, it is `nce_gpt3_training_data_prepared.jsonl`. We have 500 training examples in this file, the format of each example is:

```json
{"prompt": "<Persona>\n.Engage in a conversation about <topic> by showcasing your personas. Share interesting anecdotes, facts, and experiences related to <topic>\n\n### Input:\n[Start]\n\n### Response:\n", "completion": "<next bot response>"}
```

You can also use the openai library to prepare your CSV, TSV, XLSX, JSON or JSONL file. For example:

```bash
openai tools fine_tunes.prepare -f nce_gpt3_training_data.json -o nce_gpt3_training_data_prepared.jsonl
```

### 2. Upload your dataset and fine-tune the GPT-3.5 model

Use the following command to fine-tune the davinci-text-003 model:

```bash
openai api fine_tunes.create -t "nce_gpt3_training_data_prepared.jsonl" -m davinci
```

### 3. Check the fine-tuning status

To monitor the progress of your fine-tuning process, use the following commands:

```bash
# List all created fine-tunes
openai api fine_tunes.list

# Retrieve the state of a fine-tune. The resulting object includes
# job status (which can be one of pending, running, succeeded, or failed)
# and other information
openai api fine_tunes.get -i <YOUR_FINE_TUNE_JOB_ID>

# Cancel a job
openai api fine_tunes.cancel -i <YOUR_FINE_TUNE_JOB_ID>
```

### 5. Test your fine-tuned model

After the fine-tuning process is complete, you can test your model using the following Python script:

```python
import openai

openai.api_key = "your-api-key"

response = openai.Completion.create(
    engine="your-fine-tuned-model",
    prompt="Your prompt goes here",
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
)

print(response.choices[0].text)
```

Replace `"your-fine-tuned-model"` with the ID of your fine-tuned model.

In our case, you can run `test-gpt3-model.py` to test the fine-tuned model.

That's it! You have successfully fine-tuned the GPT-3.5 model using OpenAI APIs with your specific data. You can now use your fine-tuned model to generate more accurate and relevant complet

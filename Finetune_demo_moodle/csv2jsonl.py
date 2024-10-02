import json
import pandas as pd

#make sure change this:
DEFAULT_SYSTEM_PROMPT = 'AiBot is a theocean.ai chatbot.'

def get_example(question, answer):
    return {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    }

if __name__ == "__main__":
    df = pd.read_csv("dataset.csv")
    with open("train.jsonl", "w") as f:
        for i, row in list(df.iterrows()):
            question = row["question"]
            answer = row["answer"]
            example = get_example(question, answer)
            example_str = json.dumps(example)
            f.write(example_str + "\n")

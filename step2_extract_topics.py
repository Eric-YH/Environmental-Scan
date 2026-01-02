import os
import pandas as pd
from io import StringIO
from common import BASE_DIR, read_text_file, escape_csv, call_llm, save_csv

BATCH_SIZE = 20


def load_statements():
    path = os.path.join(BASE_DIR, "Environmental Scan.xlsx")
    df = pd.read_excel(path)
    return df.iloc[:, 0].dropna().astype(str).tolist()


def extract_topics(statements):
    api_key = read_text_file("OpenRouter API key.txt")
    prompt_template = read_text_file("Prompt Words1.txt")

    all_batches = []

    for start in range(0, len(statements), BATCH_SIZE):
        batch = statements[start:start + BATCH_SIZE]

        lines = ["id,statement"]
        for i, stmt in enumerate(batch):
            stmt_id = start + i + 1
            lines.append(f'{stmt_id},"{escape_csv(stmt)}"')

        input_csv = "\n".join(lines)
        prompt = prompt_template.replace("{STATEMENTS}", input_csv)

        print(f"\n📦 Step2 batch {start // BATCH_SIZE + 1}")
        raw = call_llm(prompt, api_key)

        df_batch = pd.read_csv(StringIO(raw), engine="python")
        all_batches.append(df_batch)

    return pd.concat(all_batches, ignore_index=True)


if __name__ == "__main__":
    statements = load_statements()
    topics_df = extract_topics(statements)
    save_csv(topics_df, "step2_topics.csv")
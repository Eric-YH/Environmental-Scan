import pandas as pd
from io import StringIO
from common import read_text_file, call_llm, save_csv, BASE_DIR


def induce_categories():
    api_key = read_text_file("OpenRouter API key.txt")
    prompt_template = read_text_file("Prompt Words2.txt")

    topics_df = pd.read_csv(f"{BASE_DIR}\\step2_topics.csv")
    topics_csv = topics_df.to_csv(index=False)

    prompt = prompt_template.replace("{TOPICS}", topics_csv)

    print("📊 Step3 inducing categories...")
    raw = call_llm(prompt, api_key)

    categories_df = pd.read_csv(StringIO(raw), engine="python")
    return categories_df


if __name__ == "__main__":
    df = induce_categories()
    save_csv(df, "step3_suggested_categories.csv")
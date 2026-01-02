import os
import pandas as pd
from io import StringIO
from common import BASE_DIR, read_text_file, escape_csv, call_llm, save_csv


def load_statements():
    df = pd.read_excel(f"{BASE_DIR}\\Environmental Scan.xlsx")
    return df.iloc[:, 0].dropna().astype(str).tolist()


def classify_in_batches(statements, categories_df, batch_size=10):
    api_key = read_text_file("OpenRouter API key.txt")
    prompt_template = read_text_file("Prompt Words3.txt")

    all_results = []

    for start in range(0, len(statements), batch_size):
        batch = statements[start:start + batch_size]
        print(f"\n📦 Classifying statements {start + 1}–{start + len(batch)}")

        # build statements CSV with GLOBAL id
        stmt_lines = ["id,statement"]
        for i, stmt in enumerate(batch):
            stmt_lines.append(
                f'{start + i + 1},"{escape_csv(stmt)}"'
            )

        statements_csv = "\n".join(stmt_lines)
        categories_csv = categories_df.to_csv(index=False)

        prompt = (
            prompt_template
            .replace("{STATEMENTS}", statements_csv)
            .replace("{CATEGORIES}", categories_csv)
        )

        raw = call_llm(prompt, api_key)

        batch_df = pd.read_csv(
            StringIO(raw),
            engine="python",
            on_bad_lines="error"
        )

        all_results.append(batch_df)

    return pd.concat(all_results, ignore_index=True)


if __name__ == "__main__":
    statements = load_statements()

    final_path = f"{BASE_DIR}\\final_categories.csv"
    if os.path.exists(final_path):
        categories_df = pd.read_csv(final_path)
        print("✅ Using final_categories.csv")
    else:
        categories_df = pd.read_csv(f"{BASE_DIR}\\step3_suggested_categories.csv")
        print("⚠️ Using suggested categories")

    results_df = classify_in_batches(
        statements,
        categories_df,
        batch_size=10
    )

    save_csv(results_df, "step5_final_classification.csv")
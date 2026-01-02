import pandas as pd
from common import BASE_DIR, save_csv


def safe_text(text):
    """
    Prevent Excel from interpreting text as formulas
    """
    if not isinstance(text, str):
        return ""
    text = text.strip()
    if text.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def summarize_by_category():
    df = pd.read_csv(f"{BASE_DIR}\\step5_final_classification.csv")

    rows = []

    for category, g in df.groupby("category"):
        opps = [
            safe_text(o)
            for o in g["opportunity"].dropna().unique()
            if str(o).strip()
        ]

        risks = [
            safe_text(r)
            for r in g["risk"].dropna().unique()
            if str(r).strip()
        ]

        rows.append({
            "category": category,
            "opportunities_summary": "\n".join(f"- {o}" for o in opps),
            "risks_summary": "\n".join(f"- {r}" for r in risks)
        })

    summary_df = pd.DataFrame(rows)
    save_csv(summary_df, "step6_category_summary.csv")


if __name__ == "__main__":
    summarize_by_category()
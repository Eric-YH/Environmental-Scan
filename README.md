LLM-assisted Text Classification Pipeline

This project implements a human-in-the-loop NLP pipeline for classifying unstructured text using Large Language Models (LLMs).
The workflow combines automated topic extraction and classification with manual review for semantic accuracy.

Project Structure
classify/
├── Environmental Scan.xlsx        # Input file (first column contains raw text)
├── Prompt Words1.txt              # Prompt for topic extraction (Step 2)
├── Prompt Words2.txt              # Prompt for category induction (Step 3)
├── Prompt Words3.txt              # Prompt for final classification (Step 5)
├── OpenRouter API key.txt          # OpenRouter API key (NOT committed)
├── common.py                      # Shared utilities (LLM call, IO helpers)
├── step2_topics.csv               # Extracted topics (LLM output)
├── step3_suggested_categories.csv # LLM-suggested taxonomy
├── final_categories.csv           # (Optional) Human-reviewed taxonomy
├── step5_final_classification.csv # Final classification results
└── README.md


Minimum required versions:
requests>=2.31.0
python-docx>=0.8.11
pandas>=1.5.0
openpyxl>=3.0.10

API Key Setup (Required)
OpenRouter API key.txt

Notes
Batch processing is used to reduce cost and improve stability
LLM temperature is set to 0 for deterministic output
CSV is used as the interface between pipeline steps
Human review is required for final category definitions

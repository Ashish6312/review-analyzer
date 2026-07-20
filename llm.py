import json
from typing import Any

import pandas as pd
from tqdm import tqdm

from config import INPUT_FILE, OUTPUT_CSV, OUTPUT_JSON
from llm import analyze_review
from parser import parse_llm_response
from prompts import PROMPT
from utils import logger


def load_reviews(file_path) -> list[str]:
    """
    Load customer reviews from a JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data: list[dict[str, Any]], file_path) -> None:
    """
    Save results to a JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def save_csv(data: list[dict[str, Any]], file_path) -> None:
    """
    Save results to a CSV file.
    """
    df = pd.DataFrame(data)

    # Store topics as comma-separated values
    df["topics"] = df["topics"].apply(
        lambda topics: ", ".join(topics)
        if isinstance(topics, list)
        else topics
    )

    df.to_csv(file_path, index=False)


def process_reviews(reviews: list[str]) -> list[dict[str, Any]]:
    """
    Analyze all reviews using the LLM.
    """
    results: list[dict[str, Any]] = []

    for index, review in enumerate(
        tqdm(reviews, desc="Analyzing Reviews"),
        start=1,
    ):
        logger.info("Processing review %s/%s", index, len(reviews))

        try:
            response = analyze_review(review, PROMPT)

            parsed = parse_llm_response(response)
            parsed["review"] = review

            results.append(parsed)

        except ValueError as error:
            logger.error("Parsing failed: %s", error)

            results.append(
                {
                    "sentiment": "Unknown",
                    "topics": [],
                    "summary": "Extraction failed.",
                    "review": review,
                }
            )

        except Exception as error:
            logger.exception("Unexpected error: %s", error)

            results.append(
                {
                    "sentiment": "Unknown",
                    "topics": [],
                    "summary": "Unexpected error.",
                    "review": review,
                }
            )

    return results


def main() -> None:
    """
    Main application entry point.
    """
    try:
        logger.info("Loading reviews...")

        reviews = load_reviews(INPUT_FILE)

        logger.info("Loaded %s reviews.", len(reviews))

        results = process_reviews(reviews)

        save_json(results, OUTPUT_JSON)
        save_csv(results, OUTPUT_CSV)

        logger.info("Results saved successfully.")
        logger.info("JSON -> %s", OUTPUT_JSON.name)
        logger.info("CSV  -> %s", OUTPUT_CSV.name)

    except FileNotFoundError:
        logger.error("Input file '%s' not found.", INPUT_FILE.name)

    except json.JSONDecodeError:
        logger.error("Invalid JSON in '%s'.", INPUT_FILE.name)

    except Exception as error:
        logger.exception("Application failed: %s", error)


if __name__ == "__main__":
    main()
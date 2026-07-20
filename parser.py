import json
import re


def clean_response(response: str) -> str:
    """
    Removes markdown code fences and extra whitespace.
    """

    response = response.strip()

    # Remove markdown code blocks
    response = response.replace("```json", "")
    response = response.replace("```", "")

    return response.strip()


def extract_json(response: str) -> str:
    """
    Extract the first JSON object from the response.
    This handles cases where the model adds extra text.
    """

    match = re.search(r"\{[\s\S]*\}", response)

    if not match:
        raise ValueError(
            f"No JSON object found in model response:\n\n{response}"
        )

    return match.group(0)


def validate_response(data: dict):
    """
    Validate required fields exist.
    """

    required_fields = [
        "sentiment",
        "topics",
        "summary"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(data["topics"], list):
        raise ValueError("'topics' must be a list")


def parse_llm_response(response: str) -> dict:
    """
    Complete parsing pipeline.
    """

    cleaned = clean_response(response)

    json_string = extract_json(cleaned)

    try:
        data = json.loads(json_string)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by model:\n\n{json_string}"
        ) from e

    validate_response(data)

    return data
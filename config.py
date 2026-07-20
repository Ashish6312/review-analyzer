from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Input / Output Files
INPUT_FILE = BASE_DIR / "reviews.json"
OUTPUT_JSON = BASE_DIR / "output.json"
OUTPUT_CSV = BASE_DIR / "output.csv"

# LLM Configuration
MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0
MAX_TOKENS = 300
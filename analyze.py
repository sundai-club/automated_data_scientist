import sys
from pathlib import Path

from dotenv import load_dotenv

_ = load_dotenv(Path(__file__).parent / ".env")


def analyze(prompt: str, data: str):
    # TODO insert agentic system
    print("Analyzing data...")
    print("Data analyzed!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyze.py <promptfile> <datafile>")
        print("Example: python analyze.py data/prompt.txt data/data.vcf")
        sys.exit(1)

    promptfile = sys.argv[1]
    datafile = sys.argv[2]
    prompt = open(promptfile).read()
    data = open(datafile).read()
    analyze(prompt, data)

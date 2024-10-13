# Installation

```
cp .env.example .env
# then edit .env file, add you
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Run

Run the analyzer
```
python analyze.py  data/prompt.txt data/data.vcf
```

Run the planner
```
python planner.py data/prompt_planner.txt knowledge_sources
```

# Crisis Need to Resource Matching Engine

## Problem
During disasters, emergency requests arrive as unstructured, emotional messages.
Manual interpretation slows response time and increases errors.

## Solution
This project is a decision-support tool that:
- Reads unstructured emergency messages
- Extracts need, location, and urgency
- Prioritizes requests using transparent rules
- Matches requests with available nearby resources
- Explains every decision for human responders

## How It Works
1. Emergency messages are ingested as free text
2. Rule-based logic extracts key information
3. Urgency is scored using explainable criteria
4. Matching resources are identified
5. Output is presented for responder review

## Tech Stack
- Python
- Rule-based NLP
- Explainable logic (no black-box AI)

## How to Run
```bash
python main.py

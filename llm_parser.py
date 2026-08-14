"""
llm_parser.py
-------------
Sends raw client notes to an LLM (via Groq API) and asks for a
structured backlog: Epics -> User Stories -> Acceptance Criteria.

Returns a Python dict (parsed from the model's JSON response) or
None if parsing fails.
"""

import os
from dotenv import load_dotenv
import json
import re
from groq import Groq
load_dotenv()
# Load API key from environment variable GROQ_API_KEY
# (set this in a .env file or your shell — see README)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an experienced Agile Business Analyst / Scrum consultant.
Given raw, unstructured client notes (meeting transcript, email, or brief),
extract a structured product backlog.

Return ONLY valid JSON, no preamble, no markdown fences, in exactly this shape:

{
  "epics": [
    {
      "title": "string",
      "description": "string",
      "stories": [
        {
          "title": "string (format: As a <user>, I want <goal>, so that <benefit>)",
          "description": "string, 1-2 sentences",
          "priority": "High | Medium | Low",
          "acceptance_criteria": ["string", "string"]
        }
      ]
    }
  ]
}

Rules:
- Group related requirements into epics (3-6 epics max for a typical brief).
- Each epic should have 2-5 user stories.
- Infer sensible priority based on what the client emphasized (e.g. MVP scope = High).
- Write acceptance criteria as short, testable statements (Given/When/Then style is fine).
- If the notes mention a phase 2 / deferred item, still include it but mark priority "Low".
- Do not invent unrelated features. Only extract what is implied by the notes.
"""


def extract_backlog(raw_notes: str):
    """Call the LLM and parse its JSON response into a Python dict."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw_notes},
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        content = response.choices[0].message.content.strip()

        # Strip markdown code fences if the model added them anyway
        content = re.sub(r"^```(json)?|```$", "", content, flags=re.MULTILINE).strip()

        return json.loads(content)

    except json.JSONDecodeError:
        print("Failed to parse JSON from model output:\n", content)
        return None
    except Exception as e:
        print("LLM call failed:", e)
        return None

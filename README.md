# AI-Assisted Sprint Planning Tool

Paste raw, unstructured client notes (a call transcript, an email, a brief) and this
tool uses an LLM to extract a structured Agile backlog — **Epics → User Stories →
Acceptance Criteria** — which you can then push directly into **Jira** as real issues.

This simulates the exact workflow described in most Tech/Digital Transformation
consulting JDs: *"ensure requirements are captured in a proper manner and converted
into solutions design... using agile methodology."*

---

## What's in this folder

```
ai-sprint-planner/
├── app.py                      # Streamlit UI — main entry point
├── llm_parser.py                # Sends notes to Groq LLM, returns structured backlog
├── jira_client.py               # Pushes backlog into Jira via REST API
├── requirements.txt
├── .env.example                 # Template for your API key
└── data/
    └── sample_client_notes.txt  # Ready-made test input
```

---

## Step-by-step setup

### 1. Get your free Groq API key
1. Go to https://console.groq.com and sign up (free).
2. Go to **API Keys** → **Create API Key**.
3. Copy the key.

### 2. Get a free Jira Cloud sandbox (optional but recommended)
1. Go to https://www.atlassian.com/software/jira/free and create a free Jira Cloud site
   (e.g. `yourname.atlassian.net`).
2. Create a new **Scrum project** — note its **Project Key** (shown in the URL / project settings,
   e.g. `SCRUM`).
3. Create an API token: go to https://id.atlassian.com/manage-profile/security/api-tokens →
   **Create API token**. Copy it — you'll paste it into the app's sidebar, not into any file.

> You can skip Jira entirely and still demo the tool — it will generate and display the
> backlog beautifully in the UI. Jira push is the "bonus" step that makes the project stand out.

### 3. Install dependencies
```bash
cd ai-sprint-planner
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Add your Groq key
```bash
cp .env.example .env
```
Open `.env` and paste your real Groq key:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

Then load it before running (or use `python-dotenv`, already in requirements):
```bash
export $(cat .env | xargs)      # Mac/Linux
```
(On Windows, set it via `set GROQ_API_KEY=gsk_xxxx` or a `.env` loader in your shell.)

### 5. Run the app
```bash
streamlit run app.py
```
It opens at `http://localhost:8501`.

### 6. Try it
- Click **"Use Sample Notes"** to auto-fill a realistic client brief and generate a backlog instantly.
- Or paste your own notes and click **Generate Backlog**.
- To push to Jira: fill in the sidebar (Jira URL, email, API token, project key), click
  **Test Jira Connection** to confirm it works, then click **Push Backlog to Jira**.
- Open your Jira board — you'll see real Epics and Stories created from your notes.

---

## Suggested build order (if you want to build this yourself rather than just run it)

1. **Day 1–2:** Get the Streamlit UI working with a hardcoded/fake backlog (no LLM yet) —
   just get the epic/story/acceptance-criteria display right.
2. **Day 2–3:** Wire up the Groq API call in `llm_parser.py`. Test with 3-4 different
   sample notes until the JSON output is consistently well-structured.
3. **Day 4:** Set up your free Jira Cloud sandbox and get the REST API creating issues
   manually first (via `curl` or Postman) before wiring it into `jira_client.py`.
4. **Day 5:** Connect the "Push to Jira" button end-to-end. Test with real notes.
5. **Day 6:** Polish — add error handling, a "download backlog as CSV" button, maybe a
   sprint-grouping feature (assign stories to Sprint 1 / Sprint 2 based on priority).
6. **Day 7:** Write up your README, take screenshots of the UI + resulting Jira board,
   push to GitHub.

## Extension ideas (if you have extra time)
- Auto-assign stories to sprints based on priority + a team velocity estimate.
- Add a "story point estimation" step where the LLM suggests Fibonacci estimates.
- Export the backlog as a CSV/Excel (useful stakeholders who don't use Jira).
- Add a second LLM pass that flags ambiguous/missing requirements ("client didn't specify
  password reset flow — recommend clarifying before sprint planning").

---

## Troubleshooting

**Jira Epic creation fails / 400 error on Epic type**
Some Jira "team-managed" free projects don't expose the `Epic` issue type by default.
The code already handles this gracefully (falls back to just creating Stories) — but if you
want Epics too, go to **Project Settings → Issue Types** in Jira and enable Epic.

**LLM returns text that isn't valid JSON**
This happens occasionally with any LLM. The `extract_backlog()` function already strips
markdown code fences, but if it still fails, just click **Generate Backlog** again —
`temperature=0.3` keeps it fairly consistent but not perfectly deterministic.

**`GROQ_API_KEY` not found**
Make sure you exported it in the same terminal session you're running `streamlit run app.py` from,
or use `python-dotenv` to auto-load `.env` (add `from dotenv import load_dotenv; load_dotenv()`
at the top of `llm_parser.py` if you'd rather not export manually).

---

## How to describe this on your resume

**AI-Assisted Sprint Planning Tool** | Python, Streamlit, Groq API (LLM), Jira REST API
- Built a tool that converts unstructured client notes into a structured Agile backlog
  (Epics, User Stories, Acceptance Criteria) using an LLM, then pushes issues directly into
  Jira via its REST API — automating a core requirements-gathering workflow used in Agile
  delivery and digital transformation programs.
- Designed prompt logic to consistently extract prioritized, testable user stories from
  raw meeting notes, reducing manual backlog-grooming effort.

Keep the specific numbers/claims honest to what you actually built and tested — if you
only tested it on 3-4 sample inputs, don't claim it's "production-ready"; say "prototype"
or "proof of concept," which is accurate and still impressive for a student project.

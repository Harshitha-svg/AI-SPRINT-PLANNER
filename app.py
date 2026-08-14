"""
AI-Assisted Sprint Planning Tool
--------------------------------
Paste raw client notes / meeting transcript / email -> LLM extracts
structured Epics, User Stories, and Acceptance Criteria -> push to Jira.

Run:
    streamlit run app.py
"""

import streamlit as st
from llm_parser import extract_backlog
from jira_client import push_to_jira, test_jira_connection

st.set_page_config(page_title="AI Sprint Planner", layout="wide")

st.title("🧠 AI-Assisted Sprint Planning Tool")
st.caption(
    "Paste unstructured client notes, an email thread, or meeting minutes. "
    "The tool extracts Epics → User Stories → Acceptance Criteria, "
    "then (optionally) creates them directly in Jira."
)

# ---------------------------------------------------------------------
# Sidebar: Jira connection settings
# ---------------------------------------------------------------------
with st.sidebar:
    st.header("Jira Settings (optional)")
    jira_url = st.text_input("Jira URL", placeholder="https://yourdomain.atlassian.net")
    jira_email = st.text_input("Jira Email")
    jira_token = st.text_input("Jira API Token", type="password")
    jira_project_key = st.text_input("Project Key", placeholder="e.g. SCRUM")

    if st.button("Test Jira Connection"):
        ok, msg = test_jira_connection(jira_url, jira_email, jira_token)
        st.success(msg) if ok else st.error(msg)

    st.divider()
    st.caption(
        "No Jira account? Leave these blank — the tool still generates "
        "the backlog, you just won't be able to push it automatically."
    )

# ---------------------------------------------------------------------
# Main input
# ---------------------------------------------------------------------
sample = """We had a call with the client today about their new customer
loyalty app. They want users to sign up with email or phone, earn points
on purchases, and redeem points for discounts. They also mentioned wanting
a referral system where existing users get bonus points for inviting
friends. Admin team needs a dashboard to see redemption trends. They're
worried about launch timeline — want an MVP in 6 weeks focused on
signup, points earning, and redemption only. Referral and admin dashboard
can be phase 2."""

notes = st.text_area(
    "Paste client notes / transcript / email here",
    height=220,
    placeholder=sample,
)

col1, col2 = st.columns([1, 1])
with col1:
    generate_clicked = st.button("Generate Backlog", type="primary")
with col2:
    use_sample = st.button("Use Sample Notes")

if use_sample:
    notes = sample
    generate_clicked = True

# ---------------------------------------------------------------------
# Generate backlog
# ---------------------------------------------------------------------
if generate_clicked:
    if not notes.strip():
        st.warning("Paste some notes first.")
    else:
        with st.spinner("Extracting epics and user stories..."):
            backlog = extract_backlog(notes)

        if backlog is None:
            st.error("Could not parse a backlog from the model output. Try again.")
        else:
            st.session_state["backlog"] = backlog

# ---------------------------------------------------------------------
# Display + push to Jira
# ---------------------------------------------------------------------
if "backlog" in st.session_state:
    backlog = st.session_state["backlog"]
    st.subheader("Generated Backlog")

    for epic in backlog.get("epics", []):
        with st.expander(f"📦 EPIC: {epic['title']}", expanded=True):
            st.write(epic.get("description", ""))
            for story in epic.get("stories", []):
                st.markdown(f"**• {story['title']}**  \n_Priority: {story.get('priority', 'Medium')}_")
                st.markdown(f"> {story.get('description', '')}")
                if story.get("acceptance_criteria"):
                    st.markdown("**Acceptance Criteria:**")
                    for ac in story["acceptance_criteria"]:
                        st.markdown(f"- {ac}")
                st.markdown("---")

    st.divider()
    if st.button("🚀 Push Backlog to Jira"):
        if not all([jira_url, jira_email, jira_token, jira_project_key]):
            st.error("Fill in all Jira settings in the sidebar first.")
        else:
            with st.spinner("Creating issues in Jira..."):
                results = push_to_jira(
                    backlog, jira_url, jira_email, jira_token, jira_project_key
                )
            st.success(f"Created {len(results)} issues in Jira.")
            for r in results:
                st.write(f"- [{r['key']}]({jira_url}/browse/{r['key']}) — {r['summary']}")

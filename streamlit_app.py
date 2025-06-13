# streamlit_app.py

import streamlit as st
from main import app  # import the LangGraph app
import time

st.set_page_config(page_title="Agentic Workflow Demo", layout="centered")

st.title("PRSR Plan + Refine + Solve + Reflect")
st.caption("Built using LangGraph + Claude 3 on OpenRouter")

task_input = st.text_area("📝 Enter your task here:", height=200)

if st.button("Run Agentic Workflow"):
    if not task_input.strip():
        st.warning("Please enter a task.")
    else:
        with st.spinner("Thinking..."):
            try:
                result = app.invoke({"input": task_input})
                st.success("✅ Final Output")
                for i, r in enumerate(result["results"], start=1):
                    st.markdown(f"**{i}.** {r}")
            except Exception as e:
                st.error("❌ Something went wrong")
                st.code(str(e))

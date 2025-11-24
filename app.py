import streamlit as st
import pandas as pd
import os
from job_agent.main import run_job_agent
from job_agent.user_profile import UserProfile

st.set_page_config(page_title="AI Job Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Job Application Agent")
st.markdown(f"**User:** {UserProfile.NAME} | **Location:** {UserProfile.LOCATION}")

# Sidebar for configuration
st.sidebar.header("Configuration")

default_keywords = "Data Scientist, Machine Learning Engineer, AI Engineer"
keywords_input = st.sidebar.text_area("Keywords (comma separated)", default_keywords)
keywords = [k.strip() for k in keywords_input.split(",")]

default_locations = "Hyderabad, Bangalore, Pune, Remote"
locations_input = st.sidebar.text_area("Locations (comma separated)", default_locations)
locations = [l.strip() for l in locations_input.split(",")]

resume_exists = os.path.exists(UserProfile.RESUME_PATH)
if resume_exists:
    st.sidebar.success(f"✅ Resume found: {UserProfile.RESUME_PATH}")
else:
    st.sidebar.error(f"❌ Resume not found at {UserProfile.RESUME_PATH}")

# Main area
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Search Jobs", type="primary"):
        if not resume_exists:
            st.error("Please add your resume file before searching.")
        else:
            with st.status("Searching for jobs...", expanded=True) as status:
                st.write("Initializing browser...")
                try:
                    results = run_job_agent(keywords, locations, apply_mode=False)
                    
                    if results is not None and not results.empty:
                        status.update(label="Search complete!", state="complete", expanded=False)
                        st.session_state['results'] = results
                        st.success(f"Found {len(results)} jobs.")
                    else:
                        status.update(label="No jobs found.", state="error", expanded=False)
                        st.warning("No jobs found matching your criteria.")
                        if os.path.exists("debug_screenshot.png"):
                            st.image("debug_screenshot.png", caption="Debug Screenshot (What the agent saw)")
                except Exception as e:
                    import traceback
                    status.update(label="Error occurred!", state="error", expanded=False)
                    st.error(f"An error occurred: {e}")
                    st.code(traceback.format_exc())
                    st.error("Tip: Ensure Chrome is closed and you have internet access.")

with col2:
    if 'results' in st.session_state and not st.session_state['results'].empty:
        if st.button("🚀 Apply to All Found Jobs", type="secondary"):
             with st.status("Applying to jobs...", expanded=True) as status:
                st.write("Starting application process...")
                # Re-run with apply_mode=True. 
                # Note: This re-runs search which isn't ideal but safe for MVP.
                # Optimization: Pass the results to apply directly if refactored further.
                run_job_agent(keywords, locations, apply_mode=True)
                status.update(label="Application process finished!", state="complete", expanded=False)
                st.success("Application process completed. Check logs for details.")

# Display results
if 'results' in st.session_state and not st.session_state['results'].empty:
    st.subheader("Search Results")
    st.dataframe(st.session_state['results'], use_container_width=True)

import streamlit as st

# -------------------------------
# Initialize session state
# -------------------------------
if "compare_replace_tasks" not in st.session_state:
    st.session_state.compare_replace_tasks = []

if "auto_lookup_tasks" not in st.session_state:
    st.session_state.auto_lookup_tasks = []

# -------------------------------
# Available Options
# -------------------------------
compare_replace_options = ["Compare Customers", "Replace Airlines", "Match Branch Codes"]
auto_lookup_options = ["Auto Lookup Fare", "Auto Lookup Taxes", "Auto Lookup Segments"]

# Filter options (remove already selected ones)
available_compare_replace = [opt for opt in compare_replace_options if opt not in st.session_state.compare_replace_tasks]
available_auto_lookup = [opt for opt in auto_lookup_options if opt not in st.session_state.auto_lookup_tasks]

# -------------------------------
# UI Layout
# -------------------------------
st.set_page_config(page_title="Automation Tool", layout="wide")
st.title("Automation Tool - Task Manager")

# -------------------------------
# Compare & Replace Module (First)
# -------------------------------
with st.expander("🔄 Compare & Replace Module", expanded=True):
    st.write("Manage your Compare & Replace tasks here:")

    col1, col2 = st.columns([3,1])
    with col1:
        selected_compare = st.selectbox(
            "Select a Compare & Replace task to add:",
            options=[""] + available_compare_replace,
            key="compare_select"
        )
    with col2:
        if st.button("➕ Add Compare & Replace", key="add_compare"):
            if selected_compare and selected_compare not in st.session_state.compare_replace_tasks:
                st.session_state.compare_replace_tasks.append(selected_compare)
                st.session_state.compare_select = ""  # Reset dropdown

    # Display Task Pane
    if st.session_state.compare_replace_tasks:
        st.write("### Current Compare & Replace Tasks")
        for idx, task in enumerate(st.session_state.compare_replace_tasks):
            col1, col2 = st.columns([5,1])
            with col1:
                st.write(f"- {task}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_compare_{idx}"):
                    st.session_state.compare_replace_tasks.pop(idx)
                    st.rerun()

# -------------------------------
# Auto Lookup Module (Second)
# -------------------------------
with st.expander("🔍 Auto Lookup Module", expanded=True):
    st.write("Manage your Auto Lookup tasks here:")

    col1, col2 = st.columns([3,1])
    with col1:
        selected_lookup = st.selectbox(
            "Select an Auto Lookup task to add:",
            options=[""] + available_auto_lookup,
            key="lookup_select"
        )
    with col2:
        if st.button("➕ Add Auto Lookup", key="add_lookup"):
            if selected_lookup and selected_lookup not in st.session_state.auto_lookup_tasks:
                st.session_state.auto_lookup_tasks.append(selected_lookup)
                st.session_state.lookup_select = ""  # Reset dropdown

    # Display Task Pane
    if st.session_state.auto_lookup_tasks:
        st.write("### Current Auto Lookup Tasks")
        for idx, task in enumerate(st.session_state.auto_lookup_tasks):
            col1, col2 = st.columns([5,1])
            with col1:
                st.write(f"- {task}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_lookup_{idx}"):
                    st.session_state.auto_lookup_tasks.pop(idx)
                    st.rerun()

# -------------------------------
# Summary Section
# -------------------------------
st.write("---")
st.subheader("📋 Final Task Summary")
st.write("Compare & Replace Tasks:", st.session_state.compare_replace_tasks)
st.write("Auto Lookup Tasks:", st.session_state.auto_lookup_tasks)

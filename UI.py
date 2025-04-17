import streamlit as st
import requests
from datetime import date, datetime

API_URL = "http://localhost:8000"
st.set_page_config(page_title="📟 To-Do Dashboard", layout="wide")

# --- CSS Styling ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap" rel="stylesheet">
<style>
html, body, [class*="st-"] {
    font-family: 'EB Garamond', serif !important;
    color: #000 !important;
}
.stButton > button {
    background-color: #cfefff !important;
    color: black !important;
    border: none !important;
    font-size: 0.75rem !important;
    padding: 0.25rem 0.6rem !important;
    border-radius: 50px !important;
    margin: 0.2rem 0.3rem !important;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
.sidebar-button .stButton > button {
    width: 100% !important;
    font-size: 15px !important;
    padding: 0.4rem 0.6rem !important;
    margin-bottom: 0.5rem;
    border-radius: 10px !important;
    background-color: #cfefff !important;
}
.page-title {
    font-size: 28px;
    font-weight: 700;
    padding: 0.3rem 1rem;
    margin-bottom: 1rem;
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
    text-align: center;
}
.task-left {
    display: flex;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
}
.task-desc {
    font-size: 14px;
    color: #000;
    margin-left: 1.5rem;
}
.center-save {
    display: flex;
    justify-content: center;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar Page Title ---
st.sidebar.markdown("<div class='page-title'>📟 To-Do Dashboard</div>", unsafe_allow_html=True)

# --- Sidebar Navigation ---
if "section" not in st.session_state:
    st.session_state.section = "➕ Add New Task"
if "editing_task_id" not in st.session_state:
    st.session_state.editing_task_id = None

with st.sidebar.container():
    st.markdown("<div class='sidebar-button'>", unsafe_allow_html=True)
    if st.button("➕ Add New Task"):
        st.session_state.section = "➕ Add New Task"
        st.session_state.editing_task_id = None
    if st.button("📋 Current Tasks"):
        st.session_state.section = "📋 Current Tasks"
        st.session_state.editing_task_id = None
    if st.button("✅ Completed Tasks"):
        st.session_state.section = "✅ Completed Tasks"
        st.session_state.editing_task_id = None
    st.markdown("</div>", unsafe_allow_html=True)

section = st.session_state.section

priority_map = {"🔴 High": "High", "🟡 Medium": "Medium", "🟢 Low": "Low"}
priority_display = list(priority_map.keys())
def get_priority_dot(priority):
    return {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "🟢")

if section == "➕ Add New Task":
    st.markdown("<div class='section-title'>➕ Add New Task</div>", unsafe_allow_html=True)

    if "task_add_status" not in st.session_state:
        st.session_state.task_add_status = ""

    if "task_form_data" not in st.session_state:
        st.session_state.task_form_data = {
            "title": "",
            "description": "",
            "priority": "🟢 Low",
            "deadline": date.today()
        }

    with st.form("add_task_form", clear_on_submit=False):
        title = st.text_input("Title", value=st.session_state.task_form_data["title"], placeholder="e.g. Buy groceries")
        description = st.text_area("Description", value=st.session_state.task_form_data["description"], placeholder="e.g. Milk, Bread, Eggs")
        col1, col2 = st.columns(2)
        with col1:
            selected_priority = st.selectbox("Priority", priority_display, index=priority_display.index(st.session_state.task_form_data["priority"]))
        with col2:
            use_deadline_checked = st.checkbox("Set a deadline")

        deadline = None
        if use_deadline_checked:
            deadline = st.date_input("Deadline", key="add_deadline", value=date.today(), min_value=date.today())

        submitted = st.form_submit_button("✅ Add Task")

        if submitted:
            if not title.strip() or not description.strip():
                st.session_state.task_add_status = "error"
            else:
                payload = {
                    "title": title,
                    "description": description,
                    "priority": priority_map[selected_priority],
                    "deadline": str(deadline) if use_deadline_checked else None
                }

                response = requests.post(f"{API_URL}/tasks/", json=payload)

                if response.status_code == 200:
                    st.session_state.task_add_status = "success"
                    st.session_state.task_form_data = {
                        "title": "",
                        "description": "",
                        "priority": "🟢 Low",
                        "deadline": date.today()
                    }
                else:
                    st.session_state.task_add_status = "fail"
            st.rerun()

    if st.session_state.task_add_status == "success":
        st.success("✅ Task added successfully!")
        st.session_state.task_add_status = ""
    elif st.session_state.task_add_status == "fail":
        st.error("❌ Failed to add task.")
        st.session_state.task_add_status = ""
    elif st.session_state.task_add_status == "error":
        st.error("Please fill both Title and Description.")
        st.session_state.task_add_status = ""


# --- Render Task Function ---
def render_task(task, completed=False):
    key = str(task["id"])
    edit_key = f"edit_mode_{key}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

    if st.session_state["editing_task_id"] and st.session_state["editing_task_id"] != task["id"]:
        return

    if st.session_state[edit_key]:
        new_title = st.text_input("Title", value=task["title"], key=f"title_{key}")
        new_desc = st.text_area("Description", value=task["description"], key=f"desc_{key}")
        try:
            deadline_raw = task.get("deadline")
            parsed_deadline = datetime.strptime(deadline_raw, "%Y-%m-%d").date() if deadline_raw else None
        except:
            parsed_deadline = None

        use_deadline = st.checkbox("Set a deadline", value=parsed_deadline is not None, key=f"deadline_checkbox_{key}")
        new_deadline = st.date_input("Deadline", value=parsed_deadline or date.today(), key=f"deadline_{key}") if use_deadline else None

        new_priority = st.selectbox("Priority", priority_display,
                                    index=["High", "Medium", "Low"].index(task["priority"]),
                                    key=f"priority_{key}")
        st.markdown('<div class="center-save">', unsafe_allow_html=True)
        col_save, col_cancel = st.columns([1, 1])
        with col_save:
            if st.button("💾 Save", key=f"save_{key}"):
                payload = {
                    "title": new_title,
                    "description": new_desc,
                    "priority": priority_map[new_priority],
                    "deadline": str(new_deadline) if new_deadline else None
                }
                r = requests.put(f"{API_URL}/tasks/{task['id']}/edit", json=payload)
                if r.status_code == 200:
                    st.session_state[edit_key] = False
                    st.session_state["editing_task_id"] = None
                    st.rerun()
        with col_cancel:
            if st.button("❌ Cancel", key=f"cancel_{key}"):
                st.session_state[edit_key] = False
                st.session_state["editing_task_id"] = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    left_col, right_col = st.columns([6, 2])
    with left_col:
        st.markdown(
            f"<div class='task-left' title='{task['priority']} Priority'>{get_priority_dot(task['priority'])}&nbsp;&nbsp;{task['title']}</div>",
            unsafe_allow_html=True
        )
    with right_col:
        col1, col2, col3 = st.columns(3)
        with col1:
            label = "✅" if not completed else "↩️"
            if st.button(label, key=f"toggle_{key}"):
                requests.put(f"{API_URL}/tasks/{task['id']}/toggle")
                st.rerun()
        with col2:
            if not completed and st.button("✏️", key=f"edit_{key}"):
                st.session_state[edit_key] = True
                st.session_state["editing_task_id"] = task["id"]
                st.rerun()
        with col3:
            if st.button("🗑️", key=f"delete_{key}"):
                requests.delete(f"{API_URL}/tasks/{task['id']}")
                st.rerun()

    if task.get("description"):
        st.markdown(f"<div class='task-desc'>{task['description']}</div>", unsafe_allow_html=True)
    if task.get("deadline"):
        st.markdown(f"<div class='task-desc'>📅 Due: {task['deadline']}</div>", unsafe_allow_html=True)
    st.markdown("---")

# --- Fetch Tasks ---
response = requests.get(f"{API_URL}/tasks/")
if response.status_code != 200:
    st.error("Failed to fetch tasks.")
    st.stop()

tasks = response.json()
incomplete_tasks = [t for t in tasks if not t["completed"]]
completed_tasks = [t for t in tasks if t["completed"]]

# --- Display Sections ---
if section == "📋 Current Tasks":
    left, right = st.columns([6, 1])
    with left:
        st.markdown(f"<div class='section-title'>📋 Current Tasks ({len(incomplete_tasks)})</div>", unsafe_allow_html=True)
    with right:
        priority_filter = st.selectbox("Filter", ["All", "High", "Medium", "Low"], key="priority_filter")

    if priority_filter != "All":
        incomplete_tasks = [t for t in incomplete_tasks if t["priority"] == priority_filter]

    for task in incomplete_tasks:
        render_task(task)

elif section == "✅ Completed Tasks":
    st.markdown(f"<div class='section-title'>✅ Completed Tasks ({len(completed_tasks)})</div>", unsafe_allow_html=True)
    for task in completed_tasks:
        render_task(task, completed=True)

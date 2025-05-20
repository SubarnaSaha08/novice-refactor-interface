import streamlit as st
import time
from streamlit.components.v1 import html

def show_task_page():
    index = st.session_state.current_index
    problem = st.session_state.problems[index]
    session_id = st.session_state.session_id

    # Set start time if not already set or task changed
    if "start_time" not in st.session_state or st.session_state.get("current_index") != index:
        st.session_state.start_time = time.time()
        st.session_state.current_index = index

    st.subheader(f"Problem {index+1}: {problem['question']}")
    st.markdown("[See Instructions](https://docs.google.com/document/d/1kg68XyJLMlI3LZbRfUmfuqVoirruVKe2VVsVebf3TKE/edit?tab=t.0#heading=h.3c80ktufw1pg)", unsafe_allow_html=True)
    if session_id == 2:
        st.markdown("[Use RefactorGPT](https://chatgpt.com/g/g-6801a23d42488191bd410191cd8512a1-beginner-code-refactor)", unsafe_allow_html=True)
    st.code(problem["code"])

    # Timer display with JavaScript
    start_time = st.session_state.start_time
    timer_html = f"""
    <div id="timer_{index}" style="font-size: 18px; margin-bottom: 10px; color: white;">
        Elapsed Time: <span id="elapsed_{index}">00:00</span>
    </div>
    <script>
        function updateTimer() {{
            try {{
                var start = {start_time * 1000};
                var now = Date.now();
                var elapsed = Math.floor((now - start) / 1000);
                var minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
                var seconds = (elapsed % 60).toString().padStart(2, '0');
                document.getElementById('elapsed_{index}').innerText = minutes + ':' + seconds;
            }} catch (e) {{
                console.error('Timer error:', e);
            }}
        }}
        updateTimer();
        setInterval(updateTimer, 1000);
    </script>
    """
    html(timer_html, height=40)

    if st.button("➡️ Next", key=f"responses_for_task_{index}"):
        st.session_state.page = "response_form_page"
        st.rerun()
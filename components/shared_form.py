import streamlit as st
from data.save_responses import autosave_user_responses


def render_form(problem, response_data):
    pid = problem["id"]
    username = st.session_state.username
    session_id = st.session_state.session_id

    # Ensure response dict for this problem id exists in session_state.responses
    response_key = f"response_{pid}"
    if response_key not in st.session_state.responses:
        st.session_state.responses[response_key] = {}
    # Use the session state dict as the response_data to keep it in sync
    response_data = st.session_state.responses[response_key]

    def field(key, label, options):
        full_key = f"{key}_{pid}"
        current_val = response_data.get(key)
        selected = st.radio(
            label,
            options,
            index=options.index(current_val) if current_val in options else 0,
            key=full_key,
        )
        if selected != current_val:
            response_data[key] = selected
            st.session_state.responses[response_key] = response_data
            autosave_user_responses(st.session_state.responses, username)
    
    if session_id == 1:
        # --- Section A: Code Comprehension Assessment ---
        st.subheader("**Section A: Code Comprehension Assessment**")
        st.write("Please answer the following questions regarding your understanding of the code:")

        field("difficulty", "How difficult do you find the problem? (সমস্যাটি আপনার কাছে কতটা কঠিন মনে হয়?)", [None, 1, 2, 3, 4, 5])
        field(
            "code_understanding",
            "How clearly do you understand the purpose of the given code? (আপনি প্রদত্ত কোডের উদ্দেশ্য কতটা স্পষ্টভাবে বুঝতে পেরেছেন?)",
            [None, 1, 2, 3, 4, 5]
        )
        field(
            "logic_flow",
            "How well do you understand the flow of logic in the given code? (আপনি দেওয়া কোডের লজিকের প্রবাহ কতটা ভালোভাবে বুঝতে পারেন?)",
            [None, 1, 2, 3, 4, 5],
        )
        field(
            "function_identification",
            "Can you identify key functions and their purposes? (আপনি কি মূল ফাংশন এবং তাদের উদ্দেশ্য চিহ্নিত করতে পারেন?)",
            [None, 1, 2, 3, 4, 5],
        )
        field("code_structure", "How well is the code structured? (কোডটি কতটা ভালোভাবে গঠিত?)", [None, 1, 2, 3, 4, 5])

        for open_key, label in [
            ("open_ended_1", "Briefly describe what the code is doing (কোডটি কী করছে তা সংক্ষেপে বর্ণনা করুন):"),
            ("open_ended_2", "List any sections of the code that you find particularly confusing (কোডের কোনো অংশ যা আপনি বিশেষভাবে বিভ্রান্তিকর মনে করেন তা তালিকাভুক্ত করুন):"),
        ]:
            full_key = f"{open_key}_{pid}"
            val = st.text_area(label, key=full_key, value=response_data.get(open_key, ""))
            if val != response_data.get(open_key):
                response_data[open_key] = val
                st.session_state.responses[response_key] = response_data
                autosave_user_responses(st.session_state.responses, username)

        # --- Section B: Cognitive Load Assessment ---
        st.markdown("---")
        st.subheader("**Section B: Cognitive Load Assessment**")
        st.write("Rate your experience during the independent refactoring task (1 - Not at all, 5 - Extremely):")

        # NASA-TLX
        descriptions = {
            "mental_demand": "Mental Demand: How mentally demanding was the task? (কাজটি কতটা মানসিকভাবে চাহিদাসম্পন্ন ছিল?)",
            "physical_demand": "Physical Demand: How physically demanding was the task? (কাজটি কতটা শারীরিকভাবে চাহিদাসম্পন্ন ছিল?)",
            "temporal_demand": "Temporal Demand: How hurried or rushed was the pace of the task? (কাজের গতি কতটা তাড়াহুড়ো বা দ্রুত ছিল?)",
            "performance": "Performance: How successful were you in accomplishing what you were asked to do? (আপনি যা করতে বলা হয়েছিল তা কতটা সফলভাবে সম্পন্ন করেছেন?)",
            "effort": "Effort: How hard did you have to work to accomplish your level of performance? (আপনার কর্মক্ষমতার স্তর অর্জনের জন্য আপনাকে কতটা কঠোর পরিশ্রম করতে হয়েছিল?)",
            "frustration": "Frustration: How insecure, discouraged, irritated, stressed, and annoyed were you? (আপনি কতটা নিরাপত্তাহীন, হতোদ্যম, বিরক্ত, চাপগ্রস্ত এবং ক্ষুব্ধ ছিলেন?)",
        }

        for metric, description in descriptions.items():
            field(metric, description, [None, 1, 2, 3, 4, 5])
            
    elif session_id == 2:
            # --- Section A: Code Comprehension Assessment (Post-CodeRefactorGPT) ---
            st.subheader("**Section A: Code Comprehension Assessment (Post-CodeRefactorGPT)**")
            st.write("Please answer the following questions regarding your understanding of the code:")
            
            field(
                "code_understanding",
                "How clearly do you understand the purpose of the given code after CodeRefactorGPT guidance? (1 = Not at all clear, 5 = Very clear)", 
                [None, 1, 2, 3, 4, 5]
            )
            
            field(
                "logic_flow",
                "How well do you understand the flow of logic in the refactored code after   CodeRefactorGPT guidance? (1 = Very confusing, 5 = Very clear)",
                [None, 1, 2, 3, 4, 5],
            )
            field(
                "function_identification",
                "Can you identify the key functions and their purposes in the refactored code after CodeRefactorGPT guidance? (1 = Not at all, 5 = Completely)",
                [None, 1, 2, 3, 4, 5],
            )
            field(
                "code_structure",
                "How well is the code structured for readability and maintainability after CodeRefactorGPT guidance? (1 = Very poorly structured, 5 = Very well structured)",
                [None, 1, 2, 3, 4, 5]
            )

            for open_key, label in [
                ("open_ended_1", "Briefly describe what the refactored code is doing:"),
                ("open_ended_2", "Which sections of the code became clearer after CodeRefactorGPT guidance?"),
            ]:
                full_key = f"{open_key}_{pid}"
                val = st.text_area(label, key=full_key, value=response_data.get(open_key, ""))
                if val != response_data.get(open_key):
                    response_data[open_key] = val
                    st.session_state.responses[response_key] = response_data
                    autosave_user_responses(st.session_state.responses, username)

            # --- Section B: Cognitive Load Assessment ---
            st.markdown("---")
            st.subheader("**Section B: Cognitive Load Assessment**")
            st.write("Rate your experience during the independent refactoring task (1 = Not at all, 5 = Extremely):")

            # NASA-TLX
            descriptions = {
                "mental_demand": "Mental Demand: How mentally demanding was the task after receiving CodeRefactorGPT guidance?",
                "physical_demand": "Physical Demand: How physically demanding was the task?",
                "temporal_demand": "Temporal Demand: How hurried or rushed did you feel during the task?",
                "performance": "Performance: How successful were you in achieving the refactoring goals after CodeRefactorGPT guidance?",
                "effort": "Effort: How hard did you have to work to accomplish the task after CodeRefactorGPT guidance?",
                "frustration": "Frustration: How insecure, discouraged, irritated, stressed, and annoyed did you feel during the task after CodeRefactorGPT guidance?",
            }

            for metric, description in descriptions.items():
                field(metric, description, [None, 1, 2, 3, 4, 5])
            
            # --- Section C: Perceived Learning and Effectiveness of Assistance ---
            st.subheader("**Section C: Perceived Learning and Effectiveness of Assistance**")
            st.write("Please rate how the assistance impacted your learning")
            
            field(
                "overall_effectiveness",
                "How effective was the guidance in helping you refactor the code? (1 = Not at all effective, 5 = Very effective)", 
                [None, 1, 2, 3, 4, 5]
            )
            
            field(
                "support_for_learning",
                "To what extent did the guidance support your understanding of how to structure functions and organize code logically? (1 = Not at all, 5 = Very much)", 
                [None, 1, 2, 3, 4, 5]
            )
            
            for open_key, label in [
                ("application_of_new_strategies", "Did you learn any new strategies for breaking down functions or organizing code? (If yes, please specify):"),
            ]:
                full_key = f"{open_key}_{pid}"
                val = st.text_area(label, key=full_key, value=response_data.get(open_key, ""))
                if val != response_data.get(open_key):
                    response_data[open_key] = val
                    st.session_state.responses[response_key] = response_data
                    autosave_user_responses(st.session_state.responses, username)
            
            field(
                "confidence_boost",
                "How much did the guidance increase your confidence in refactoring code? (1 = Not at all, 5 = A great deal)", 
                [None, 1, 2, 3, 4, 5]
            )
            
            field(
                "impact_on_approach",
                "How likely are you to apply the strategies you learned to future refactoring tasks? (1 = Not likely, 5 = Very likely)", 
                [None, 1, 2, 3, 4, 5]
            )
            
            for open_key, label in [
                ("open_ended_3", "What specific aspects of the guidance were most helpful in improving your approach to refactoring? (Open-ended)")
            ]:
                full_key = f"{open_key}_{pid}"
                val = st.text_area(label, key=full_key, value=response_data.get(open_key, ""))
                if val != response_data.get(open_key):
                    response_data[open_key] = val
                    st.session_state.responses[response_key] = response_data
                    autosave_user_responses(st.session_state.responses, username)

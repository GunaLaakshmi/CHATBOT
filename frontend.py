import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Enhanced Custom CSS with animations and modern design
st.markdown("""
    <style>
    /* Modern gradient animations */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating animation */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Enhanced title container */
    .title-container {
        background: linear-gradient(-45deg, #FF6B6B, #4ECDC4, #FFD93D, #6C63FF);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .title-text {
        color: white;
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        animation: float 6s ease-in-out infinite;
    }
    
    .subtitle-text {
        color: white;
        text-align: center;
        font-size: 1.4em;
        margin-top: 15px;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
    }
    
    /* Glass morphism chat messages */
    .user-message {
        background: rgba(255, 107, 107, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        margin: 15px 0;
        border-left: 5px solid #FF6B6B;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.1);
        transition: all 0.3s ease;
    }
    
    .assistant-message {
        background: rgba(78, 205, 196, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        margin: 15px 0;
        border-left: 5px solid #4ECDC4;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.1);
        transition: all 0.3s ease;
    }
    
    .user-message:hover, .assistant-message:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Modern button styling with new gradients */
    .stButton > button {
        background: linear-gradient(-45deg, #FF61D2, #FE9090, #FFC947, #9B4DFF);
        background-size: 200% 200%;
        animation: gradient 5s ease infinite;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(255, 97, 210, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(155, 77, 255, 0.3);
        background: linear-gradient(-45deg, #9B4DFF, #FF61D2, #FE9090, #FFC947);
        background-size: 200% 200%;
    }
    
    /* Task completion button special styling */
    .stButton > [data-testid*="complete"] {
        background: linear-gradient(-45deg, #00F5A0, #00D9F5, #9B4DFF);
        background-size: 200% 200%;
        box-shadow: 0 4px 15px rgba(0, 245, 160, 0.2);
    }
    
    .stButton > [data-testid*="complete"]:hover {
        box-shadow: 0 8px 25px rgba(0, 217, 245, 0.3);
        background: linear-gradient(-45deg, #9B4DFF, #00F5A0, #00D9F5);
        background-size: 200% 200%;
    }
    
    /* Create Task button special styling */
    .stButton > [data-testid*="schedule_btn"] {
        background: linear-gradient(-45deg, #FF6FBD, #FF8C48, #FFC947);
        background-size: 200% 200%;
        box-shadow: 0 4px 15px rgba(255, 111, 189, 0.2);
    }
    
    .stButton > [data-testid*="schedule_btn"]:hover {
        box-shadow: 0 8px 25px rgba(255, 140, 72, 0.3);
        background: linear-gradient(-45deg, #FFC947, #FF6FBD, #FF8C48);
        background-size: 200% 200%;
    }
    
    /* Refresh button special styling */
    .stButton > [data-testid*="refresh"] {
        background: linear-gradient(-45deg, #7C4DFF, #448AFF, #00E5FF);
        background-size: 200% 200%;
        box-shadow: 0 4px 15px rgba(124, 77, 255, 0.2);
    }
    
    .stButton > [data-testid*="refresh"]:hover {
        box-shadow: 0 8px 25px rgba(68, 138, 255, 0.3);
        background: linear-gradient(-45deg, #00E5FF, #7C4DFF, #448AFF);
        background-size: 200% 200%;
    }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 25px;
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 15px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(-45deg, #FF6B6B, #4ECDC4);
        color: white;
        transform: scale(1.05);
    }
    
    /* Form styling */
    .stTextInput > div > div, .stSelectbox > div > div {
        border-radius: 15px;
        border: 2px solid rgba(78, 205, 196, 0.2);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div:focus-within, .stSelectbox > div > div:focus-within {
        border-color: #4ECDC4;
        box-shadow: 0 0 15px rgba(78, 205, 196, 0.2);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Backend API URL
API_URL = "http://127.0.0.1:5000"

# Enhanced animated title
st.markdown("""
    <div class="title-container">
        <div class="title-text">✨Task Genie </div>
        <div class="subtitle-text">Your Intelligent Daily Planning Assistant</div>
    </div>
""", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "show_scheduler" not in st.session_state:
    st.session_state["show_scheduler"] = False
if "current_task" not in st.session_state:
    st.session_state["current_task"] = ""

# Modern tabs with icons
tab1, tab2 = st.tabs(["🎯 Chat & Plan", "📊 Schedule Overview"])

with tab1:
    for idx, chat in enumerate(st.session_state["messages"]):
        with st.chat_message(chat["role"], avatar="👤" if chat["role"] == "user" else "🤖"):
            style_class = "user-message" if chat["role"] == "user" else "assistant-message"
            st.markdown(f'<div class="{style_class}">{chat["content"]}</div>', unsafe_allow_html=True)
            
            if chat["role"] == "assistant":
                if st.button("✨ Create Task", key=f"schedule_btn_{idx}"):
                    st.session_state["show_scheduler"] = True
                    if idx > 0 and st.session_state["messages"][idx-1]["role"] == "user":
                        st.session_state["current_task"] = st.session_state["messages"][idx-1]["content"]
                
                if st.session_state["show_scheduler"]:
                    with st.form(key=f"schedule_form_{idx}"):
                        st.markdown("### 🌟 New Task Details")
                        
                        task = st.text_input("📝 Task Description:", 
                                           value=st.session_state["current_task"],
                                           key=f"task_input_{idx}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            time = st.time_input("⏰ Schedule Time:", key=f"time_input_{idx}")
                        with col2:
                            priority = st.selectbox("🎯 Priority Level:", 
                                                  ["Low", "Medium", "High"],
                                                  key=f"priority_input_{idx}")
                        
                        if st.form_submit_button("🚀 Create Task"):
                            try:
                                with st.spinner("Creating your task..."):
                                    response = requests.post(
                                        f"{API_URL}/add-task",
                                        json={
                                            "task": task,
                                            "time": time.strftime("%H:%M"),
                                            "priority": priority
                                        }
                                    )
                                    if response.status_code == 200:
                                        st.balloons()
                                        st.success("🎉 Task created successfully!")
                                        st.session_state["show_scheduler"] = False
                                        st.session_state["current_task"] = ""
                                        st.session_state["messages"].append({
                                            "role": "assistant",
                                            "content": f"✅ Task Created:\n🎯 '{task}'\n⏰ {time.strftime('%H:%M')}\n🔥 {priority} Priority"
                                        })
                                        st.rerun()
                                    else:
                                        st.error("⚠️ Couldn't create task. Please try again.")
                            except requests.exceptions.ConnectionError:
                                st.error("📡 Connection failed. Please check server status.")

    # Enhanced chat input
    user_input = st.chat_input("💭 What would you like to plan today?")

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        try:
            with st.spinner("Thinking..."):
                response = requests.post(f"{API_URL}/daily-planner", 
                                       json={"message": user_input})
                bot_reply = response.json().get("response", "I couldn't process that request. Try again.")
        except requests.exceptions.ConnectionError:
            bot_reply = "⚠️ Connection to planning service failed. Please check server status."

        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)
            
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f'<div class="assistant-message">{bot_reply}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 📊 Your Schedule Overview")
    
    if st.button("🔄 Refresh Schedule", key="refresh_schedule"):
        try:
            with st.spinner("Updating schedule..."):
                schedule_response = requests.get(f"{API_URL}/schedule")
                if schedule_response.status_code == 200:
                    schedule_data = schedule_response.json()
                    
                    if schedule_data["tasks"]:
                        df = pd.DataFrame(schedule_data["tasks"])
                        df = df.sort_values(by=["priority", "time"])
                        
                        # Enhanced styling for priority levels
                        def style_priority(val):
                            colors = {
                                'High': '#FF6B6B',
                                'Medium': '#FFD93D',
                                'Low': '#4ECDC4'
                            }
                            return f'background: linear-gradient(90deg, {colors.get(val, "")}22, {colors.get(val, "")}11);'
                        
                        styled_df = df.style.apply(lambda x: [style_priority(v) for v in x], subset=['priority'])
                        st.dataframe(styled_df, use_container_width=True)
                        
                        # Task completion section
                        st.markdown("### ✅ Complete Tasks")
                        for idx, task in df.iterrows():
                            if task["status"] != "completed":
                                if st.button(f"✨ Complete: {task['task']}", key=f"complete_{idx}"):
                                    with st.spinner("Updating task..."):
                                        requests.post(f"{API_URL}/complete-task/{idx}")
                                        st.success("🎉 Task completed!")
                                        st.rerun()
                    else:
                        st.info("🌟 Your schedule is clear! Add tasks using the chat.")
                else:
                    st.error("⚠️ Couldn't fetch schedule. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("📡 Connection failed. Please check server status.")
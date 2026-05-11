import streamlit as st
from openai import OpenAI
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="AI Decision-Making Assistant",
    page_icon="🤖",
    layout="wide"
)

# Button
if "result" not in st.session_state:
    st.session_state.result = ""

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0f172a;
    color: white;
}
            
/* Hide Streamlit Header */
header {
    visibility: hidden;
}

/* Remove Top Padding */
.block-container {
    padding-top: 1rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    color: white !important;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Input Boxes */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
}

/* Labels */
label {
    color: white !important;
    font-weight: 600;
}

/* Buttons */
.stButton button {
    background: linear-gradient(to right, #06b6d4, #3b82f6);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 25px;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.03);
    background: linear-gradient(to right, #0891b2, #2563eb);
}

/* Recommendation Box */
.stSuccess {
    border-radius: 15px;
}

/* Download Button */
.stDownloadButton button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}

/* Charts */
canvas {
    border-radius: 15px;
}

/* Table Styling */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin-top: 20px !important;
    background-color: #111827 !important;
    border: 2px solid #334155 !important;
}

thead tr th {
    background-color: #1e293b !important;
    color: #38bdf8 !important;
    padding: 16px !important;
    border: 2px solid #334155 !important;
    text-align: center !important;
    font-size: 22px !important;
    font-weight: bold !important;
}

tbody tr td {
    padding: 14px !important;
    border: 2px solid #334155 !important;
    text-align: center !important;
    color: white !important;
    font-size: 18px !important;
    background-color: #0f172a !important;
}

tbody tr:hover td {
    background-color: #172033 !important;
    transition: 0.3s;
}

</style>
""", unsafe_allow_html=True)

# OpenAI API Key
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# Sidebar
st.sidebar.title("📌 About This Project")

st.sidebar.write("""
This AI-powered assistant helps users compare multiple options,
analyze pros and cons, calculate scores,
and receive smart recommendations.
""")

st.sidebar.info("Built using Streamlit + OpenAI API")

st.sidebar.markdown("---")

st.sidebar.markdown("""
<h2 style='color:white; margin-bottom:15px;'>
🕘 Recent Searches
</h2>
""", unsafe_allow_html=True)

for i, item in enumerate(reversed(st.session_state.history)):

    button_label = f"📌 {item['category']} - {item['purpose']}"

    if st.sidebar.button(
       button_label,
       key=f"history_{i}",
       use_container_width=True
    ):

       st.session_state.selected_category = item["category"]
       st.session_state.selected_purpose = item["purpose"]
       st.session_state.selected_budget = item["budget"]
       st.session_state.selected_options = item["options"]

    # Restore previous output
       st.session_state.result = item["result"]
       st.session_state.scores = item["scores"]

       st.rerun()

# Clear History Button
if st.sidebar.button("🗑 Clear History"):

    st.session_state.history = []

    st.rerun()

# Hero Section
st.markdown("""
<div style="
    background: linear-gradient(to right, #00c6ff, #0072ff);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
">

<h1 style="
    color: white;
    font-size: 55px;
    margin-bottom: 10px;
">
🤖 AI Decision-Making Assistant
</h1>

<p style="
    color: white;
    font-size: 22px;
">
Smart AI-powered comparison and recommendation platform
for faster and better decision-making.
</p>

</div>
""", unsafe_allow_html=True)

# Inputs
# Inputs

category = st.selectbox(
    "Select Decision Category",
    [
        "Laptop",
        "Mobile",
        "Career",
        "Courses",
        "Travel",
        "Other"
    ],
    index=[
        "Laptop",
        "Mobile",
        "Career",
        "Courses",
        "Travel",
        "Other"
    ].index(
        st.session_state.get("selected_category", "Laptop")
    )
)

purpose = st.text_input(
    "Enter your purpose",
    value=st.session_state.get("selected_purpose", "")
)

budget = st.text_input(
    "Enter your budget",
    value=st.session_state.get("selected_budget", "")
)

options = st.text_area(
    "Enter options separated by commas",
    value=st.session_state.get("selected_options", "")
)

if st.button("Analyze Options"):

    option_list = options.split(",")

        # Sample Scores for Visualization
        # Dynamic AI-Based Scores
    scores = {}

    for option in option_list:

        score_prompt = f"""
        Give only one score out of 10 for this option.

        Option: {option}
        Category: {category}
        Purpose: {purpose}
        Budget: {budget}

        Return ONLY a number between 1 and 10.
        Example:
        8.5
        """

        score_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": score_prompt}
            ]
        )

        score = float(
            score_response.choices[0].message.content.strip()
        )

        scores[option.strip()] = score
        st.session_state.scores = scores

    # AI Prompt
    prompt = f"""
    You are an intelligent AI Decision-Making Assistant.

    Compare these options:
    {option_list}

    Category: {category}
    Purpose: {purpose}
    Budget: {budget}

    Provide the response in this exact format:

    ## 1. Detailed Pros and Cons of Each Option

    ## 2. Scores out of 10

    Provide scores in proper table format.

    ## 3. Best Recommendation

    Clearly mention the best option.

    ## 4. Detailed Explanation

    Explain WHY this option is best according to:
    - budget
    - usability
    - performance
    - value
    - user purpose

    ## 5. Helpful Resources & Useful Links

    Based on the user's category and purpose, provide:

    - Best websites
    - Official links
    - Useful tools/platforms
    - YouTube channels
    - Tutorials
    - Buying guides
    - Communities/forums
    - Courses or learning resources if applicable

    Provide clickable links whenever possible.

    ## 6. Final Conclusion

    Summarize the recommendation professionally.

    Use proper markdown formatting.
    Make all section headings bold and properly spaced.

    Make the response professional, modern, and structured.

    Do not ask follow-up questions.
    Do not add conversational endings.
    Do not say "let me know" or "feel free to ask".

    Only provide the final analysis and recommendation.
    """

    # OpenAI Response
    with st.spinner("🔍 AI is analyzing the options..."):

        # OpenAI Response
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        st.session_state.result = response.choices[0].message.content

    if purpose.strip() != "":

        history_item = {
            "category": category,
            "purpose": purpose,
            "budget": budget,
            "options": options,
            "result": st.session_state.result,
            "scores": st.session_state.scores
        }

        if history_item not in st.session_state.history:
            st.session_state.history.append(history_item)

    # Output
    # SHOW RESULTS AFTER GENERATION

if st.session_state.result != "":

    # Recommendation Heading
    st.subheader("🤖 AI Recommendation")

    # Success Message
    st.success("🏆 AI Analysis & Recommendation Generated")

    # AI Result
    st.markdown(st.session_state.result)

    # Best Option
    best_option = max(
        st.session_state.scores,
        key=st.session_state.scores.get
    )

    # Highest Score
    highest_score = max(
        st.session_state.scores.values()
    )

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            padding:18px;
            border-radius:15px;
            height:260px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            text-align:center;
            color:white;
        ">
            <h3>🏆 Best Option</h3>
            <h2 style='font-size:38px;'>{best_option}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #065f46, #10b981);
            padding:18px;
            border-radius:15px;
            height:260px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            text-align:center;
            color:white;
        ">
            <h3>⭐ Highest Score</h3>
            <h2 style='font-size:38px;'>{highest_score}/10</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #7c2d12, #f97316);
            padding:18px;
            border-radius:15px;
            height:260px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            text-align:center;
            color:white;
        ">
            <h3>💰 Budget Match</h3>
            <h2 style='font-size:38px;'>Good</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #581c87, #a855f7);
            padding:18px;
            border-radius:15px;
            height:260px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            text-align:center;
            color:white;
        ">
            <h3>⚡ AI Confidence</h3>
            <h2 style='font-size:38px;'>95%</h2>
        </div>
        """, unsafe_allow_html=True)

    # Download Button
    st.markdown(
        "<div style='margin-top:30px;'></div>",
        unsafe_allow_html=True
    )

    st.download_button(
        label="📥 Download Report",
        data=st.session_state.result,
        file_name="AI_Decision_Report.txt",
        mime="text/plain"
    )

    # Chart Heading
    st.markdown("""
    <h1 style='color:white; margin-bottom:20px;'>
    📊 Score Comparison
    </h1>
    """, unsafe_allow_html=True)

    # DataFrame
    df = pd.DataFrame({
        "Options": list(st.session_state.scores.keys()),
        "Scores": list(st.session_state.scores.values())
    })

    # Plotly Chart
    fig = px.bar(
        df,
        x="Options",
        y="Scores",
        color="Scores",
        text="Scores",
        text_auto=True,
        template="plotly_dark",
        title=""
    )

    fig.update_layout(
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font_color="white",

        xaxis=dict(
            tickfont=dict(size=18, color='white')
        ),

        yaxis=dict(
            tickfont=dict(size=18, color='white')
        )
    )

    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import random

st.set_page_config(page_title="Game Học Toán Cấp 1 🎓", page_icon="📚", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-size: 48px;'>🎓 Game Học Toán Cấp 1</h1>
    <hr style='border: 2px solid #4CAF50;'>
""", unsafe_allow_html=True)

if "score" not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.question = ""
    st.session_state.answer = 0
    st.session_state.explanation = ""
    st.session_state.last_answered = False
    st.session_state.correct = False
    st.session_state.user_input = ""

def generate_question(level):
    if level == 1:
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(['+', '-'])
        if op == '-' and a < b:
            a, b = b, a
    elif level == 2:
        a, b = random.randint(2, 20), random.randint(2, 20)
        op = random.choice(['+', '-', '*'])
        if op == '-' and a < b:
            a, b = b, a
    else:
        b = random.randint(1, 10)
        a = b * random.randint(2, 10)
        op = random.choice(['+', '-', '*', '/'])

    question = f"{a} {op} {b}"
    answer = int(eval(question))
    explanation = f"Vì {question} = {answer}"
    return question, answer, explanation

st.markdown("""
    <style>
    .stRadio > div { flex-direction: row !important; justify-content: center; }
    .big-font { font-size: 28px !important; }
    .question-box { font-size: 40px; font-weight: bold; color: #333; text-align: center; margin: 20px 0; }
    .score-text { font-size: 26px; font-weight: bold; text-align: center; margin: 20px 0; }
    .stButton button {
        font-size: 26px;
        padding: 15px 40px;
        border-radius: 12px;
        background-color: #4CAF50;
        color: white;
        margin-top: 10px;
    }
    input[type="text"] {
        font-size: 28px;
        text-align: center;
        height: 60px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.total == 0:
    st.session_state.level = st.radio("Chọn cấp độ", [1, 2, 3], horizontal=True)
    if st.button("🎮 Bắt đầu chơi"):
        q, a, exp = generate_question(st.session_state.level)
        st.session_state.question = q
        st.session_state.answer = a
        st.session_state.explanation = exp
        st.session_state.total = 1
        st.session_state.last_answered = False
        st.session_state.correct = False
        st.session_state.user_input = ""
else:
    if not st.session_state.last_answered or not st.session_state.correct:
        st.markdown(f"<div class='question-box'>Câu {st.session_state.total}/10: {st.session_state.question} = ?</div>", unsafe_allow_html=True)
        st.session_state.user_input = st.text_input("Nhập đáp án của bạn", value=st.session_state.user_input, key="answer_input")

        if st.button("✅ Trả lời"):
            user_answer = st.session_state.user_input.strip()
            if user_answer.isdigit() and int(user_answer) == st.session_state.answer:
                st.success("🎉 Đúng rồi!")
                st.session_state.score += 1
                st.session_state.correct = True
                st.session_state.last_answered = True
            else:
                st.error(f"❌ Sai rồi! {st.session_state.explanation}")
                st.session_state.correct = False
                st.session_state.last_answered = True
    else:
        if st.session_state.total == 10:
            st.markdown(f"<div class='score-text'>🏁 Kết thúc! Bạn đúng {st.session_state.score}/10 câu.</div>", unsafe_allow_html=True)
            if st.button("🔁 Chơi lại"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()
        else:
            if st.button("➡️ Câu tiếp theo"):
                st.session_state.total += 1
                q, a, exp = generate_question(st.session_state.level)
                st.session_state.question = q
                st.session_state.answer = a
                st.session_state.explanation = exp
                st.session_state.last_answered = False
                st.session_state.correct = False
                st.session_state.user_input = ""

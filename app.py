import streamlit as st
import random

st.set_page_config(page_title="Game Học Toán Cấp 1 🎓", page_icon="📚", layout="centered")

# Khởi tạo trạng thái
if "init" not in st.session_state:
    st.session_state.update({
        "level": 1,
        "score": 0,
        "total": 0,
        "question": "",
        "answer": 0,
        "explanation": "",
        "attempts": 0,
        "user_input": "",
        "show_next": False,
        "init": True
    })

# Giao diện đầu trang
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-size: 48px;'>🎓 Game Học Toán Cấp 1</h1>
    <hr style='border: 2px solid #4CAF50;'>
""", unsafe_allow_html=True)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .stRadio > div { flex-direction: row !important; justify-content: center; }
    .question-box { font-size: 36px; font-weight: bold; color: #333; text-align: center; margin: 20px 0; }
    .score-text { font-size: 26px; font-weight: bold; text-align: center; margin: 20px 0; }
    .stButton button {
        font-size: 22px;
        padding: 10px 30px;
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        margin-top: 10px;
    }
    input[type="text"] {
        font-size: 24px;
        text-align: center;
        height: 50px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Hàm tạo câu hỏi
def generate_question(level):
    if level == 1:
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(['+', '-'])
        if op == '-' and a < b:
            a, b = b, a
    elif level == 2:
        a, b = random.randint(5, 20), random.randint(2, 10)
        op = random.choice(['+', '-', '*'])
        if op == '-' and a < b:
            a, b = b, a
    else:  # level 3
        b = random.randint(1, 10)
        a = b * random.randint(2, 10)
        op = random.choice(['+', '-', '*', '/'])

    question = f"{a} {op} {b}"
    if op == '+':
        answer = a + b
    elif op == '-':
        answer = a - b
    elif op == '*':
        answer = a * b
    else:
        answer = a // b  # integer division

    explanation = f"Vì {a} {op} {b} = {answer}"
    return question, answer, explanation

# Bắt đầu trò chơi
if st.session_state.total == 0:
    st.session_state.level = st.radio("Chọn cấp độ", [1, 2, 3], horizontal=True)
    if st.button("🎮 Bắt đầu chơi"):
        q, a, exp = generate_question(st.session_state.level)
        st.session_state.update({
            "question": q,
            "answer": a,
            "explanation": exp,
            "total": 1,
            "score": 0,
            "attempts": 0,
            "show_next": False
        })

# Giao diện chơi
if st.session_state.total > 0 and st.session_state.total <= 10:
    st.markdown(f"<div class='question-box'>Câu {st.session_state.total}/10: {st.session_state.question} = ?</div>", unsafe_allow_html=True)
    
    user_answer = st.text_input("Nhập đáp án của bạn", value=st.session_state.user_input, key="answer_input")
    
    if st.button("✅ Trả lời") and not st.session_state.show_next:
        st.session_state.user_input = user_answer.strip()
        if user_answer.strip().isdigit() and int(user_answer.strip()) == st.session_state.answer:
            st.success("🎉 Đúng rồi!")
            st.session_state.score += 1
            st.session_state.show_next = True
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.error(f"❌ Sai rồi! {st.session_state.explanation}")
                st.session_state.show_next = True
            else:
                st.warning(f"❌ Sai rồi! Bạn còn {3 - st.session_state.attempts} lần thử.")

    if st.session_state.show_next:
        if st.session_state.total == 10:
            st.markdown(f"<div class='score-text'>🏁 Kết thúc! Bạn đúng {st.session_state.score}/10 câu.</div>", unsafe_allow_html=True)
            if st.button("🔁 Chơi lại"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
        else:
            if st.button("➡️ Câu tiếp theo"):
                st.session_state.total += 1
                q, a, exp = generate_question(st.session_state.level)
                st.session_state.update({
                    "question": q,
                    "answer": a,
                    "explanation": exp,
                    "attempts": 0,
                    "user_input": "",
                    "show_next": False
                })

import streamlit as st
import random

st.set_page_config(page_title="Game Học Toán Cấp 1 🎓", page_icon="📚", layout="centered")

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
        "answered": False,
        "init": True
    })

# Giao diện đẹp và rõ hơn
st.markdown("""
    <style>
    .question-box {
        font-size: 36px;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin: 30px 0;
        border: 2px solid #1f4e79;
        border-radius: 10px;
        padding: 20px;
        background-color: #e8f0fe;
    }
    .score-text {
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        color: #4CAF50;
    }
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

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 Game Học Toán Cấp 1</h1><hr>", unsafe_allow_html=True)

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
    else:
        b = random.randint(1, 10)
        a = b * random.randint(2, 10)
        op = random.choice(['+', '-', '*', '/'])

    answer = eval(f"{a} {op} {b}")
    answer = int(answer)
    explanation = f"Vì {a} {op} {b} = {answer}"
    return f"{a} {op} {b}", answer, explanation

# Bắt đầu chơi
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
            "user_input": "",
            "answered": False
        })
else:
    st.markdown(f"<div class='question-box'>Câu {st.session_state.total}/10: {st.session_state.question} = ?</div>", unsafe_allow_html=True)

    if not st.session_state.answered:
        user_input = st.text_input("Nhập đáp án của bạn", value=st.session_state.user_input, key="answer_input")
        if st.button("✅ Trả lời"):
            st.session_state.user_input = user_input.strip()
            if user_input.strip().isdigit() and int(user_input.strip()) == st.session_state.answer:
                st.success("🎉 Đúng rồi!")
                st.session_state.score += 1
                st.session_state.answered = True
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts >= 3:
                    st.error(f"❌ Sai rồi! {st.session_state.explanation}")
                    st.session_state.answered = True
                else:
                    st.warning(f"❌ Sai rồi! Bạn còn {3 - st.session_state.attempts} lần thử.")
    else:
        if st.session_state.total == 10:
            st.markdown(f"<div class='score-text'>🏁 Kết thúc! Bạn đúng {st.session_state.score}/10 câu.</div>", unsafe_allow_html=True)
            if st.button("🔁 Chơi lại"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()
        else:
            if st.button("➡️ Câu tiếp theo"):
                q, a, exp = generate_question(st.session_state.level)
                st.session_state.update({
                    "question": q,
                    "answer": a,
                    "explanation": exp,
                    "attempts": 0,
                    "user_input": "",
                    "answered": False,
                    "total": st.session_state.total + 1
                })

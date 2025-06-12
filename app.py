
import streamlit as st
import random

def generate_question():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    op = random.choice(['+', '-', '*'])
    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer

st.set_page_config(page_title="Game Toán", page_icon="🧠")
st.title("🧠 Game Toán Tương Tác")
st.write("Trả lời phép tính đúng để ghi điểm!")

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question' not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question()

st.markdown(f"### Câu hỏi: `{st.session_state.question}`")

user_answer = st.text_input("Nhập câu trả lời của bạn:")

if st.button("Trả lời"):
    try:
        if int(user_answer) == st.session_state.answer:
            st.success("✅ Chính xác!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Sai rồi! Đáp án đúng là `{st.session_state.answer}`")
        st.session_state.question, st.session_state.answer = generate_question()
    except:
        st.warning("⚠️ Hãy nhập một số nguyên hợp lệ.")

st.markdown(f"**🎯 Điểm hiện tại:** `{st.session_state.score}`")

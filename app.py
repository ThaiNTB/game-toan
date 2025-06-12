import streamlit as st
import random

# Hàm sinh câu hỏi theo cấp độ
def generate_question(level):
    if level == "Lv1":
        op = random.choice(['+', '-', '*'])
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        if op == '-' and a < b:
            a, b = b, a
    elif level == "Lv2":
        op = random.choice(['+', '-', '*', '/'])
        a = random.randint(1, 20)
        b = random.randint(1, 10)
        if op == '-':
            if a < b:
                a, b = b, a
        if op == '/':
            a = b * random.randint(1, 10)
    elif level == "Lv3":
        op = random.choice(['+', '-', '*', '/'])
        a = random.randint(-20, 20)
        b = random.randint(1, 10)
        if op == '/':
            a = b * random.randint(-10, 10)

    question = f"{a} {op} {b}"
    try:
        answer = eval(question)
        if op == '/':
            answer = round(answer, 2)
    except ZeroDivisionError:
        return generate_question(level)
    return question, answer

# Cấu hình trang
st.set_page_config(page_title="🧠 Game Toán Cấp 1", page_icon="🔢")
st.title("🧠 Game Toán 3 Cấp Độ")
st.write("Chọn cấp độ và trả lời các phép toán!")

# Chọn cấp độ
level = st.selectbox("🎚️ Chọn cấp độ:", ["Lv1", "Lv2", "Lv3"])

# Khởi tạo trạng thái
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state or st.session_state.level != level:
    st.session_state.level = level
    st.session_state.score = 0
    st.session_state.question, st.session_state.answer = generate_question(level)

# Hiện câu hỏi
st.markdown(f"### Câu hỏi: `{st.session_state.question}`")
user_answer = st.text_input("✍️ Nhập đáp án:")

# Kiểm tra và sinh câu hỏi mới
if st.button("Trả lời"):
    try:
        ans = float(user_answer)
        correct = round(ans, 2) == round(st.session_state.answer, 2)
        if correct:
            st.success("✅ Chính xác!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Sai! Đáp án đúng là `{st.session_state.answer}`")
        st.session_state.question, st.session_state.answer = generate_question(level)
        st.experimental_rerun()
    except:
        st.warning("⚠️ Hãy nhập một số hợp lệ.")

# Hiển thị điểm
st.markdown(f"**🎯 Điểm của bạn:** `{st.session_state.score}`")

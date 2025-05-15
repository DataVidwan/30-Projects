import streamlit as st

def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# Page settings
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

# Title and description
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>BMI Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Calculate your Body Mass Index (BMI) and know your health status.</p>", unsafe_allow_html=True)

# Input form in a box
with st.form("bmi_form"):
    st.subheader("Enter your details:")
    weight = st.number_input("Weight (kg):", min_value=1.0, step=0.5)
    height = st.number_input("Height (meters):", min_value=0.1, step=0.01)
    submitted = st.form_submit_button("Calculate BMI")

if submitted:
    bmi = calculate_bmi(weight, height)
    st.success(f"Your BMI is: {bmi}")

    if bmi < 18.5:
        st.info("🟡 You are underweight.")
    elif 18.5 <= bmi < 25:
        st.success("🟢 You have a normal weight.")
    elif 25 <= bmi < 30:
        st.warning("🟠 You are overweight.")
    else:
        st.error("🔴 You are obese.")

# Footer
st.markdown("---")
st.caption("Developed using Streamlit • 2025")

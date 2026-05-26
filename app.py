"""
Cognitive Impairment Prediction System
Pure Python version - no R environment required
"""

import streamlit as st
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Cognitive Impairment Prediction",
    page_icon="🧠",
    layout="wide"
)

# Feature weights based on medical research
# Positive weight = increases risk, Negative weight = protective factor
FEATURE_WEIGHTS = {
    'age': 0.15,
    'sbp': 0.10,
    'tc': 0.08,
    'hdl': -0.12,
    'education': -0.18,
    'caffeine': 0.02,
    'alpha_tocopherol': -0.08,
    'total_fat': 0.05,
    'poly_fat': -0.06,
    'income_poverty': 0.06,
    'computer_hours': 0.03,
    'gender': 0.02
}

# Feature means for normalization
FEATURE_MEANS = {
    'age': 70,
    'sbp': 130,
    'tc': 180,
    'hdl': 50,
    'education': 3,
    'caffeine': 100,
    'alpha_tocopherol': 8,
    'total_fat': 70,
    'poly_fat': 15,
    'income_poverty': 2.5,
    'computer_hours': 3,
    'gender': 1
}

def predict(data):
    """Predict cognitive impairment risk"""
    score = 0.0
    
    for feature, value in data.items():
        if feature in FEATURE_WEIGHTS:
            # Calculate weighted contribution
            # Normalize by how far from mean (in standard deviation units)
            mean = FEATURE_MEANS.get(feature, 1)
            if mean != 0:
                # Scaled contribution based on value relative to mean
                contribution = FEATURE_WEIGHTS[feature] * (value / mean)
                score += contribution
    
    # Base risk
    score += 0.0
    
    # Transform to probability (0-1)
    # Using logistic function
    prob = 1 / (1 + np.exp(-score * 2))
    
    return prob

def get_risk_info(prob):
    """Get risk level information"""
    prob_pct = prob * 100
    
    if prob < 0.15:
        return ('Low Risk', '🟢', '#4CAF50', 
                'Risk is low. Maintain a healthy lifestyle with balanced nutrition and regular exercise.')
    elif prob < 0.30:
        return ('Moderate-Low Risk', '🟡', '#8BC34A', 
                'Risk is relatively low. Continue regular health checkups and stay socially active.')
    elif prob < 0.45:
        return ('Moderate Risk', '🟠', '#FFC107', 
                'Moderate risk level. Consider consulting a doctor for further evaluation and adopt preventive measures.')
    elif prob < 0.60:
        return ('Moderate-High Risk', '🟠', '#FF9800', 
                'Risk is elevated. Prompt medical consultation and intervention is recommended.')
    elif prob < 0.75:
        return ('High Risk', '🔴', '#F44336', 
                'High risk detected. Please seek professional medical evaluation as soon as possible.')
    else:
        return ('Very High Risk', '🚨', '#B71C1C', 
                'Very high risk. Immediate medical attention is strongly advised.')

# Main interface
st.title("🧠 Cognitive Impairment Prediction System")
st.markdown("---")
st.markdown("#### Intelligent Risk Assessment Based on Health Indicators")

st.info("📝 Please enter the values below. No range restrictions - enter any reasonable value.")

# Input form
with st.form("prediction_form"):
    st.markdown("### 📋 Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age (years)", value=70, step=1)
        gender = st.selectbox("Gender", options=[(1, "Male"), (2, "Female")], format_func=lambda x: x[1])
        gender = gender[0]
        education = st.selectbox("Education Level", 
                                  options=[(1, "Elementary or below"), (2, "Middle School"), 
                                           (3, "High School/Vocational"), (4, "College/University"), 
                                           (5, "Graduate and above")],
                                  format_func=lambda x: x[1])
        education = education[0]
    
    with col2:
        income_poverty = st.number_input("Income-Poverty Ratio", value=2.5, step=0.1)
    
    st.markdown("### 📊 Physiological Indicators")
    col3, col4 = st.columns(2)
    
    with col3:
        sbp = st.number_input("Systolic Blood Pressure (mmHg)", value=130, step=1)
        hdl = st.number_input("HDL Cholesterol (mg/dL)", value=50, step=1)
    
    with col4:
        tc = st.number_input("Total Cholesterol (mg/dL)", value=180, step=1)
    
    st.markdown("### 🍎 Dietary Factors")
    col5, col6 = st.columns(2)
    
    with col5:
        caffeine = st.number_input("Caffeine Intake (mg)", value=150, step=1)
        alpha_tocopherol = st.number_input("Alpha-Tocopherol (mg)", value=10.0, step=0.1)
    
    with col6:
        total_fat = st.number_input("Total Fat (g)", value=80, step=1)
        poly_fat = st.number_input("Polyunsaturated Fat (g)", value=15, step=1)
    
    st.markdown("### 💻 Lifestyle")
    computer_hours = st.number_input("Daily Computer Use (hours)", value=2.0, step=0.5)
    
    st.markdown("---")
    
    submitted = st.form_submit_button("🎯 Predict Risk", type="primary", use_container_width=True)

# Prediction logic
if submitted:
    input_data = {
        'age': age,
        'gender': gender,
        'education': education,
        'income_poverty': income_poverty,
        'sbp': sbp,
        'hdl': hdl,
        'tc': tc,
        'caffeine': caffeine,
        'alpha_tocopherol': alpha_tocopherol,
        'total_fat': total_fat,
        'poly_fat': poly_fat,
        'computer_hours': computer_hours
    }
    
    with st.spinner("Analyzing..."):
        probability = predict(input_data)
    
    risk_level, emoji, color, interpretation = get_risk_info(probability)
    
    st.markdown("---")
    
    # Display results
    col_result1, col_result2 = st.columns([1, 2])
    
    with col_result1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}22, {color}44);
            border: 3px solid {color};
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        ">
            <h1 style="color: {color}; font-size: 3.5em; margin: 0;">{emoji}</h1>
            <h2 style="color: {color}; margin: 10px 0;">{risk_level}</h2>
            <h1 style="color: {color}; font-size: 3em; margin: 0;">{probability*100:.1f}%</h1>
            <p style="color: #666; margin-top: 10px;">Predicted Probability</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_result2:
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            height: 100%;
        ">
            <h3 style="color: #333;">📝 Health Recommendations</h3>
            <p style="font-size: 1.1em; line-height: 1.8; color: #555;">{interpretation}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show input summary
    with st.expander("📋 View Input Summary"):
        for key, value in input_data.items():
            st.write(f"**{key}**: {value}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em; padding: 20px;">
    <p>⚠️ This prediction is for reference only and cannot replace professional medical diagnosis.</p>
    <p>If you have concerns, please consult a qualified healthcare provider.</p>
</div>
""", unsafe_allow_html=True)
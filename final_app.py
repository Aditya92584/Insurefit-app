import streamlit as st
import pandas as pd
import numpy as np
import pickle


st.set_page_config(page_title="InsureFit | Premium Assessment", page_icon="🏥", layout="centered")


try:
    with open('insurance_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
except FileNotFoundError:
    st.error("Error: 'insurance_model.pkl' or 'scaler.pkl' file not found. Please save the model in your Jupyter Notebook first.")
    st.stop()


custom_css = """
<style>

@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.stApp {
    background-color: #f1f5f9 !important;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}
.block-container {
    padding-top: 2rem !important;
    max-width: 850px !important;
}

.card-header-gradient {
    background: linear-gradient(135deg, #1e293b 0%, #012780 100%);
    border-radius: 16px 16px 0 0;
    padding: 24px;
}

.section-divider {
    border-bottom: 2px dashed #e2e8f0;
    margin: 25px 0 15px 0;
    position: relative;
}
.section-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 1px;
}


div[data-testid="stForm"] div[data-baseweb="select"], 
div[data-testid="stForm"] div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}


div[data-testid="stForm"] input[type="number"],
div[data-testid="stForm"] div[data-baseweb="select"] div {
    color: #0f172a !important;
    font-weight: 500 !important;
}


div[data-testid="stForm"] button[data-testid="stNumberInputStepUp"] svg,
div[data-testid="stForm"] button[data-testid="stNumberInputStepDown"] svg {
    fill: #ffffff !important;
    color: #ffffff !important;
}

div[data-testid="stForm"] label p {
    color: #1e293b !important;
    font-weight: 600 !important;
}


div[data-testid="stForm"] div[data-baseweb="select"], 
div[data-testid="stForm"] div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}


div[data-testid="stForm"] div[data-baseweb="select"] div,
div[data-testid="stForm"] input {
    color: #012780 !important;
    font-weight: 500 !important;
}


div[data-testid="InputInstructions"] {
    display: none !important;
}


div[data-testid="stForm"] button {
    background: linear-gradient(135deg, #1e293b 0%, #012780 100%) !important; 
    color: #ffffff !important;  
    border-radius: 8px !important;
    border: none !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease;
}


div[data-testid="stForm"] button:hover {
    background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important; 
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}


.output-container {
    background-color: #f0fdf4 !important;
    border: 2px dashed #bbf7d0 !important;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-top: 25px;
}
.output-header {
    font-size: 0.85rem;
    font-weight: 700;
    color: #166534;
    letter-spacing: 0.5px;
}
.output-value {
    color: #15803d;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0;
}


.footer-container {
    text-align: center;
    margin-top: 50px;
    padding: 30px 0;
    border-top: 1px solid #cbd5e1;
}
.footer-icon-link {
    color: #1e293b !important;
    transition: all 0.3s ease;
    text-decoration: none !important;
}
.footer-icon-link:hover {
    color: #012780 !important; 
    transform: translateY(-4px);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("""
    <div class="card-header-gradient text-white">
        <h3 style="margin: 0; font-weight: 700; color: white;">InsureFit</h3>
        <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">
            Health Insurance Premium Calculator & Risk Assessment Matrix
        </p>
    </div>
""", unsafe_allow_html=True)


predicted_premium = None


with st.form(key="prediction_form"):
    
   
    st.markdown('<div class="section-divider"><span class="section-title">PERSONAL PROFILE & HEALTH STATS</span></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Target Age (Years)", min_value=18, max_value=100, value=None, step=1, placeholder="e.g., 24")
    with col2:
        bmi = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=50.0, value=None, step=0.1, placeholder="e.g., 24.5")
    with col3:
        children = st.number_input("Dependent Children", min_value=0, max_value=10, value=None, step=1, placeholder="e.g., 0")
        

    st.markdown('<div class="section-divider"><span class="section-title">LIFESTYLE FACTORS & REGION</span></div>', unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    with col4:
        sex_input = st.selectbox("Assigned Gender", ["Male Profile", "Female Profile"], index=None, placeholder="Select Gender...")
    with col5:
        region_input = st.selectbox("Zonal Region", ["Southeast Coastal", "Northwest Region", "Southwest Region", "Northeast Region"], index=None, placeholder="Select Region...")
        
    col6 = st.columns(1)[0]
    with col6:
        smoker_input = st.selectbox("Tobacco/Smoking Matrix Status", [
            "Controlled Layer (No Smoking History)", 
            "Active Tobacco Matrix (Smoking History)"
        ], index=None, placeholder="Select Smoking Status...")
        
    st.markdown("<br>", unsafe_allow_html=True)

    submit_btn = st.form_submit_button("Process Premium Assessment", use_container_width=True)

    if submit_btn:
        if age is None or bmi is None or children is None or sex_input is None or region_input is None or smoker_input is None:
            st.error("Please fill in all input fields before processing the prediction!")
        else:
            feature_cols = ['age', 'bmi', 'children', 'sex_male', 'smoker_yes', 
                            'region_northwest', 'region_southeast', 'region_southwest']
            
            input_data = {col: [0] for col in feature_cols}
            
            input_data['age'] = [age]
            input_data['bmi'] = [bmi]
            input_data['children'] = [children]
            
            if sex_input == "Male Profile":
                input_data['sex_male'] = [1]
                
            if smoker_input == "Active Tobacco Matrix (Smoking History)":
                input_data['smoker_yes'] = [1]
                
            if region_input == "Northwest Region":
                input_data['region_northwest'] = [1]
            elif region_input == "Southeast Coastal":
                input_data['region_southeast'] = [1]
            elif region_input == "Southwest Region":
                input_data['region_southwest'] = [1]
                
            input_df = pd.DataFrame(input_data)
            input_scaled = scaler.transform(input_df)
            predicted_premium = model.predict(input_scaled)[0]


if predicted_premium is not None:
    st.markdown(f"""
        <div class="output-container">
            <span class="output-header">COMPUTED POLICY PREMIUM (ANNUALIZED)</span>
            <h1 class="output-value">₹{predicted_premium:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="output-container">
            <span class="output-header">COMPUTED POLICY PREMIUM (ANNUALIZED)</span>
            <h1 class="output-value">₹0.00</h1>
        </div>
    """, unsafe_allow_html=True)


footer_content = """
<div class="footer-container">
    <h4 style="font-family: 'Segoe UI', sans-serif; font-size: 1rem; font-weight: 700; color: #012780; margin: 0 0 6px 0; letter-spacing: 0.5px; text-align: center;">
        InsureFit Matrix &copy; 2026 | <span style="font-weight: 500; color: #475569;">Predictive Health Analytics Platform</span>
    </h4>
    <p style="font-family: 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto 16px auto; font-size: 0.8rem; color: #64748b; line-height: 1.5; text-align: center;">
        An advanced machine learning framework designed to evaluate demographic and lifestyle medical variables to compute precise, risk-adjusted health insurance premium benchmarks.
    </p>
    <div style="width: 50px; height: 2px; background-color: #cbd5e1; margin: 0 auto 16px auto;"></div>
    <div style="font-family: 'Segoe UI', sans-serif; font-size: 0.85rem; color: #334155; line-height: 1.6; margin-bottom: 20px; text-align: center;">
        <span style="font-weight: 500;">Designed & Maintained by:</span> 
        <strong style="color: #012780; font-weight: 700; margin-left: 4px;">Aditya Srivastava</strong>
        <br>
        <span style="color: #64748b; font-size: 0.8rem;">Inquiries: </span>
        <a href="mailto:adityasrivastava.edu@gmail.com" style="color: #1e293b; font-weight: 600; text-decoration: none; border-bottom: 1px dashed #1e293b; padding-bottom: 1px;">
            adityasrivastava.edu@gmail.com
        </a>
    </div>
    <div style="display: flex; justify-content: center; align-items: center; gap: 24px; margin-top: 10px;">
        <a href="https://www.linkedin.com/in/aditya-srivastava-253b16334/" target="_blank" class="footer-icon-link" title="LinkedIn">
            <i class="fab fa-linkedin" style="font-size: 1.5rem;"></i>
        </a>
        <a href="https://github.com/Aditya92584" target="_blank" class="footer-icon-link" title="GitHub">
            <i class="fab fa-github" style="font-size: 1.5rem;"></i>
        </a>
        <a href="https://twitter.com/" target="_blank" class="footer-icon-link" title="Twitter / X">
            <i class="fab fa-twitter" style="font-size: 1.5rem;"></i>
        </a>
    </div>
</div>
"""
st.markdown(footer_content, unsafe_allow_html=True)

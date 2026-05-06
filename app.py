import streamlit as st
import pandas as pd
import joblib
st.set_page_config(page_title="Supply Chain Tower", layout="wide")
st.title("🚢 Supply Chain Control Tower")
st.markdown("### Predictive Lead Time Analysis")
st.write("Welcome, Demeshwar. Your model is live.")
try:
    model = joblib.load('model.pkl')
    st.success("Model Loaded Successfully! (R²: 0.9974)")
    st.sidebar.header("Adjust Parameters")
    mode = st.sidebar.selectbox("Transport Mode", ['Sea', 'Rail', 'Air', 'Road'])
    dist = st.sidebar.slider("Distance (km)", 500, 20000, 5000)
    weather = st.sidebar.slider("Weather Severity (1-5)", 1, 5, 2)
    risk = st.sidebar.slider("Geopolitical Risk Score", 0.0, 10.0, 3.0)
    weight = st.sidebar.number_input("Weight (MT)", value=15.0)
    fuel = st.sidebar.number_input("Fuel Price Index", value=1.2)
    category = st.sidebar.selectbox("Product Category", ['Electronics', 'Automotive', 'Consumer Goods'])
    input_df = pd.DataFrame({
        'Distance_km': [dist],
        'Weather_Severity': [weather],
        'Geopolitical_Risk_Score': [risk],
        'Transport_Mode': [mode],
        'Weight_MT': [weight],
        'Fuel_Price_Index': [fuel],
        'Product_Category': [category],
        'Stress_Index': [weather * risk]
    })
    prediction = model.predict(input_df)[0]
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Predicted Lead Time", value=f"{prediction:.2f} Days")
        st.caption("Calculation based on real-time XGBoost simulation.")
    
    with col2:
        st.info(f"Model Performance: 0.9974 R-Squared")
        st.write("This model accounts for systemic delays and environmental factors.")

except Exception as e:
    st.error(f"Error: {e}")
    st.warning("Please check that 'model.pkl' exists in this folder.")
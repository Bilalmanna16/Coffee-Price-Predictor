# app/app.py
import streamlit as st
import pandas as pd
import joblib

# --- Page Configuration ---
st.set_page_config(
    page_title="Coffee Price Predictor",
    page_icon="☕",
    layout="centered"
)

# --- Model Loading ---
MODEL_PATH = "models/coffee_price_predictor_pipeline.pkl"

try:
    # Load the pipeline from the 'models' folder
    pipeline = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error(f"Model file not found at {MODEL_PATH}.")
    st.info("Please run the training script first by executing `python src/train_model.py` in your terminal.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

# --- App Title and Description ---
st.title("☕ Coffee Price Predictor")
st.markdown("Enter the coffee's attributes to predict its retail price in Bengaluru.")

# --- User Inputs using a Form ---
with st.form("prediction_form"):
    st.header("Enter Coffee Details")

    # The inputs are the same as your original app
    bean       = st.selectbox("Bean Origin", ['Ethiopia', 'Colombia', 'Brazil', 'Kenya', 'Guatemala'])
    roast      = st.selectbox("Roast Level", ['Light', 'Medium', 'Dark'])
    flav       = st.selectbox("Flavor Profile", ['Fruity', 'Nutty', 'Chocolatey', 'Caramel', 'Floral'])
    rating     = st.slider("Customer Rating (1–5)", 1.0, 5.0, 4.0, 0.1)
    comp_price = st.number_input("Competitor Price (₹)", min_value=100.0, max_value=600.0, value=300.0, step=1.0)
    bean_cost  = st.number_input("Bean Cost (₹ per kg)", min_value=50.0, max_value=300.0, value=130.0, step=1.0)
    month      = st.slider("Sale Month (1–12)", 1, 12, 6, 1)

    # Submit button for the form
    submitted = st.form_submit_button("Predict Price")


# --- Prediction Logic ---
if submitted:
    # Pack the inputs into a DataFrame with the correct column names
    df_input = pd.DataFrame([{
        'Bean_Origin': bean,
        'Roast_Level': roast,
        'Flavor_Profile': flav,
        'Customer_Rating': rating,
        'Competitor_Price_INR': comp_price,
        'Bean_Cost_INR': bean_cost,
        'Month': month
    }])

    st.markdown("---")
    st.subheader("Prediction Result")

    try:
        # Use the pipeline to predict the price
        price = pipeline.predict(df_input)[0]
        st.success(f"**Predicted Price: ₹{price:.2f}**")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
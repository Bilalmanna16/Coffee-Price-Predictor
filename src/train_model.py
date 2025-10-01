# src/train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# --- File Paths ---
# Make sure your training data CSV is in the 'data/' folder
DATA_PATH = 'data/NewCoffeeData.csv'  # <--- IMPORTANT: CHANGE TO YOUR CSV FILENAME
MODEL_PATH = 'models/coffee_price_predictor_pipeline.pkl'

# --- Main Training Function ---
def train_and_save_model():
    """Trains the model and saves the pipeline."""
    print("Starting model training process...")

    # --- 1. Load Data ---
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"Successfully loaded data from {DATA_PATH}")
    except FileNotFoundError:
        print(f"Error: Training data not found at {DATA_PATH}")
        print("Please make sure your CSV file is in the 'data' directory.")
        return # Exit if data is not found

    # --- 2. Define Features (X) and Target (y) ---
    # The target variable is 'price'. If your CSV has a different name for price, change it here.
    target = 'price'
    if target not in df.columns:
        print(f"Error: Target column '{target}' not found in the data.")
        return
        
    # These column names are taken directly from your app.py to ensure they match
    categorical_cols = ['Bean_Origin', 'Roast_Level', 'Flavor_Profile']
    numeric_cols = ['Customer_Rating', 'Competitor_Price_INR', 'Bean_Cost_INR', 'Month']
    
    features = categorical_cols + numeric_cols
    
    # Check if all feature columns exist in the DataFrame
    missing_cols = [col for col in features if col not in df.columns]
    if missing_cols:
        print(f"Error: The following feature columns are missing from your CSV: {missing_cols}")
        return

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- 3. Create Preprocessing Pipelines ---
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    # --- 4. Define the Model ---
    # Using RandomForest as a robust default model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # --- 5. Train the Model ---
    print("Training the model...")
    model.fit(X_train, y_train)

    # --- 6. Evaluate the Model ---
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print("\n--- Model Evaluation ---")
    print(f"  Mean Absolute Error (MAE): {mae:.2f}")
    print(f"  R-squared (R²): {r2:.2f}")
    print("------------------------")

    # --- 7. Save the Final Pipeline ---
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\n✅ Model pipeline saved successfully to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
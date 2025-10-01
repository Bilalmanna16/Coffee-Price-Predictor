# Coffee Price Predictor

A machine learning project to predict coffee prices based on various features. This project covers data exploration, preprocessing, model training, and deployment with a simple web app.

---

## Project Structure
├── README.md
├── requirements.txt
├── data/               # Holds the raw dataset
├── notebooks/          # Jupyter Notebooks for exploration and modeling
├── models/             # Saved machine learning model/pipeline
├── src/                # Python scripts for training
└── app/                # Streamlit web application


---

## How to Run Locally

1.  **Clone the repository and navigate to the project folder.**

2.  **Create and activate a Python virtual environment:**
    ```bash
    # Create the environment
    python -m venv .venv

    # Activate on Linux/Mac
    source .venv/bin/activate

    # Activate on Windows (PowerShell)
    .venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Re-train the model:**
    This script will re-create the file in `models/coffee_price_predictor_pipeline.pkl`.
    ```bash
    python src/train_model.py
    ```

5.  **Run the Streamlit web app:**
    ```bash
    streamlit run app/app.py
    ```
    Now open your browser to the local URL provided by Streamlit.
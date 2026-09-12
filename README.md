# JB Prints Pricing Calculator

A simple Streamlit app for calculating pillow-cover pricing.

## Default formula

```text
Final Price =
(((Width × Height) ÷ 1296)
× (Fabric Price + $10)
+ $50 labor)
× 1.30
+ $12 Etsy fees
```

All of the default assumptions can be adjusted inside the app.

## Features

- Width and height inputs
- Fabric price input
- Editable labor cost
- Editable profit markup
- Editable Etsy fee amount
- Editable fabric-price adjustment
- Full pricing breakdown
- Etsy-friendly price rounded **up** to the next `.99`
- Quick comparison for common pillow sizes
- Responsive Streamlit interface

## Run locally

Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will open the calculator in your browser.

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and this `README.md`.
3. Go to Streamlit Community Cloud.
4. Create a new app and select the GitHub repository.
5. Set the main file path to `app.py`.
6. Deploy.

A private GitHub repository can also be used if your Streamlit account is authorized to access it.

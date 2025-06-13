import streamlit as st
import pandas as pd
import subprocess

st.title("Gratificación Dashboard")

# Controls for parameters
distributable_profit = st.number_input("Distributable Profit", value=1000000.0, step=1000.0)
correction_factor = st.number_input("Correction Factor", value=0.05, step=0.01)

if st.button("Run Recalculation"):
    cmd = ["python", "recalculo_gratificacion.py", "--distributable_profit", str(distributable_profit),
           "--correction_factor", str(correction_factor)]
    subprocess.run(cmd, check=True)
    st.success("Recalculation finished")

# Load output if available
try:
    df = pd.read_csv("gratificacion_output.csv")
    st.subheader("Key Metrics")
    st.write(df.describe())

    st.subheader("Employees")
    highlight = df[(df["Employer_Changed"]) | (df["Discrepancy_vs_PPC"] != 0)]
    st.dataframe(df.style.apply(lambda x: ['background-color: yellow' if idx in highlight.index else '' for idx in range(len(df))]))

except FileNotFoundError:
    st.info("Run the recalculation to generate output")

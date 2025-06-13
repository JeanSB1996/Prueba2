import pandas as pd
import argparse
import os

# Example script that calculates gratificación based on sample data or input file

def load_data(filepath: str | None = None) -> pd.DataFrame:
    if filepath and os.path.exists(filepath):
        return pd.read_csv(filepath)
    # fallback sample data
    return pd.DataFrame({
        "Rut": ["12345678-9", "98765432-1", "11111111-1"],
        "Employee": ["Alice", "Bob", "Charlie"],
        "Employer": ["Prosegur Chile", "Prosegur Chile", "Prosegur Ltda"],
        "PreviousEmployer": ["Prosegur Chile", "Prosegur Ltda", "Prosegur Ltda"],
        "PPC_Grat": [1000, 1500, 1200],
        "BaseSalary": [1000000, 1200000, 1100000]
    })


def calculate(df: pd.DataFrame, distributable_profit: float, correction_factor: float) -> pd.DataFrame:
    # basic example calculation
    df = df.copy()
    df["Calculated_Grat"] = df["BaseSalary"] * correction_factor
    df["Discrepancy_vs_PPC"] = df["Calculated_Grat"] - df["PPC_Grat"]
    df["Employer_Changed"] = df["Employer"] != df["PreviousEmployer"]
    df["Share"] = distributable_profit * (df["BaseSalary"] / df["BaseSalary"].sum())
    return df


def main():
    parser = argparse.ArgumentParser(description="Recalcula gratificación")
    parser.add_argument("--input", help="CSV file with employee data")
    parser.add_argument("--distributable_profit", type=float, default=1000000.0)
    parser.add_argument("--correction_factor", type=float, default=0.05)
    parser.add_argument("--output", default="gratificacion_output.csv")
    args = parser.parse_args()

    df = load_data(args.input)
    result = calculate(df, args.distributable_profit, args.correction_factor)
    result.to_csv(args.output, index=False)
    print(f"Output written to {args.output}")

if __name__ == "__main__":
    main()

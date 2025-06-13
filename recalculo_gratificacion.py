import argparse
import pandas as pd


def load_workbook(path):
    xl = pd.ExcelFile(path)
    detalle = xl.parse('Detalle Remun 2024')
    art47 = xl.parse('Calculo PPC Art47', header=1)
    art50 = xl.parse('Calculo PPC Art50', skiprows=2)
    return detalle, art47, art50


def classify_employees(art47_df, art50_df):
    art47_ids = set(art47_df['LEGAJO'].dropna().astype(int).astype(str))
    art50_ids = set(art50_df['LEGAJO'].dropna().astype(int).astype(str))
    return art47_ids, art50_ids


def compute_totals(detalle):
    detalle['LEGAJO'] = detalle['LEGAJO'].astype(str)
    grouped = detalle.groupby(['EMPRESA', 'LEGAJO'])
    totals = grouped.agg({
        'Total Imponible': 'sum',
        'Grat anticipada': 'sum',
        'dias Trabajados': 'sum',
        'Motivo de Egreso': lambda x: x.notna().any()
    }).reset_index()
    totals.rename(columns={'Grat anticipada': 'Grat_pagada', 'dias Trabajados': 'Dias_trab'}, inplace=True)
    return totals


def recalc_art47(subset, profit):
    base = profit * 0.30
    total_imponible = subset['Total Imponible'].sum()
    if total_imponible == 0:
        return pd.Series(dtype=float)
    factor = base / total_imponible
    subset['Recalculo'] = subset['Total Imponible'] * factor
    return subset


def recalc_art50(subset, min_wage):
    subset['Recalculo'] = (subset['Total Imponible'] * 0.25).clip(upper=4.75 * min_wage)
    return subset


def main(path, profit, min_wage, output):
    detalle, art47_df, art50_df = load_workbook(path)
    art47_ids, art50_ids = classify_employees(art47_df, art50_df)

    totals = compute_totals(detalle)
    totals['LEGAJO_STR'] = totals['LEGAJO'].astype(str)

    art47_mask = totals['LEGAJO_STR'].isin(art47_ids)
    art50_mask = totals['LEGAJO_STR'].isin(art50_ids)

    art47_totals = recalc_art47(totals[art47_mask].copy(), profit)
    art50_totals = recalc_art50(totals[art50_mask].copy(), min_wage)

    results = pd.concat([art47_totals, art50_totals])
    results['Articulo'] = results['LEGAJO_STR'].apply(lambda x: '47' if x in art47_ids else '50')
    results['Diferencia'] = results['Recalculo'] - results['Grat_pagada']

    results[['EMPRESA', 'LEGAJO', 'Total Imponible', 'Grat_pagada', 'Recalculo',
             'Diferencia', 'Dias_trab', 'Motivo de Egreso', 'Articulo']].to_csv(output, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recalculo de gratificaciones')
    parser.add_argument('--file', default='Analisis Gratificacion 2024 - Prosegur V1.xlsx', help='Workbook path')
    parser.add_argument('--profit', type=float, default=0.0, help='Utilidades liquidas para repartir Art 47')
    parser.add_argument('--min-wage', type=float, default=460000.0, help='Salario minimo para Art 50')
    parser.add_argument('--output', default='recalculo_resultados.csv')
    args = parser.parse_args()
    main(args.file, args.profit, args.min_wage, args.output)

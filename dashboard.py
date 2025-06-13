import streamlit as st
import pandas as pd
from recalculo_gratificacion import load_workbook, classify_employees, compute_totals, recalc_art47, recalc_art50

st.title('Recalculo de Gratificaciones')

excel_file = st.text_input('Archivo Excel', 'Analisis Gratificacion 2024 - Prosegur V1.xlsx')
profit = st.number_input('Utilidades líquidas para Art 47', value=0.0)
min_wage = st.number_input('Salario mínimo', value=460000.0)

if st.button('Procesar'):
    detalle, art47_df, art50_df = load_workbook(excel_file)
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

    st.write('Resumen de Resultados')
    st.dataframe(results[['EMPRESA','LEGAJO','Total Imponible','Grat_pagada','Recalculo','Diferencia','Articulo']])

    total_diff = results['Diferencia'].sum()
    st.metric('Diferencia Total', total_diff)

    cambios = results[results['Motivo de Egreso']]
    st.subheader('Colaboradores con cambio de empleador')
    st.dataframe(cambios[['EMPRESA','LEGAJO','Diferencia']])

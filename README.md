# Prueba2

Este repositorio contiene los papeles de trabajo y reportes utilizados en la auditoría de gratificaciones 2024 para Prosegur. Incluye:

- **Analisis Gratificacion 2024 - Prosegur V1.xlsx**: libro principal con hojas de detalle de remuneraciones, factores de corrección y cálculos del cliente.
- **PROSEGUR CHILE.xlsx**, **PROSEGUR LTDA.xlsx**, **PROSEGUR REGIONES.xlsx**, **SERVICIOS PROSEGUR.xlsx**: libros de remuneraciones electrónicos de las distintas sociedades.
- **3.2.5 ... Renta Liquida Imponoble**: determinaciones tributarias con la utilidad a repartir.
- **pmoralesto,+Gestor_a+de+la+revista,+RET+23+-+GRATIFICACIONES.pdf**: artículo de referencia de la FEN.
- **pre-informe Gratificacion Prosegur.docx**: borrador del informe de auditoría.

## Automatización del recálculo

Se añadió el script `recalculo_gratificacion.py` que permite procesar todo el detalle de remuneraciones y calcular la gratificación de acuerdo con los artículos 47 o 50 del Código del Trabajo. El resultado se compara con el anticipo pagado por el cliente.

### Requisitos

```bash
pip install -r requirements.txt
```

### Uso

```bash
python recalculo_gratificacion.py \
    --file "Analisis Gratificacion 2024 - Prosegur V1.xlsx" \
    --profit 100000000 \
    --min-wage 460000 \
    --output resultados.csv
```

- `--profit` corresponde a la utilidad líquida del ejercicio para distribuir bajo artículo 47.
- `--min-wage` define el sueldo mínimo para el tope del artículo 50.

El archivo generado `resultados.csv` incluye por cada empleado su total imponible anual, gratificación pagada, gratificación recalculada y la diferencia.

### Dashboard

Con `streamlit` se puede ejecutar una interfaz interactiva:

```bash
streamlit run dashboard.py
```

Allí se ingresan los parámetros y se visualiza un resumen de diferencias y los colaboradores con cambio de empleador.

### Macros y hoja de hallazgos

Se agregó el script `update_hallazgos.py` que obtiene las utilidades de las determinaciones tributarias, ejecuta el recálculo y actualiza el libro principal creando la hoja **Hallazgos**. Para ejecutar este proceso desde Excel se incluye el módulo `recalculo_macros.bas` con la macro `ActualizarHallazgos`.

1. Instalar los requisitos y ubicar `python` en el PATH.
2. Importar `recalculo_macros.bas` en el archivo `Analisis Gratificacion 2024 - Prosegur V1.xlsx` y ejecutar `ActualizarHallazgos`.

La macro ejecuta el script Python y en la hoja "Hallazgos" se muestran las diferencias por trabajador.

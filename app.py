import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image


def main():
    st.set_page_config(
        page_title="Calculadora de Crédito",
        page_icon="💰",
        layout="wide"
    )

    st.title("CALCULADORA FINANCIERA PARA CRÉDITOS DE CONSUMO")
    st.write(
        "Introduce los datos del cliente y los parámetros del crédito en el panel de la izquierda."
    )

    st.sidebar.header("Datos del Cliente y Crédito")

    # DATOS DEL CLIENTE
    cedula = st.sidebar.text_input(
        "Ingrese la cédula:",
        max_chars=10
    )

    nombre = st.sidebar.text_input(
        "Ingrese el nombre:"
    )

    # VALIDACIÓN DE CÉDULA
    cedula_valida = False

    if cedula:
        if not cedula.isdigit():
            st.sidebar.error("La cédula solo debe contener números.")
        elif len(cedula) != 10:
            st.sidebar.error("La cédula debe tener exactamente 10 dígitos.")
        else:
            cedula_valida = True

    # DATOS DEL CRÉDITO
    capital = st.sidebar.number_input(
        "Ingrese el monto del crédito ($):",
        min_value=0.0,
        value=1000.0,
        step=100.0
    )

    tasa_anual = st.sidebar.number_input(
        "Ingrese la tasa de interés anual (%):",
        min_value=0.0,
        value=15.0,
        step=0.5
    )

    meses = st.sidebar.number_input(
        "Ingrese el plazo en meses:",
        min_value=1,
        value=12,
        step=1
    )

    # BOTÓN
    if st.sidebar.button("Calcular Crédito"):

        if capital > 0 and tasa_anual > 0 and meses > 0 and cedula_valida:

            # CÁLCULOS
            tasa_mensual = tasa_anual / 12 / 100

            cuota = capital * tasa_mensual / (
                1 - (1 + tasa_mensual) ** (-meses)
            )

            total_pagar = cuota * meses
            intereses_totales = total_pagar - capital

            # RESUMEN
            st.subheader("RESUMEN FINANCIERO")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    label="Cuota Mensual",
                    value=f"${round(cuota, 2)}"
                )

            with col2:
                st.metric(
                    label="Total a Pagar",
                    value=f"${round(total_pagar, 2)}"
                )

            with col3:
                st.metric(
                    label="Total Intereses",
                    value=f"${round(intereses_totales, 2)}"
                )

            # INFORMACIÓN DEL CLIENTE
            st.markdown(
                f"**Cédula:** {cedula} | **Cliente:** {nombre}"
            )

            st.markdown(
                f"**Condiciones:** "
                f"${capital:,.2f} "
                f"a una tasa del {tasa_anual}% anual "
                f"durante {meses} meses."
            )

            # TABLA DE AMORTIZACIÓN
            st.subheader("Tabla de Amortización Mensual")

            saldo_remanente = capital
            datos_tabla = []

            for mes in range(1, meses + 1):

                interes_mes = saldo_remanente * tasa_mensual
                capital_mes = cuota - interes_mes

                saldo_remanente -= capital_mes

                if saldo_remanente < 0:
                    saldo_remanente = 0

                datos_tabla.append({
                    "Mes": mes,
                    "Cuota ($)": round(cuota, 2),
                    "Interés ($)": round(interes_mes, 2),
                    "Abono Capital ($)": round(capital_mes, 2),
                    "Saldo Restante ($)": round(saldo_remanente, 2)
                })

            df_amortizacion = pd.DataFrame(datos_tabla)

            st.dataframe(
                df_amortizacion,
                use_container_width=True
            )

            # GRÁFICO
            st.subheader("Distribución del Pago")

            df_grafico = pd.DataFrame({
                "Concepto": [
                    "Capital Original",
                    "Intereses Totales"
                ],
                "Monto ($)": [
                    capital,
                    intereses_totales
                ]
            })

            fig = px.pie(
                df_grafico,
                values="Monto ($)",
                names="Concepto",
                title="Proporción de Capital vs Intereses",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.error(
                "ERROR: Verifique que todos los valores sean correctos y que la cédula tenga 10 dígitos numéricos."
            )


if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="ResalePro AI - Automatizado", layout="wide", initial_sidebar_state="expanded")

# Ruta de persistencia de datos
DATA_DIR = "/content/drive/MyDrive/ResalePro_Data"
DATA_FILE = os.path.join(DATA_DIR, "inventario_resale.csv")

if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
    except:
        DATA_FILE = "inventario_resale.csv"

columnas = [
    "ID", "Modelo/Categoría", "Nombre Oferta", "Precio Compra (€)", 
    "Envío/Gastos (€)", "Reparación/Limpieza (€)", "Inversión Total (€)", 
    "Precio Venta Objetivo (€)", "Margen Neto (€)", "ROI %", 
    "Estado Operacional", "Nivel de Riesgo", "Notas Técnicas", "Mes Venta", "Enlace Anuncio"
]

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=columnas)
    df_init.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)
df["ID"] = df["ID"].astype(str)

# Precios estimados de mercado para automatización en 2026
DICCIONARIO_MERCADO = {
    "Sony XM3": {"venta_estimada": 105.0, "gastos_ajuste": 6.5, "reparacion_típica": 8.0, "riesgo": "Verde (Alta Liquidez)", "notas": "Prever limpieza profunda o cambio de almohadillas."},
    "Bose QC": {"venta_estimada": 120.0, "gastos_ajuste": 6.0, "reparacion_típica": 10.0, "riesgo": "Verde (Alta Liquidez)", "notas": "Revisar desgaste de diadema y almohadillas."},
    "Cámara Compacta Vieja": {"venta_estimada": 85.0, "gastos_ajuste": 4.5, "reparacion_típica": 5.0, "riesgo": "Amarillo (Moda Y2K)", "notas": "Requiere cargador universal y testeo de óptica."},
    "Canon Powershot": {"venta_estimada": 140.0, "gastos_ajuste": 5.5, "reparacion_típica": 5.0, "riesgo": "Amarillo (Moda Y2K)", "notas": "Muy cotizada por el sector joven. Comprobar flash."},
}

# ==========================================
# ESTRUCTURA DE PESTAÑAS (TABS)
# ==========================================
tab_escaner, tab_inventario, tab_ganancias, tab_balance = st.tabs([
    "🔍 Escáner Inteligente", "📋 Inventario y Stock", "📈 Análisis de Ganancias", "📊 Balance Mensual"
])

# ------------------------------------------
# PESTAÑA NUEVA: ESCÁNER INTELIGENTE
# ------------------------------------------
with tab_escaner:
    st.title("🔍 Escáner de Oportunidades Automatizado")
    st.write("Copia los datos básicos del anuncio para que el sistema calcule el riesgo y la rentabilidad al instante.")
    
    col_input, col_prediccion = st.columns(2)
    
    with col_input:
        st.subheader("Datos del Anuncio")
        url_anuncio = st.text_input("Pega el enlace del anuncio aquí (Wallapop / Vinted):")
        titulo_anuncio = st.text_input("Título o descripción corta (Ej: Sony WH-1000XM3 Negros Impecables):")
        precio_anuncio = st.number_input("Precio que pide el vendedor (€):", min_value=0.0, step=5.0)
        
        # Clasificación asistida inteligente de un solo clic
        modelo_detectado = "Otros"
        for clave in DICCIONARIO_MERCADO.keys():
            if clave.lower() in titulo_anuncio.lower() or (url_anuncio and clave.lower().replace(" ", "") in url_anuncio.lower()):
                modelo_detectado = clave
                
        st.info(f"🤖 Sistema ResalePro AI: Detectado automáticamente como **{modelo_detectado}**")
        
        btn_analizar = st.button("Simular e Inspeccionar Rentabilidad")

    with col_prediccion:
        st.subheader("Análisis de Viabilidad Financiera")
        
        if btn_analizar and titulo_anuncio and precio_anuncio > 0:
            # Extraer métricas de nuestra base de datos interna si coincide
            if modelo_detectado in DICCIONARIO_MERCADO:
                meta = DICCIONARIO_MERCADO[modelo_detectado]
                v_venta = meta["venta_estimada"]
                v_gastos = meta["gastos_ajuste"]
                v_rep = meta["reparacion_típica"]
                v_riesgo = meta["riesgo"]
                v_notas = meta["notas"]
            else:
                v_venta = precio_anuncio * 1.5
                v_gastos = 6.0
                v_rep = 0.0
                v_riesgo = "Amarillo (Por determinar)"
                v_notas = "Revisar manualmente el nicho."
            
            # Ecuaciones financieras
            inv_total = precio_anuncio + v_gastos + v_rep
            margen = v_venta - inv_total
            roi = (margen / inv_total * 100) if inv_total > 0 else 0.0
            
            # Renderizado de Tarjetas de decisión
            if roi >= 40.0 and margen >= 30.0:
                st.success(f"🟢 ¡COMPRA RECOMENDADA! ROI estimado del {roi:.1f}%")
            else:
                st.error(f"🔴 COMPRA DESACONSEJADA. Margen demasiado ajustado ({roi:.1f}% ROI)")
                
            st.metric("Margen Neto Esperado", f"{margen:.2f} €")
            st.metric("Inversión Total Estimada", f"{inv_total:.2f} €")
            
            st.markdown(f"**Semáforo de Riesgo:** {v_riesgo}")
            st.caption(f"ℹ️ *Nota del sistema:* {v_notas}")
            
            # Botón definitivo para guardarlo directamente en el inventario con un clic
            if st.button("📥 Confirmar Compra y Añadir al Inventario"):
                next_id = str(len(df) + 1)
                new_row = {
                    "ID": next_id, "Modelo/Categoría": modelo_detectado, "Nombre Oferta": titulo_anuncio,
                    "Precio Compra (€)": precio_anuncio, "Envío/Gastos (€)": v_gastos,
                    "Reparación/Limpieza (€)": v_rep, "Inversión Total (€)": inv_total,
                    "Precio Venta Objetivo (€)": v_venta, "Margen Neto (€)": margen,
                    "ROI %": round(roi, 1), "Estado Operacional": "Necesita Limpieza/Reparación",
                    "Nivel de Riesgo": v_riesgo, "Notas Técnicas": v_notas, "Mes Venta": "En Stock", "Enlace Anuncio": url_anuncio
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.balloons()
                st.success("¡Guardado automáticamente en la pestaña de Inventario!")

# ------------------------------------------
# PESTAÑA 2: INVENTARIO Y STOCK
# ------------------------------------------
with tab_inventario:
    st.title("💸 Panel de Control de Inventario")
    st.dataframe(df, use_container_width=True)

# ------------------------------------------
# PESTAÑA 3: ANÁLISIS DE GANANCIAS
# ------------------------------------------
with tab_ganancias:
    st.title("📈 Distribución de Ganancias por Modelo")
    df_vendidos = df[df["Estado Operacional"] == "Vendido"]
    if df_vendidos.empty:
        st.info("Registra ventas para activar las gráficas.")
    else:
        df_agrupado_modelo = df_vendidos.groupby("Modelo/Categoría", as_index=False)["Margen Neto (€)"].sum()
        fig_ganancias = px.bar(df_agrupado_modelo, x="Modelo/Categoría", y="Margen Neto (€)", color="Modelo/Categoría", text_auto='.2f')
        st.plotly_chart(fig_ganancias, use_container_width=True)

# ------------------------------------------
# PESTAÑA 4: BALANCE MENSUAL
# ------------------------------------------
with tab_balance:
    st.title("📊 Historial y Balance Mensual")
    df_mes = df[df["Mes Venta"] != "En Stock"]
    if df_mes.empty:
        st.info("No hay datos históricos mensuales todavía.")
    else:
        df_balance_mes = df_mes.groupby("Mes Venta", as_index=False).agg({"Inversión Total (€)": "sum", "Margen Neto (€)": "sum"})
        st.table(df_balance_mes)

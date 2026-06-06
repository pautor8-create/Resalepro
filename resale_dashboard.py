import os

code = """
import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# Configuración de la página sin contraseña (Acceso Directo)
st.set_page_config(page_title="ResalePro AI - Modo Avanzado", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# BASE DE DATOS Y CONFIGURACIÓN
# ==========================================
DATA_DIR = "/content/drive/MyDrive/ResalePro_Data"
DATA_FILE = os.path.join(DATA_DIR, "inventario_resale.csv")

if not os.path.exists(DATA_DIR):
    try: os.makedirs(DATA_DIR)
    except: DATA_FILE = "inventario_resale.csv"

columnas = ["ID", "Modelo/Categoría", "Nombre Oferta", "Precio Compra (€)", "Envío/Gastos (€)", "Reparación/Limpieza (€)", "Inversión Total (€)", "Precio Venta Objetivo (€)", "Margen Neto (€)", "ROI %", "Estado Operacional", "Nivel de Riesgo", "Notas Técnicas", "Mes Venta", "Enlace Anuncio"]

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=columnas)
    df_init.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)
df["ID"] = df["ID"].astype(str)

# Base de datos de mercado optimizada (Historial de últimas ventas y rangos reales)
DICCIONARIO_MERCADO = {
    "Sony XM3": {
        "rango_min": 95.0, "rango_max": 125.0, "venta_estimada": 110.0, 
        "gastos_ajuste": 6.5, "reparacion_tipica": 8.0, "riesgo": "Bajo (Alta rotación)", 
        "descripcion": "Auriculares con demanda constante. Se venden rápido si las almohadillas están bien."
    },
    "Bose QC": {
        "rango_min": 110.0, "rango_max": 145.0, "venta_estimada": 125.0, 
        "gastos_ajuste": 6.0, "reparacion_tipica": 10.0, "riesgo": "Bajo (Muy buscados)", 
        "descripcion": "Competencia directa de Sony. El valor se mantiene sólido en mercados de segunda mano."
    },
    "Cámara Compacta Vieja": {
        "rango_min": 70.0, "rango_max": 110.0, "venta_estimada": 90.0, 
        "gastos_ajuste": 4.5, "reparacion_tipica": 5.0, "riesgo": "Medio (Moda temporal Y2K)", 
        "descripcion": "Depende mucho de la estética visual. Alta demanda por público joven actual."
    },
    "Canon Powershot": {
        "rango_min": 120.0, "rango_max": 170.0, "venta_estimada": 145.0, 
        "gastos_ajuste": 5.5, "reparacion_tipica": 5.0, "riesgo": "Bajo (Muy cotizada)", 
        "descripcion": "Modelo icónico dentro de la tendencia vintage. Margen de salida rápido."
    },
}

tab_escaner, tab_inventario, tab_ganancias, tab_balance = st.tabs(["🔍 Escáner Inteligente", "📋 Inventario y Stock", "📈 Análisis de Ganancias", "📊 Balance Mensual"])

with tab_escaner:
    st.title("🔍 Escáner de Oportunidades Basado en Mercado")
    col_input, col_prediccion = st.columns(2)
    
    with col_input:
        st.subheader("Datos del Anuncio")
        url_anuncio = st.text_input("Pega el enlace del anuncio aquí:")
        titulo_anuncio = st.text_input("Título o descripción corta:")
        precio_anuncio = st.number_input("Precio que pide el vendedor (€):", min_value=0.0, step=5.0)
        
        modelo_detectado = "Otros"
        for clave in DICCIONARIO_MERCADO.keys():
            if clave.lower() in titulo_anuncio.lower(): 
                modelo_detectado = clave
        st.info(f"🤖 Sistema ResalePro AI: Detectado automáticamente como **{modelo_detectado}**")
        btn_analizar = st.button("Simular e Inspeccionar Rentabilidad")

    with col_prediccion:
        st.subheader("Informe Técnico de Viabilidad")
        if btn_analizar and titulo_anuncio and precio_anuncio > 0:
            
            # Asignar métricas según mercado o genéricas
            if modelo_detectado in DICCIONARIO_MERCADO:
                meta = DICCIONARIO_MERCADO[modelo_detectado]
                r_min, r_max = meta["rango_min"], meta["rango_max"]
                v_venta = meta["venta_estimada"]
                v_gastos = meta["gastos_ajuste"]
                v_rep = meta["reparacion_tipica"]
                v_riesgo = meta["riesgo"]
                v_desc = meta["descripcion"]
            else:
                r_min, r_max = precio_anuncio * 1.2, precio_anuncio * 1.7
                v_venta = precio_anuncio * 1.4
                v_gastos = 6.0
                v_rep = 0.0
                v_riesgo = "Variable (Sin historial)"
                v_desc = "Producto no catalogado. Análisis basado en estimación matemática estándar."

            inv_total = precio_anuncio + v_gastos + v_rep
            margen = v_venta - inv_total
            roi = (margen / inv_total * 100) if inv_total > 0 else 0.0
            
            # --- NUEVO CEREBRO DE DECISIÓN (Por qué SÍ o por qué NO) ---
            st.markdown("### 📊 Justificación de la Compra:")
            
            # Caso especial cascos o productos de alta rotación con buena ganancia absoluta
            if modelo_detectado in ["Sony XM3", "Bose QC"] and precio_anuncio <= 65.0:
                st.success("🟢 **COMPRA RECOMENDADA (Viabilidad de Rotación Rápida)**")
                st.write(f"**¿Por qué sí?** Aunque el ROI porcentual marque un {roi:.1f}%, el precio de entrada ({precio_anuncio}€) está muy por debajo del valor real de mercado. Estás asegurando un margen neto limpio de {margen:.2f}€ en un producto de alta liquidez que te quitarán de las manos en pocos días. Mitiga el riesgo porcentual gracias al volumen y velocidad de venta.")
            elif roi >= 30.0 and margen >= 20.0:
                st.success("🟢 **COMPRA RECOMENDADA (Métricas Óptimas)**")
                st.write(f"**¿Por qué sí?** Cumple con los umbrales de seguridad financiera. El retorno de inversión es del {roi:.1f}% y dejas colchón suficiente para cubrir cualquier imprevisto de envío o limpieza sin perder dinero.")
            else:
                st.error("🔴 **COMPRA DESACONSEJADA (Riesgo Financiero)**")
                st.write(f"**¿Por qué no?** El precio que pide el vendedor ({precio_anuncio}€) está demasiado inflado o muy cerca del precio de venta final. El margen neto resultante ({margen:.2f}€) o el ROI ({roi:.1f}%) no justifican el tiempo de gestión, empaquetado y el riesgo de que el producto tarde en venderse.")

            st.write(f"ℹ️ *Análisis del catálogo:* {v_desc}")
            
            # --- NUEVA SECCIÓN DE RANGOS DE MERCADO ---
            st.markdown("---")
            st.markdown("### 🎯 Estimación de Precios de Venta")
            st.write(f"Basado en las últimas ventas registradas y anuncios similares activos:")
            
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric("Precio Venta Objetivo (Recomendado)", f"{v_venta:.2f} €")
                st.metric("Margen Neto Neto", f"{margen:.2f} €")
            with col_metric2:
                st.warning(f"Rango Real de Mercado: **{r_min:.0f}€ - {r_max:.0f}€**")
                st.metric("ROI Realizado", f"{roi:.1f} %")
            
            if st.button("📥 Confirmar Compra y Añadir al Inventario"):
                new_row = {"ID": str(len(df)+1), "Modelo/Categoría": modelo_detectado, "Nombre Oferta": titulo_anuncio, "Precio Compra (€)": precio_anuncio, "Envío/Gastos (€)": v_gastos, "Reparación/Limpieza (€)": v_rep, "Inversión Total (€)": inv_total, "Precio Venta Objetivo (€)": v_venta, "Margen Neto (€)": margen, "ROI %": round(roi, 1), "Estado Operacional": "Necesita Limpieza/Reparación", "Nivel de Riesgo": v_riesgo, "Notas Técnicas": v_desc, "Mes Venta": "En Stock", "Enlace Anuncio": url_anuncio}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("¡Guardado con éxito en tu inventario!")

with tab_inventario:
    st.title("💸 Panel de Control de Inventario")
    st.dataframe(df, use_container_width=True)

with tab_ganancias:
    st.title("📈 Distribución de Ganancias por Modelo")
    df_vendidos = df[df["Estado Operacional"] == "Vendido"]
    if df_vendidos.empty: st.info("Registra ventas para activar las gráficas.")
    else:
        df_agrupado_modelo = df_vendidos.groupby("Modelo/Categoría", as_index=False)["Margen Neto (€)"].sum()
        fig_ganancias = px.bar(df_agrupado_modelo, x="Modelo/Categoría", y="Margen Neto (€)", color="Modelo/Categoría", text_auto='.2f')
        st.plotly_chart(fig_ganancias, use_container_width=True)

with tab_balance:
    st.title("📊 Historial y Balance Mensual")
    df_mes = df[df["Mes Venta"] != "En Stock"]
    if df_mes.empty: st.info("No hay datos históricos mensuales todavía.")
    else:
        df_balance_mes = df_mes.groupby("Mes Venta", as_index=False).agg({"Inversión Total (€)": "sum", "Margen Neto (€)": "sum"})
        st.table(df_balance_mes)
"""

with open("resale_dashboard.py", "w") as f:
    f.write(code)

print("[+] ¡Archivo 'resale_dashboard.py' actualizado con el nuevo cerebro de mercado y sin contraseñas!")

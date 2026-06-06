import os

code = """
import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="ResalePro AI - Ultra", layout="wide", initial_sidebar_state="expanded")

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

# Diccionario de Mercado para el Escáner
DICCIONARIO_MERCADO = {
    "Sony XM3": {"rango_min": 95.0, "rango_max": 125.0, "venta_estimada": 110.0, "gastos_ajuste": 6.5, "reparacion_tipica": 8.0, "riesgo": "Bajo (Alta rotación)", "descripcion": "Auriculares con demanda constante. Se venden rápido si las almohadillas están bien."},
    "Bose QC": {"rango_min": 110.0, "rango_max": 145.0, "venta_estimada": 125.0, "gastos_ajuste": 6.0, "reparacion_tipica": 10.0, "riesgo": "Bajo (Muy buscados)", "descripcion": "Competencia directa de Sony. El valor se mantiene sólido en mercados de segunda mano."},
    "Cámara Compacta Vieja": {"rango_min": 70.0, "rango_max": 110.0, "venta_estimada": 90.0, "gastos_ajuste": 4.5, "reparacion_tipica": 5.0, "riesgo": "Medio (Moda temporal Y2K)", "descripcion": "Depende mucho de la estética visual. Alta demanda por público joven actual."},
    "Canon Powershot": {"rango_min": 120.0, "rango_max": 170.0, "venta_estimada": 145.0, "gastos_ajuste": 5.5, "reparacion_tipica": 5.0, "riesgo": "Bajo (Muy cotizada)", "descripcion": "Modelo icónico dentro de la tendencia vintage. Margen de salida rápido."},
}

# Base de conocimiento predictiva de Nichos (Matriz de Inteligencia Estacional y Macroeconómica)
MATRIZ_NICHOS = {
    "Verano": {
        "meses": [6, 7, 8],
        "nombre": "Campaña de Verano y Ocio Estival",
        "factores_contexto": {
            "atmosfericos": "Temperaturas extremas y olas de calor que adelantan la compra de tecnología portátil y de exteriores. Descenso radical del uso de setups fijos de escritorio.",
            "sociales": "Moda Y2K e hiper-estética en redes sociales (Instagram/TikTok). Alta necesidad de registrar viajes, festivales y vacaciones con dispositivos portátiles ligeros.",
            "politicos": "Encarecimiento general de las tasas turísticas y vuelos, lo que provoca que el público joven reduzca presupuesto de gadgets nuevos y recurra al mercado de reventa para sus vacaciones."
        },
        "objetos": [
            {"Objeto": "Cámaras Compactas Y2K (Canon Powershot / Sony Cybershot)", "Demanda": "Crítica (96%)", "Margen": "40-70€", "Días Stock": "3 días", "Estrategia": "Comprar lotes que incluyan tarjeta SD y cargador. El público estival busca soluciones listas para usar en sus viajes de forma inmediata."},
            {"Objeto": "Altavoces Portátiles Bluetooth (JBL / Ultimate Ears)", "Demanda": "Alta (85%)", "Margen": "20-40€", "Días Stock": "5 días", "Estrategia": "Enfocarse en modelos con resistencia al agua certificada (IPX7). Limpiar rejillas a fondo para aumentar el valor percibido."},
            {"Objeto": "Gafas de Sol de Marca (Ray-Ban / Oakley)", "Demanda": "Alta (80%)", "Margen": "25-50€", "Días Stock": "6 días", "Estrategia": "Exigir estuche original en la compra en Wallapop. El margen se duplica si el estado de los cristales es impecable."}
        ]
    },
    "Vuelta al Cole": {
        "meses": [9, 10, 11],
        "nombre": "Campaña de Retorno Educativo y Teletrabajo",
        "factores_contexto": {
            "atmosfericos": "Llegada del otoño, aumento de precipitaciones y bajada de temperaturas. El consumidor pasa más tiempo en interiores (bibliotecas, oficinas, aulas).",
            "sociales": "Necesidad crítica de aislamiento y concentración para el inicio del curso académico y la reactivación de proyectos corporativos tras el parón vacacional.",
            "politicos": "Presión inflacionaria típica de septiembre. Las familias optimizan gastos recortando en tecnología de primera mano en grandes superficies, disparando la demanda de tecnología reacondicionada o usada."
        },
        "objetos": [
            {"Objeto": "Auriculares ANC (Sony XM3/XM4 y Bose QC)", "Demanda": "Masiva (98%)", "Margen": "35-65€", "Días Stock": "2 días", "Estrategia": "Buscar gangas con almohadillas desgastadas. Invertir 6€ en repuestos y vender a precio premium como reacondicionados."},
            {"Objeto": "Teclados y Ratones Ergonómicos (Logitech MX Series)", "Demanda": "Alta (80%)", "Margen": "25-45€", "Días Stock": "7 días", "Estrategia": "Verificar la conectividad Bluetooth y dongle Unifying. La compatibilidad Mac/Windows es un argumento de venta clave."},
            {"Objeto": "Monitores Portátiles USB-C", "Demanda": "Media-Alta (75%)", "Margen": "30-60€", "Días Stock": "9 días", "Estrategia": "Nicho en crecimiento para estudiantes y nómadas digitales que necesitan doble pantalla en espacios reducidos."}
        ]
    },
    "Navidades": {
        "meses": [12, 1],
        "nombre": "Campaña de Regalos y Propósitos de Año Nuevo",
        "factores_contexto": {
            "atmosfericos": "Invierno cerrado. Consumo centrado al 100% en el hogar, entretenimiento digital y ocio indoor.",
            "sociales": "Presión social por regalos navideños e impulsos consumistas. En enero cambia el chip radicalmente hacia la salud, el deporte y el control financiero personal.",
            "politicos": "Estrategias de marketing agresivas en retail que saturan al comprador. El mercado de segunda mano se convierte en el refugio para encontrar stock descatalogado o precios razonables."
        },
        "objetos": [
            {"Objeto": "Consolas Portátiles (Nintendo Switch / Steam Deck)", "Demanda": "Frenética (100%)", "Margen": "50-90€", "Días Stock": "1 día", "Estrategia": "Comprar packs con juegos físicos. Vender los juegos por separado y la consola limpia en su caja original para maximizar el retorno."},
            {"Objeto": "Smartwatches y Pulsómetros (Garmin / Polar / Amazfit)", "Demanda": "Muy Alta (92%)", "Margen": "20-45€", "Días Stock": "4 días", "Estrategia": "Foco absoluto en las dos primeras semanas de enero (auge de los propósitos de gimnasio). Sincronización y batería probadas."},
            {"Objeto": "Cámaras Réflex / Mirrorless de Iniciación", "Demanda": "Alta (85%)", "Margen": "60-120€", "Días Stock": "6 días", "Estrategia": "El regalo estrella. Ofrecer cuerpos con pocos disparos y objetivos de kit limpios."}
        ]
    },
    "Primavera": {
        "meses": [2, 3, 4, 5],
        "nombre": "Campaña de Apertura Exterior y Deporte",
        "factores_contexto": {
            "atmosfericos": "Mejora del tiempo, días más largos y temperaturas agradables que invitan a salir al aire libre y reactivar la actividad física exterior.",
            "sociales": "Operación biquini y auge del ciclismo, running y senderismo de fin de semana.",
            "politicos": "Estabilización de presupuestos familiares post-cuesta de enero. Mayor disposición al gasto recreativo y de salud personal."
        },
        "objetos": [
            {"Objeto": "Ciclocomputadores y GPS (Garmin Edge / Wahoo)", "Demanda": "Alta (85%)", "Margen": "30-65€", "Días Stock": "5 días", "Estrategia": "Incluir soportes de manillar si es posible. La comunidad ciclista valora enormemente el estado de la pantalla y la duración de la batería bajo el sol."},
            {"Objeto": "Auriculares Deportivos de Conducción Ósea (Shokz)", "Demanda": "Alta (78%)", "Margen": "25-50€", "Días Stock": "6 días", "Estrategia": "Nicho premium de alta fidelidad. Desinfectar minuciosamente y destacar la seguridad que ofrecen para correr al aire libre."},
            {"Objeto": "Proyectores Portátiles Domésticos", "Demanda": "Media-Alta (70%)", "Margen": "30-70€", "Días Stock": "8 días", "Estrategia": "Buscados para las primeras noches de terraza y cine de verano improvisado en salones abiertos."}
        ]
    }
}

# ==========================================
# ESTRUCTURA DE PESTAÑAS (TABS)
# ==========================================
tab_escaner, tab_radar, tab_inventario, tab_ganancias, tab_balance = st.tabs([
    "🔍 Escáner Inteligente", "🔮 Radar de Nichos IA", "📋 Inventario y Stock", "📈 Análisis de Ganancias", "📊 Balance Mensual"
])

# ------------------------------------------
# PESTAÑA 1: ESCÁNER INTELIGENTE
# ------------------------------------------
with tab_escaner:
    st.title("🔍 Escáner de Oportunidades")
    col_input, col_prediccion = st.columns(2)
    with col_input:
        st.subheader("Datos del Anuncio")
        url_anuncio = st.text_input("Pega el enlace del anuncio aquí:")
        titulo_anuncio = st.text_input("Título o descripción corta:")
        precio_anuncio = st.number_input("Precio que pide el vendedor (€):", min_value=0.0, step=5.0)
        modelo_detectado = "Otros"
        for clave in DICCIONARIO_MERCADO.keys():
            if clave.lower() in titulo_anuncio.lower(): modelo_detectado = clave
        st.info(f"🤖 Sistema ResalePro AI: Detectado automáticamente como **{modelo_detectado}**")
        btn_analizar = st.button("Simular e Inspeccionar Rentabilidad")

    with col_prediccion:
        st.subheader("Informe Técnico de Viabilidad")
        if btn_analizar and titulo_anuncio and precio_anuncio > 0:
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
                v_riesgo = "Variable"
                v_desc = "Producto no catalogado."

            inv_total = precio_anuncio + v_gastos + v_rep
            margen = v_venta - inv_total
            roi = (margen / inv_total * 100) if inv_total > 0 else 0.0
            
            st.markdown("### 📊 Justificación de la Compra:")
            if modelo_detectado in ["Sony XM3", "Bose QC"] and precio_anuncio <= 65.0:
                st.success("🟢 **COMPRA RECOMENDADA (Viabilidad de Rotación Rápida)**")
                st.write(f"**¿Por qué sí?** El precio de entrada ({precio_anuncio}€) está muy por debajo del valor real. Aseguras {margen:.2f}€ limpios en un producto que se vende en días.")
            elif roi >= 30.0 and margen >= 20.0:
                st.success("🟢 **COMPRA RECOMENDADA (Métricas Óptimas)**")
                st.write(f"**¿Por qué sí?** Cumple umbrales financieros con ROI del {roi:.1f}% y dejas colchón para imprevistos.")
            else:
                st.error("🔴 **COMPRA DESACONSEJADA (Riesgo Financiero)**")
                st.write(f"**¿Por qué no?** El precio está muy inflado. El margen neto ({margen:.2f}€) no justifica el riesgo.")

            st.markdown("---")
            st.markdown("### 🎯 Estimación de Precios de Venta")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Precio Venta Objetivo", f"{v_venta:.2f} €")
                st.metric("Margen Neto", f"{margen:.2f} €")
            with col_m2:
                st.warning(f"Rango Real: {r_min:.0f}€ - {r_max:.0f}€")
                st.metric("ROI", f"{roi:.1f} %")
            
            if st.button("📥 Confirmar Compra y Añadir al Inventario"):
                new_row = {"ID": str(len(df)+1), "Modelo/Categoría": modelo_detectado, "Nombre Oferta": titulo_anuncio, "Precio Compra (€)": precio_anuncio, "Envío/Gastos (€)": v_gastos, "Reparación/Limpieza (€)": v_rep, "Inversión Total (€)": inv_total, "Precio Venta Objetivo (€)": v_venta, "Margen Neto (€)": margen, "ROI %": round(roi, 1), "Estado Operacional": "Necesita Limpieza/Reparación", "Nivel de Riesgo": v_riesgo, "Notas Técnicas": v_desc, "Mes Venta": "En Stock", "Enlace Anuncio": url_anuncio}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("¡Guardado en inventario!")

# ------------------------------------------
# PESTAÑA NUEVA: RADAR DE NICHOS IA (AUTOMÁTICO)
# ------------------------------------------
with tab_radar:
    # 1. Detección automática del tiempo real del sistema
    ahora = datetime.now()
    mes_actual = ahora.month
    nombre_mes = ahora.strftime('%B')
    anio_actual = ahora.year
    
    st.title("🔮 Radar Autónomo de Nichos de Mercado")
    st.markdown(f"**🤖 Estado del Sistema:** Analizando el contexto macroeconómico global y meteorológico para hoy: **{nombre_mes} de {anio_actual}**.")
    
    # 2. Algoritmo de emparejamiento estacional interno
    temporada_activa = "Primavera" # Por defecto
    for temp, data in MATRIZ_NICHOS.items():
        if mes_actual in data["meses"]:
            temporada_activa = temp
            break
            
    info_temp = MATRIZ_NICHOS[temporada_activa]
    
    # 3. Renderizado de la macro-evaluación del entorno sin intervención del usuario
    st.success(f"📌 **Campaña Detectada por la IA:** {info_temp['nombre']}")
    
    st.markdown("### 🌐 Evaluación de Variables de Entorno (Filtro Cruzado)")
    c_atm, c_soc, c_pol = st.columns(3)
    with c_atm:
        st.error("🌤️ **Factor Atmosférico**")
        st.caption(info_temp["factores_contexto"]["atmosfericos"])
    with c_soc:
        st.warning("👥 **Factor Social / Tendencia**")
        st.caption(info_temp["factores_contexto"]["sociales"])
    with c_pol:
        st.info("⚖️ **Factor Político / Económico**")
        st.caption(info_temp["factores_contexto"]["politicos"])
        
    st.markdown("---")
    st.subheader("🎯 Objetos Nicho Recomendados para Cazar Ahora Mismo:")
    
    for obj in info_temp["objetos"]:
        with st.expander(f"📦 {obj['Objeto']} | Interés: {obj['Demanda']} | Beneficio Neto: ~{obj['Margen']}"):
            col_izq, col_der = st.columns([1, 4])
            with col_izq:
                st.metric("Rotación de Stock", obj["Días Stock"])
                st.caption("Tiempo límite recomendado antes de liquidar")
            with col_der:
                st.markdown("**💡 Plan de Acción y Captura:**")
                st.write(obj["Estrategia"])

# ------------------------------------------
# PESTAÑAS RESTANTES (INVENTARIO, GANANCIAS, BALANCE)
# ------------------------------------------
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

print("[+] ¡El motor autónomo estacional-contextual ha sido integrado con éxito!")

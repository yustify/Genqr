import streamlit as st
import qrcode
from PIL import Image
import io

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador QR", page_icon="🔳", layout="centered")

# --- ESTILO CSS (Opcional, para mejorar un poco la apariencia) ---
st.markdown("""
<style>
    h1 {
        text-align: center;
        color: #4CAF50; /* Un verde atractivo */
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5em 1em;
    }
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("🔳 Generador de Códigos QR")
st.write("Introduce el texto o la URL que quieres convertir en un código QR.")

# --- ENTRADA DE TEXTO ---
# Usamos una clave 'qr_input' para poder borrar el texto después de generar
input_data = st.text_input("Texto o URL:", key="qr_input", placeholder="Ej: https://www.google.com")

# --- BOTÓN PARA GENERAR ---
if st.button("🔗 Generar QR"):
    if input_data:
        try:
            # --- LÓGICA DE GENERACIÓN DEL QR ---
            qr = qrcode.QRCode(
                version=1, # Controla el tamaño (1 es pequeño)
                error_correction=qrcode.constants.ERROR_CORRECT_L, # Nivel de corrección de errores
                box_size=10, # Tamaño de cada "caja" del QR
                border=4, # Grosor del borde
            )
            qr.add_data(input_data)
            qr.make(fit=True)

            # Crear la imagen QR usando Pillow
            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            # --- MOSTRAR LA IMAGEN ---
            st.image(img, caption='Tu Código QR', use_column_width=True)

            # --- OPCIÓN DE DESCARGA ---
            # Convertir la imagen a bytes para el botón de descarga
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Descargar QR (.png)",
                data=byte_im,
                file_name="codigo_qr.png",
                mime="image/png"
            )

            # Opcional: Borrar el texto del input después de generar
            # st.session_state.qr_input = ""

        except Exception as e:
            st.error(f"Ocurrió un error al generar el QR: {e}")
    else:
        st.warning("Por favor, introduce algún texto o URL.")


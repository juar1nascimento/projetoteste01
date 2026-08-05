import io
import cv2
import numpy as np
import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Sistema de Código de Barras",
    page_icon="🔍",
    layout="wide"
)

def decode_barcode(image_bytes):
    """Decodifica código de barras de uma imagem utilizando OpenCV."""
    image_bytes.seek(0)
    file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    detector = cv2.barcode.BarcodeDetector()
    ok, decoded_info, decoded_type, _ = detector.detectAndDecode(img)
    
    results = []
    if ok:
        for info, btype in zip(decoded_info, decoded_type):
            if info:
                results.append({"conteudo": info, "tipo": btype})
    return results, img

def generate_barcode(code_type, code_value):
    """Gera a imagem do código de barras em memória."""
    barcode_class = barcode.get_barcode_class(code_type)
    rv = io.BytesIO()
    code_instance = barcode_class(code_value, writer=ImageWriter())
    code_instance.write(rv)
    rv.seek(0)
    return rv

# Interface Principal
st.title("📦 Sistema Web de Leitura e Geração de Código de Barras")

tab_read, tab_generate = st.tabs(["📷 Leitura / Escaneamento", "⌨️ Digitação / Geração"])

# --- ABA 1: LEITURA ---
with tab_read:
    st.header("Leitura de Código de Barras")
    source_option = st.radio("Selecione a fonte de entrada:", ["Upload de Imagem", "Câmera ao Vivo"])

    image_file = None
    if source_option == "Upload de Imagem":
        image_file = st.file_uploader("Envie uma imagem contendo código de barras", type=["png", "jpg", "jpeg", "webp"])
    else:
        image_file = st.camera_input("Tire uma foto do código de barras")

    if image_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(image_file, caption="Entrada", use_container_width=True)

        with col2:
            with st.spinner("Processando imagem..."):
                results, _ = decode_barcode(image_file)
                
                if results:
                    st.success(f"Encontrado(s) {len(results)} código(s)!")
                    for i, res in enumerate(results, 1):
                        st.text_input(f"Conteúdo #{i}", value=res["conteudo"], key=f"res_{i}")
                        st.caption(f"Tipo detectado: {res['tipo']}")
                else:
                    st.warning("Nenhum código de barras identificado na imagem.")

# --- ABA 2: GERAÇÃO ---
with tab_generate:
    st.header("Geração de Código de Barras")
    
    col_input, col_preview = st.columns([1, 1])
    
    with col_input:
        bc_type = st.selectbox(
            "Selecione o Padrão",
            ["code128", "ean13", "code39", "upc"]
        )
        bc_value = st.text_input("Digite o código / valor", value="123456789012")
        
        generate_btn = st.button("Gerar Código", type="primary")

    with col_preview:
        if generate_btn or bc_value:
            try:
                img_buf = generate_barcode(bc_type, bc_value)
                st.image(img_buf, caption=f"Código {bc_type.upper()}: {bc_value}")
                
                st.download_button(
                    label="Download PNG",
                    data=img_buf.getvalue(),
                    file_name=f"barcode_{bc_value}.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Erro ao gerar código de barras: {str(e)}")
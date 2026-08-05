import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Leitor USB - Streamlit", layout="wide")

# Inicialização do estado da sessão (Session State) revisado
if "historico_leituras" not in st.session_state:
    st.session_state.historico_leituras = []

if "codigo_input" not in st.session_state:
    st.session_state.codigo_input = ""

def processar_codigo():
    """Callback disparado quando o leitor envia o comando ENTER."""
    codigo = st.session_state.codigo_input.strip()
    if codigo:
        st.session_state.historico_leituras.insert(0, codigo)
        st.toast(f"Código lido com sucesso: {codigo}", icon="✅")
        st.session_state.codigo_input = ""

st.title("📟 Leitura via Leitor USB (Emulador de Teclado)")
st.caption("Aponte o leitor para o código de barras. Os dados serão capturados automaticamente.")

with st.form(key="form_leitor_usb", clear_on_submit=True):
    codigo_bipado = st.text_input(
        label="Aguardando leitura do código...",
        value=st.session_state.codigo_input,
        key="codigo_input",
        placeholder="O código aparecerá aqui ao bipar...",
        help="Mantenha o foco neste campo para capturar o bip."
    )
    
    submit_button = st.form_submit_button(
        label="Processar / Ler", 
        on_click=processar_codigo
    )

# --- Exibição do Histórico de Leituras ---
st.divider()
st.subheader("📋 Últimos Códigos Capturados")

if st.session_state.historico_leituras:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.dataframe(
            {"Código de Barras": st.session_state.historico_leituras},
            use_container_width=True
        )
    
    with col2:
        if st.button("Limpar Histórico", type="secondary"):
            st.session_state.historico_leituras = []
            st.rerun()
else:
    st.info("Nenhum código lido até o momento.")

# Força o foco no campo de input via JavaScript
components.html(
    """
    <script>
        const doc = window.parent.document;
        const inputs = doc.querySelectorAll('input[type="text"]');
        if (inputs.length > 0) {
            inputs[0].focus();
        }
    </script>
    """,
    height=0,
)
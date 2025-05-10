import streamlit as st
import os
import requests # Usado para fazer chamadas HTTP para a API do OpenManus
import json     # Usado para formatar o payload da API
import time     # Usado para simular atrasos da API neste exemplo

# Configura o layout da página para ser amplo
st.set_page_config(layout="wide")

# --- Configuração da Aplicação ---
# O usuário precisará ajustar a URL da API do OpenManus.
# Pode ser definida via variável de ambiente OPENMANUS_API_URL ou diretamente no código.
OPENMANUS_API_URL = os.getenv("OPENMANUS_API_URL", "http://localhost:8000/api/v1/chat") 

st.title("Interface de Chat Funcional")
st.caption(f"Interagindo com a API do OpenManus (esperada em: {OPENMANUS_API_URL})")

# --- Gerenciamento de Estado da Sessão ---
# Inicializa o histórico do chat se ainda não existir na sessão do Streamlit.
if "messages" not in st.session_state:
    st.session_state.messages = []
# Inicializa informações do arquivo carregado (para o prompt atual) se não existir.
if "uploaded_file_info" not in st.session_state:
    st.session_state.uploaded_file_info = None 

# --- Exibição do Histórico do Chat ---
# Itera sobre todas as mensagens armazenadas no estado da sessão e as exibe.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): # Define o avatar (usuário ou assistente)
        st.markdown(msg["content"]) # Exibe o conteúdo da mensagem
        # Se a mensagem tiver arquivos anexados, exibe suas informações.
        if msg.get("files"):
            for file_info in msg["files"]:
                st.markdown(f"_Arquivo Anexado: {file_info['name']} ({file_info['type']}, {file_info['size']} bytes)_ ")

# --- Layout da Interface em Colunas ---
# Divide a interface em duas colunas: uma maior para o chat e uma menor para o upload de arquivos.
col1, col2 = st.columns([3, 1])

with col1:
    # Campo de entrada de texto para o usuário digitar suas mensagens.
    prompt = st.chat_input("Digite sua mensagem...")

with col2:
    st.subheader("Anexar Arquivo")
    # Componente de upload de arquivos do Streamlit.
    uploaded_file = st.file_uploader(
        "Escolha um arquivo", 
        key="file_uploader", # Chave única para o componente
        # Lista de tipos de arquivo aceitos (bastante abrangente).
        type=[
            'txt', 'md', 'json', 'csv', 'xml', 'html', 'css', 'js', 'py', 'java', 'c', 'cpp', 'h', 'hpp', 'sh', 'rb', 'php', 'sql', 
            'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'odt', 'ods', 'odp', 
            'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'tiff', 'webp', 
            'zip', 'tar', 'gz', 'rar', '7z', 
            'mp3', 'wav', 'ogg', 'flac', 
            'mp4', 'mov', 'avi', 'mkv', 'webm' 
        ]
    )

    # Se um arquivo for carregado pelo usuário:
    if uploaded_file is not None:
        # Armazena as informações do arquivo no estado da sessão para serem usadas quando o prompt for enviado.
        st.session_state.uploaded_file_info = {
            "name": uploaded_file.name,
            "type": uploaded_file.type,
            "size": uploaded_file.size,
            # "bytes": uploaded_file.getvalue() # Descomente com cautela: carregar bytes de arquivos grandes na memória pode ser problemático.
        }
        st.success(f"Arquivo '{uploaded_file.name}' pronto para anexar.") # Feedback visual para o usuário.

# --- Processamento da Entrada do Usuário ---
# Se o usuário digitou um prompt e pressionou Enter:
if prompt:
    # Prepara a estrutura da mensagem do usuário.
    user_message_data = {"role": "user", "content": prompt, "files": []}
    
    # Verifica se há um arquivo carregado e pronto para ser anexado a este prompt.
    if st.session_state.uploaded_file_info:
        user_message_data["files"].append(st.session_state.uploaded_file_info)
    
    # Adiciona a mensagem do usuário (com ou sem arquivo) ao histórico.
    st.session_state.messages.append(user_message_data)
    
    # Exibe a mensagem do usuário na interface imediatamente.
    with st.chat_message("user"):
        st.markdown(prompt)
        if user_message_data["files"]:
            for file_info in user_message_data["files"]:
                st.markdown(f"_Arquivo Anexado: {file_info['name']} ({file_info['type']}, {file_info['size']} bytes)_ ")

    # Limpa as informações do arquivo carregado da sessão, pois já foi associado a este prompt.
    st.session_state.uploaded_file_info = None

    # --- Chamada à API do OpenManus (Simulada neste exemplo) ---
    # Prepara o payload para a API do OpenManus.
    api_payload = {
        "user_input": prompt,
        "session_id": st.session_state.get("session_id", "streamlit_chat_session"), # Exemplo de ID de sessão.
        "attachments": user_message_data["files"] # Lista de dicionários com informações dos arquivos.
    }

    assistant_response_content = ""
    try:
        # Bloco de simulação: substitua pela chamada real à API.
        # Exemplo de como a chamada real poderia ser:
        # response = requests.post(OPENMANUS_API_URL, json=api_payload, timeout=60)
        # response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx).
        # assistant_response_content = response.json().get("response", "Desculpe, não consegui processar sua solicitação.")
        
        # Lógica de simulação para este exemplo:
        if user_message_data["files"]:
            file_names = ", ".join([f['name'] for f in user_message_data["files"]])
            assistant_response_content = f"(Simulado) Recebi sua mensagem: '{prompt}' e o(s) arquivo(s): {file_names}. Eu os processaria agora."
        else:
            assistant_response_content = f"(Simulado) Recebi sua mensagem: '{prompt}'. Como posso ajudar?"
        
        time.sleep(1) # Simula um pequeno atraso da API.

    except requests.exceptions.RequestException as e:
        # Tratamento de erro para falhas de conexão com a API.
        assistant_response_content = f"Erro ao conectar com a API do OpenManus: {e}"
    except Exception as e:
        # Tratamento de erro para outras exceções inesperadas.
        assistant_response_content = f"Ocorreu um erro inesperado: {e}"
    # --- Fim da Simulação da Chamada à API ---

    # Adiciona a resposta do assistente ao histórico e a exibe na interface.
    st.session_state.messages.append({"role": "assistant", "content": assistant_response_content})
    with st.chat_message("assistant"):
        st.markdown(assistant_response_content)
    
    # Nota sobre limpar o file_uploader visualmente: 
    # O Streamlit pode manter o nome do arquivo visível no componente file_uploader mesmo após o envio.
    # Resetar o estado visual do uploader de forma programática pode ser complexo sem um rerun completo ou truques com chaves.
    # A lógica atual garante que o arquivo só é anexado ao prompt se estiver presente no momento do envio do prompt.

# --- Opções na Barra Lateral ---
st.sidebar.title("Opções")
# Botão para limpar o histórico do chat.
if st.sidebar.button("Limpar Histórico do Chat"):
    st.session_state.messages = [] # Limpa as mensagens.
    st.session_state.uploaded_file_info = None # Limpa qualquer informação de arquivo pendente.
    st.rerun() # Re-executa o script para atualizar a interface.

st.sidebar.markdown("--- ")
st.sidebar.markdown("**Sobre:** Esta é uma interface de chat funcional para interagir com um agente OpenManus. Configure a URL da API do OpenManus (variável de ambiente `OPENMANUS_API_URL` ou diretamente no código) se necessário.")

# --- Como Executar ---
# 1. Salve este código como `app.py` (ou outro nome .py).
# 2. Certifique-se de ter o Streamlit instalado: `pip install streamlit`.
# 3. Execute no terminal: `streamlit run app.py`.


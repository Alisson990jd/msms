# Interface de Chat Funcional com Streamlit para OpenManus

Esta é uma aplicação de interface de chat simples, construída com Streamlit, projetada para interagir com um backend de agente OpenManus. Ela permite enviar mensagens de texto e anexar arquivos, que seriam então processados pelo agente OpenManus.

## Funcionalidades

*   Interface de chat com histórico de mensagens.
*   Entrada de texto para enviar prompts/comandos ao agente.
*   Funcionalidade de upload de arquivos para anexar contextos ou dados às suas mensagens.
*   Exibição de informações sobre os arquivos anexados (nome, tipo, tamanho).
*   Botão para limpar o histórico do chat.
*   Configuração da URL da API do OpenManus via variável de ambiente ou diretamente no código.

## Pré-requisitos

*   Python 3.7 ou superior.
*   `pip` (gerenciador de pacotes Python).

## Instalação

1.  **Clone ou baixe o arquivo `app.py`** para o seu sistema local.

2.  **Instale as dependências necessárias.** A principal dependência é o Streamlit. Você também precisará da biblioteca `requests` se for fazer chamadas HTTP reais para a API do OpenManus (o exemplo atual simula essa chamada).

    ```bash
    pip install streamlit requests
    ```

## Configuração

Antes de executar a aplicação, você precisa configurar a URL da API do seu agente OpenManus. O agente OpenManus é o backend que processará as mensagens e os arquivos.

1.  **URL da API do OpenManus:**
    *   O script `app.py` tentará ler a URL da API da variável de ambiente `OPENMANUS_API_URL`.
    *   **Recomendado:** Defina a variável de ambiente antes de executar o script:
        ```bash
        export OPENMANUS_API_URL="http://seu-servidor-openmanus:porta/api/endpoint"
        ```
        (No Windows, use `set OPENMANUS_API_URL="http://seu-servidor-openmanus:porta/api/endpoint"`)
    *   **Alternativa:** Você pode modificar diretamente a linha no arquivo `app.py`:
        ```python
        OPENMANUS_API_URL = "http://localhost:8000/api/v1/chat" # Altere para a URL correta
        ```
        O valor padrão no script é `http://localhost:8000/api/v1/chat`, que é um placeholder.

2.  **API do OpenManus (Backend):**
    *   Certifique-se de que seu agente OpenManus está em execução e acessível na URL configurada.
    *   A API do OpenManus deve ser capaz de receber um payload JSON com `user_input` (string) e `attachments` (lista de dicionários, onde cada dicionário contém `name`, `type`, `size` do arquivo).
    *   A API deve retornar uma resposta JSON com um campo `response` contendo a mensagem do assistente.
    *   O código atual em `app.py` *simula* a chamada à API e a resposta. Você precisará descomentar e adaptar o bloco de chamada `requests.post` para se conectar ao seu backend OpenManus real.

## Como Executar

1.  Navegue até o diretório onde você salvou o arquivo `app.py`.
2.  Execute o seguinte comando no seu terminal:

    ```bash
    streamlit run app.py
    ```

3.  O Streamlit iniciará um servidor web local e abrirá a interface de chat no seu navegador padrão. Geralmente, o endereço será `http://localhost:8501`.

## Como Usar

1.  **Enviar Mensagens:** Digite sua mensagem no campo de entrada na parte inferior da área de chat e pressione Enter.
2.  **Anexar Arquivos:**
    *   Clique no botão "Escolha um arquivo" na coluna da direita.
    *   Selecione o arquivo que deseja anexar.
    *   Uma mensagem de sucesso indicará que o arquivo está "pronto para anexar".
    *   Digite sua mensagem de texto relacionada ao arquivo e pressione Enter. As informações do arquivo serão enviadas junto com o seu prompt para o OpenManus.
3.  **Limpar Histórico:** Clique no botão "Limpar Histórico do Chat" na barra lateral para remover todas as mensagens da interface.

## Estrutura do Código (`app.py`)

*   **Importações:** `streamlit` para a interface, `os` para variáveis de ambiente, `requests` e `json` para chamadas de API (simuladas/reais), `time` para simulação de atraso.
*   **Configuração:** Definição da URL da API e título da página.
*   **Gerenciamento de Estado:** Uso de `st.session_state` para armazenar o histórico de mensagens (`messages`) e informações do arquivo atualmente carregado (`uploaded_file_info`).
*   **Layout:** A interface é dividida em duas colunas para o chat e o uploader de arquivos. A barra lateral contém opções como limpar o histórico.
*   **Processamento de Entrada:** Lógica para lidar com o envio de prompts e o anexo de arquivos.
*   **Chamada à API (Simulada):** Um bloco de código que demonstra como a chamada à API do OpenManus seria feita. **Este bloco precisa ser adaptado para seu backend real.**
*   **Exibição de Mensagens:** Renderização das mensagens do usuário e do assistente, incluindo informações de arquivos anexados.

## Próximos Passos (Para o Desenvolvedor)

*   **Implementar a Chamada Real à API:** Substitua o bloco de simulação no `app.py` pela lógica real de chamada à API do seu agente OpenManus usando a biblioteca `requests`.
*   **Tratamento de Erros da API:** Melhore o tratamento de erros para diferentes respostas da API.
*   **Processamento de Arquivos no Backend:** Certifique-se de que seu agente OpenManus (backend) está preparado para receber e processar as informações dos arquivos anexados.
*   **Segurança:** Se esta interface for exposta publicamente, considere adicionar autenticação e outras medidas de segurança.


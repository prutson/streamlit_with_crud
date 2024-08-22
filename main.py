import streamlit as st
from pages import login, show_home, analyze_players, register_user
import json
import os
import tempfile
import time

# Criar um arquivo temporário para o session_state.json
temp_dir = tempfile.gettempdir()
STATE_FILE = os.path.join(temp_dir, "session_state.json")

# Função para carregar o estado de um arquivo
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            return json.load(file)
    return {}

# Função para salvar o estado em um arquivo
def save_state(state):
    with open(STATE_FILE, "w") as file:
        json.dump(state, file)

# Função para verificar se o arquivo deve ser deletado
def check_and_delete_state_file(max_age_seconds=3600):  # 1 hora por padrão
    if os.path.exists(STATE_FILE):
        file_age = time.time() - os.path.getmtime(STATE_FILE)
        if file_age > max_age_seconds:
            os.remove(STATE_FILE)

# Verificar se o arquivo temporário deve ser apagado
check_and_delete_state_file()

# Carregar o estado no início
state = load_state()

# Função principal da aplicação
def main(): 
    # Inicialização de session_state a partir do estado carregado
    if 'logado' not in st.session_state:
        st.session_state['logado'] = state.get('logado', False)
    if 'page' not in st.session_state:
        st.session_state['page'] = state.get('page', 'login')  # Inicia na página de login por padrão
    if 'cadastro' not in st.session_state:
        st.session_state['cadastro'] = state.get('cadastro', False)

    # Verifica a página atual e exibe o conteúdo correspondente
    if st.session_state['page'] == 'login' and not st.session_state['logado']:
        login()
        if st.session_state['logado']:
            st.session_state['page'] = 'Home'
            state['logado'] = True
            state['page'] = 'Home'
            save_state(state)
            st.rerun() 
    elif st.session_state['page'] == 'register' and st.session_state['cadastro']:
        register_user()
        state['cadastro'] = True
        save_state(state)  # Salvar o estado atualizado
    elif st.session_state['logado']:
        page = st.sidebar.selectbox("Navegação", ["Home", "Analise de Jogadores"])

        if page == "Home":
            st.session_state['page'] = 'Home'
            show_home()
        elif page == "Analise de Jogadores":
            st.session_state['page'] = 'Analise de Jogadores'
            analyze_players()

        # Botão de Deslogar
        if st.sidebar.button("Deslogar"):
            # Atualiza o estado para deslogado
            st.session_state['logado'] = False
            st.session_state['page'] = 'login'
            state['logado'] = False
            state['page'] = 'login'
            save_state(state)  # Salvar o estado atualizado antes do rerun

            # Recarrega a aplicação
            st.rerun()

        state['page'] = st.session_state['page']
        save_state(state)  # Salvar o estado atualizado

if __name__ == '__main__':
    main()

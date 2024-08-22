import streamlit as st
from database.functions import *
from database.models import User

def register_user():
    st.markdown("# Cadastro de Usuário")
    
    name = st.text_input("Nome")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    confirm_password = st.text_input("Confirme sua senha", type="password")

    if st.button("Cadastrar"):
        if not name or not email or not password:
            st.error("Todos os campos são obrigatórios.")
        elif password != confirm_password:
            st.error("As senhas não coincidem.")
        else:
            try:
                create_entity(engine, 'user', name=name, email=email, password=password)
                st.success("Usuário cadastrado com sucesso!")
            except ValueError as e:
                st.error(f"Erro ao cadastrar: {str(e)}")
            except IntegrityError:
                st.error("Erro de integridade ao tentar cadastrar o usuário.")

    if st.button('Retornar para login'):
        st.session_state['cadastro'] = False
        st.rerun()

def login():
    if st.session_state.get('cadastro', False):
        register_user()
    else:
        with st.container():
            st.markdown('Bem-vindo à tela de login')

            users = read_all(engine, 'user')
            users = {user['name']: user for user in users}

            user_name = st.text_input('Digite o usuário')
            password = st.text_input('Digite sua senha', type='password')

            if st.button('Logar'):
                usuario = users.get(user_name)
                if usuario and User(**usuario).verify_password(password):
                    st.success('Login efetuado com sucesso!')
                    st.session_state['usuario'] = usuario
                    st.session_state['logado'] = True
                    st.session_state['page'] = 'Home'
                else:
                    st.error('Usuário ou senha incorretos')

            if st.button('Ainda não tem uma conta? Cadastre-se aqui'):
                st.session_state['cadastro'] = True
                st.rerun()  

def show_home():

    st.markdown('# Fifa Official Dataset')
    st.sidebar.markdown("Desenvolvido por [João Pereira](https://github.com/prutson)") 

    btn = st.button("Acesse os dados no Kaggle")
    if btn:
        st.markdown("[Clique aqui para acessar os dados](https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data)")

    st.markdown(
        """
        O conjunto de dados
        de jogadores de futebol de 2017 a 2023 fornece informações 
        abrangentes sobre jogadores de futebol profissionais.
        O conjunto de dados contém uma ampla gama de atributos, incluindo dados demográficos 
        do jogador, características físicas, estatísticas de jogo, detalhes do contrato e 
        afiliações de clubes. 
        
        Com **mais de 17.000 registros**, este conjunto de dados oferece um recurso valioso para 
        analistas de futebol, pesquisadores e entusiastas interessados em explorar vários 
        aspectos do mundo do futebol, pois permite estudar atributos de jogadores, métricas de 
        desempenho, avaliação de mercado, análise de clubes, posicionamento de jogadores e 
        desenvolvimento do jogador ao longo do tempo.
        """
    )


def analyze_players():
    from page.players import analyze_players
    analyze_players()
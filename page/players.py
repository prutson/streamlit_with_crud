import streamlit as st
from shared import DefaultConfig


def analyze_players():
    # Instanciando a configuração padrão
    config = DefaultConfig()
    df_data = config.df_data


    # Criando filtros para o sidebar
    clubes = df_data['Club'].unique()
    club = st.sidebar.selectbox('Clube', clubes)

    df_players = df_data[df_data['Club'] == club]
    players = df_players['Name'].unique()
    player = st.sidebar.selectbox('Jogador', players)

    player_stats = df_data[df_data['Name'] == player].iloc[0]   # Df com o jogador selecionado nos filtros

    # Começando a criar visuais

    # header com foto e nome do jogador
    st.image(player_stats["Photo"])
    st.title(player_stats["Name"])
    st.markdown(f"**Clube:** {player_stats['Club']}")
    st.markdown(f"**Posição:** {player_stats['Position']}")

    # Area com coluna e mais informações sobre o jogador
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"**Idade:** {player_stats['Age']}")
    col2.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100}")
    col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)']*0.453:.2f}")

    st.divider()
    st.subheader(f"Overall {player_stats['Overall']}")
    st.progress(int(player_stats["Overall"]))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Valor de mercado", value=f"£ {player_stats['Value(£)']:,}")
    col2.metric(label="Remuneração semanal", value=f"£ {player_stats['Wage(£)']:,}")
    col3.metric(label="Cláusula de rescisão", value=f"£ {player_stats['Release Clause(£)']:,}")


    st.sidebar.markdown("Desenvolvido por [João Pereira](https://github.com/prutson)")

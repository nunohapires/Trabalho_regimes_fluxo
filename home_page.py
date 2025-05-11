import streamlit as st

from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Simulação de Regimes de Fluxo",
    page_icon="🔍",
    layout="wide",
)

# Função para criar um efeito de cartão
def create_card(title, content, icon="🔷"):
    st.markdown(f"""
    <div style="border-radius:10px;padding:20px;margin:10px 0px">
        <h3>{icon} {title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(90deg, #13293D 0%, #006494 100%); padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin-bottom: 30px">
    <div style="text-align:center">
        <h1 style="color:#ffffff; font-size:2.5rem; font-weight:700; margin-bottom:10px; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
            SIMULAÇÃO E COMPARAÇÃO DOS REGIMES DE FLUXO
        </h1>
        <div style="width:80%; height:2px; background-color:rgba(255,255,255,0.5); margin:10px auto 20px auto;"></div>
        <h2 style="color:#E8F1F2; font-size:1.5rem; font-weight:400; letter-spacing:1px; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
            COM BASE NA EQUAÇÃO DA DIFUSIVIDADE HIDRÁULICA
        </h2>
    </div>
</div>
""", unsafe_allow_html=True)

# Linha separadora
st.markdown("<hr>", unsafe_allow_html=True)

# Layout com colunas
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("###  Descrição do Projeto")
    st.write("""
    Este aplicativo simula o comportamento da pressão ao longo do tempo e do espaço em um reservatório 
    radialmente simétrico, utilizando as soluções analíticas da Equação da Difusividade Hidráulica.
    
    O modelo permite a análise comparativa dos três principais regimes de escoamento:
    """)
    
    create_card(
        "Regime Permanente", 
        "Estado em que a pressão não varia com o tempo em nenhum ponto do reservatório, resultando em um equilíbrio entre a produção e o influxo.",
        ""
    )
    
    create_card(
        "Regime Pseudopermanente", 
        "Comportamento de pressão quando as fronteiras do reservatório são sentidas, mas a pressão declina a uma taxa constante em todo o reservatório.",
        ""
    )
    
    create_card(
        "Regime Transiente", 
        "Estado inicial em que a distribuição de pressão está mudando com o tempo, antes que qualquer fronteira seja sentida.",
        ""
    )

with col2:
    st.markdown("###  Funcionalidades")
    st.markdown("""
    - Ajuste de parâmetros de reservatório
    - Visualização de gráficos para cada regime
    - Comparação de pressões em diferentes raios
    - Análise da evolução temporal da pressão
    """)
    
    st.markdown("###  Como usar")
    st.markdown("""
    1. Navegue para a página "Simulação" no menu lateral
    2. Ajuste os parâmetros do reservatório
    3. Selecione os raios e tempos de interesse
    4. Clique em "Calcular" para gerar os gráficos
    """)

# Linha separadora
st.markdown("<hr>", unsafe_allow_html=True)

# Informações do autor
st.markdown("### 👨‍🎓 Autor")
col_info1, col_info2 = st.columns([1, 2])

    
with col_info2:
    st.markdown("""
    **Nome:** Nuno Henrique Albuquerque Pires  
    **Curso:** Engenharia de Petróleo  
    **LinkedIn:** [www.linkedin.com/in/nuno-pires545](https://www.linkedin.com/in/nuno-pires545)  
    """)

# Rodapé com direitos autorais
year = datetime.now().year
st.markdown(f"""
<div style="text-align:center;margin-top:50px;color:#666666">
    <p> {year} Nuno Henrique Albuquerque Pires - Todos os direitos reservados</p>
    <p>Desenvolvido como parte do trabalho acadêmico em Engenharia de Petróleo</p>
</div>
""", unsafe_allow_html=True)



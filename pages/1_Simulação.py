import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expi
import time

# Configurações da página
st.set_page_config(
    page_title="Simulação de Pressão",
    page_icon="🔬",
    layout="wide"
)

# Função para criar cabeçalho estilizado profissional
def create_header(title, subtitle=None):
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #13293D 0%, #006494 100%); padding: 25px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin-bottom: 25px">
        <div style="text-align:center">
            <h1 style="color:#ffffff; font-size:2.2rem; font-weight:700; margin-bottom:10px; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
                {title}
            </h1>
            {f'<div style="width:60%; height:2px; background-color:rgba(255,255,255,0.5); margin:10px auto 18px auto;"></div><h3 style="color:#E8F1F2; font-size:1.3rem; font-weight:400; letter-spacing:1px; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">{subtitle}</h3>' if subtitle else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Título e descrição
create_header("Simulação de Pressão em Regimes de Escoamento", "Análise Gráfica e Comparativa")

# Criar duas colunas principais
col_params, col_results = st.columns([1, 3])

# Coluna de parâmetros
with col_params:
    st.markdown("""
    <div style="border-radius:10px;padding:15px">
        <h3 style="text-align:center;">⚙️ Parâmetros do Reservatório</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Grupos de parâmetros organizados
    with st.expander("🧪 Propriedades do Fluido e Reservatório"):
        k = st.number_input('Permeabilidade (k) [mD]', 1.0, 1e4, 100.0, help="Permeabilidade do meio poroso")
        phi = st.number_input('Porosidade (φ) [fração]', 0.01, 1.0, 0.2, help="Porosidade do meio poroso")
        ct = st.number_input('Compressibilidade total (cₜ) [1/psi]', 1e-7, 1e-3, 1e-5, format="%.6f", help="Compressibilidade total do sistema")
        mu = st.number_input('Viscosidade (μ) [cP]', 0.1, 100.0, 1.0, help="Viscosidade do fluido")
        B = st.number_input('Fator de formação (B)', 0.1, 10.0, 1.0, help="Fator de volume de formação")
    
    with st.expander("⛽ Parâmetros de Produção"):
        q = st.number_input('Vazão (q) [STB/dia]', 1.0, 1e4, 100.0, help="Vazão de produção na condição padrão")
        h = st.number_input('Espessura (h) [m]', 0.1, 1e3, 10.0, help="Espessura da formação")
        pe = st.number_input('Pressão de fronteira (pₑ) [psi]', 0.0, 1e4, 3000.0, help="Pressão na fronteira do reservatório")
        s = st.number_input('Fator de película (s)', -10.0, 50.0, 5.0, help="Fator de dano (skin)")
    
    with st.expander("📏 Vetores de Análise"):
        radii = st.multiselect(
            'Raios (r) [m]', 
            [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 300, 500, 1000], 
            default=[0.1, 1, 10, 100, 300],
            help="Raios para análise da pressão"
        )
        times = st.multiselect(
            'Tempos (t) [h]', 
            [0.1, 0.5, 1, 2, 5, 10, 24, 48, 100, 200, 500, 1000], 
            default=[0.1, 1, 10, 100, 1000],
            help="Tempos para análise da pressão"
        )
    
    # Botão de calcular estilizado
    st.markdown("<br>", unsafe_allow_html=True)
    calc_button = st.button('▶️ Calcular', type="primary", use_container_width=True)

# Coluna de resultados
with col_results:
    if calc_button:
        # Mostrar indicador de progresso durante o cálculo
        with st.spinner('Calculando resultados...'):
            # Pequena pausa para mostrar o spinner
            time.sleep(0.5)
            
            # Funções de pressão para os diferentes regimes
            def p_perm(r):
                return pe + (q * mu * B) / (2 * np.pi * k * h) * np.log(max(radii + [r]) / r) + (q * mu * B * s) / (2 * np.pi * k * h)
            
            def p_pseudo(t, r):
                return pe + (q * mu * B) / (2 * np.pi * k * h) * (np.log(4 * k * t / (phi * mu * ct * r**2)) - 0.5772) + (q * mu * B * s) / (2 * np.pi * k * h)
            
            def p_transient(t, r):
                u = (r**2 * phi * mu * ct) / (4 * k * t)
                return pe + (q * mu * B) / (4 * np.pi * k * h) * (-expi(-u)) + (q * mu * B * s) / (2 * np.pi * k * h)

            # Geração de pontos para plot contínuo
            t_plot = np.logspace(-2, 5, 100)  # Tempos de 0.01 a 10000 horas
            r_plot = np.logspace(-2, 5, 100)  # Raios de 0.01 a 10000 metros

            # Definição dos regimes a serem plotados
            regimes = [
                ('Permanente', p_perm, 'r', '#1f77b4'),
                ('Pseudopermanente', p_pseudo, 't', '#ff7f0e'),
                ('Transiente', p_transient, 't', '#2ca02c')
            ]

            # Criar abas para cada regime
            tabs = st.tabs([r[0] for r in regimes])
            
            # Configuração global para os gráficos
            plt.rcParams.update({
                'font.size': 12,
                'axes.labelsize': 14,
                'axes.titlesize': 16,
                'xtick.labelsize': 12,
                'ytick.labelsize': 12,
                'legend.fontsize': 11,
                'figure.figsize': (10, 6),
                'figure.dpi': 100
            })
            
            # Popular cada aba com seus respectivos gráficos
            for tab, (name, func, var, color) in zip(tabs, regimes):
                with tab:
                    st.subheader(f"Regime {name}")
                    
                    # Descrição do regime
                    regime_descriptions = {
                        'Permanente': "O regime permanente representa um sistema em equilíbrio onde a pressão não varia com o tempo em nenhum ponto do reservatório.",
                        'Pseudopermanente': "No regime pseudopermanente, as fronteiras do reservatório já foram sentidas e há um declínio de pressão a taxa constante em todo o reservatório.",
                        'Transiente': "O regime transiente ocorre inicialmente, quando as perturbações de pressão ainda não atingiram as fronteiras do reservatório."
                    }
                    st.info(regime_descriptions[name])
                    
                    # Criar colunas para os gráficos
                    col1, col2 = st.columns(2)

                    # Grafico de Pressão vs Tempo
                    with col1:
                        fig, ax = plt.subplots()
                        
                        for r in sorted(radii):
                            if var == 'r':
                                y = [func(r) for _ in t_plot] if name == 'Permanente' else None
                            else:
                                y = func(t_plot, r)
                            
                            linestyle = '-'
                            ax.semilogx(t_plot, y, label=f"r = {r} m", linestyle=linestyle, linewidth=2)
                        
                        ax.set_xlabel('Tempo (h)')
                        ax.set_ylabel('Pressão (psi)')
                        ax.set_title(f'Distribuição de Pressão vs Tempo - Regime {name}')
                        ax.grid(True, which='both', linestyle='--', alpha=0.6)
                        ax.legend(loc='best', framealpha=0.7)
                        
                        st.pyplot(fig)

                    # Grafico de Pressão vs Distância
                    with col2:
                        fig, ax = plt.subplots()
                        
                        for t in sorted(times):
                            if var == 't':
                                y = func(t, r_plot)
                                linestyle = '-'
                            else:
                                y = [func(r) for r in r_plot]
                                linestyle = '-'
                            
                            ax.semilogx(r_plot, y, label=f"t = {t} h", linestyle=linestyle, linewidth=2)
                        
                        ax.set_xlabel('Distância (m)')
                        ax.set_ylabel('Pressão (psi)')
                        ax.set_title(f'Distribuição de Pressão vs Distância - Regime {name}')
                        ax.grid(True, which='both', linestyle='--', alpha=0.6)
                        ax.legend(loc='best', framealpha=0.7)
                        
                        st.pyplot(fig)
                    
                    # Adicionar explicação das equações usadas
                    st.markdown("#### 📝 Equação Utilizada:")
                    equations = {
                        'Permanente': r'''
                        $$p(r) = p_e + \frac{q \mu B}{2\pi k h} \ln\left(\frac{r_e}{r}\right) + \frac{q \mu B s}{2\pi k h}$$
                        
                        Onde:
                        - $p(r)$ é a pressão a uma distância $r$ do poço
                        - $p_e$ é a pressão na fronteira do reservatório
                        - $r_e$ é o raio de drenagem
                        - $s$ é o fator de película (skin)
                        ''',
                        
                        'Pseudopermanente': r'''
                        $$p(r,t) = p_e + \frac{q \mu B}{2\pi k h} \left[\ln\left(\frac{4kt}{\phi \mu c_t r^2}\right) - 0.5772\right] + \frac{q \mu B s}{2\pi k h}$$
                        
                        Onde:
                        - $\phi$ é a porosidade
                        - $c_t$ é a compressibilidade total
                        - $t$ é o tempo
                        ''',
                        
                        'Transiente': r'''
                        $$p(r,t) = p_e + \frac{q \mu B}{4\pi k h} (-E_i(-u)) + \frac{q \mu B s}{2\pi k h}$$
                        
                        Onde:
                        - $u = \frac{r^2 \phi \mu c_t}{4kt}$
                        - $E_i(-u)$ é a função exponencial integral
                        '''
                    }
                    st.markdown(equations[name])

        # Mostrar mensagem de sucesso
        st.success("Simulação concluída com sucesso!")
        
    else:
        # Imagem ou mensagem para quando os gráficos não estão sendo exibidos
        st.info('Ajuste os parâmetros conforme necessário e clique em **Calcular** para visualizar os resultados da simulação.')
        
        # Adicionar imagem ilustrativa centralizada
        st.markdown("""
        <div style="display:flex;justify-content:center;margin:40px 0px">
            <img src="https://via.placeholder.com/600x350?text=Simulação+de+Regimes+de+Fluxo" width="600">
        </div>
        """, unsafe_allow_html=True)

# Adicionar informações sobre os regimes na parte inferior da página
with st.expander("ℹ️ Informações sobre os Regimes de Fluxo"):
    st.markdown("""
    ### Conceitos Fundamentais dos Regimes de Fluxo
    
    Os regimes de fluxo em um reservatório de petróleo são determinados pela Equação da Difusividade Hidráulica:
    
    $$\\frac{1}{r}\\frac{\\partial}{\\partial r}\\left(r\\frac{\\partial p}{\\partial r}\\right) = \\frac{\\phi\\mu c_t}{k}\\frac{\\partial p}{\\partial t}$$
    
    Esta equação diferencial possui diferentes soluções analíticas para cada regime:
    
    1. **Regime Transiente**: Ocorre no início da produção, quando as perturbações de pressão ainda não atingiram as fronteiras do reservatório.
    
    2. **Regime Pseudopermanente**: Acontece quando todas as fronteiras do reservatório foram atingidas, e a queda de pressão torna-se uniforme em todo o reservatório.
    
    3. **Regime Permanente**: Representa uma situação de equilíbrio, onde a pressão em qualquer ponto do reservatório não varia com o tempo. Na prática, esse regime é aproximado quando existe um forte influxo de água.
    """)

# Rodapé
st.markdown("""
<div style="text-align:center;margin-top:30px;padding-top:20px;border-top:1px solid #ddd;color:#666">
    <p>© 2025 Nuno Henrique Albuquerque Pires - Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)

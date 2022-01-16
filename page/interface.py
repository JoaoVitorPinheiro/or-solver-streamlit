import streamlit as st

def set_streamlit():
    st.set_page_config(
    page_title = "solvedOR",
    page_icon = "📉",)

    # Checar esse html 
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    hide_streamlit_style = """
    <style>
    .css-1y0tads {padding-top: 0rem;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html = True)
    
    return "initializing..."

def show_results():
    pass
    
def initialize_info():
    st.title("Ferramenta de Pesquisa Operacional")
    st.sidebar.subheader("😸 Exemplos")

    exemplo = st.sidebar.selectbox("Veja um exemplo modelado:",("1) Modelo Básico", "2) Problema de Transporte",
                                            "3) Programação Binária", "4) Designação",
                                            "5) Postes nas ruas", "6) Investimentos",
                                            "7) Exemplo de PL"))
                                        
    with st.expander("😺 Instruções de Uso"):
        st.markdown("""
        - 🐈 Use espaços entre os sinais de operação e as variáveis;
        - 🐈‍⬛ Os coeficientes das variáveis devem estar "colados" nas variáveis (vide exemplos);
        - 🐅 Não existe ordem certa para definir o modelo, contanto que tudo seja definido;
        - 🐆 Variáveis devem ser mantidas no lado esquerdo;
        - 🦖 Não usar frações;
        - 🦕 Formas decimais são representadas com " . " (ponto) ao invés de " , " vírgula.""")

    with st.expander("😺 Sintaxe dos Operadores"):
        st.markdown("""
                    ## Tipo de Problema 
            #### defina o problema com esse padrão
                problema: linear
            #### ou de forma abreviada
                p: lin
            #### para programação inteira, utilize:
                problema: inteiro
            #### ou de forma abreviada
                p: int
            deve ser declarado apenas uma vez 
            ## Função Objetivo:
            #### definindo o objetivo como maximizar: 
                max: 	
            #### para minimizar, utilize:
                min: 
            #### adicione os termos como no exemplo abaixo:
                2x1 + 3x2 + 4x3 + 5x4
            #### ao final, deve ser algo no formato: 
                min: 2x1 + 3x2 + 4x3 + 5x4
            deve ser declarada apenas uma função objetivo
            ## Restrições:
            #### definindo a restrição: 
                restricao: x1 + 2x2 <= 20 	
            #### de forma abreviada, utilize:
                r: x1 + 2x2 <= 20 
            #### outros sinais :
                r: x1 + x2 >= 1
                r: x1 + 2x2 = 10 """,
    unsafe_allow_html = True)

        st.info("Na aba lateral há exemplos de modelos de programação que apresentam algumas possibilidades e recursos. ")
        st.info("Clique em *Resolver* para solucionar seu modelo")
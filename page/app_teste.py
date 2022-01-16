from ortools.linear_solver import pywraplp
import streamlit as st
import pandas as pd
from typing import List
from pathlib import Path
from IPython.display import display, Math, Latex

from interface import set_streamlit
from examples import gerar_exemplos
from models import processar_input, solve_problem

def main():
    
    st.title("Ferramenta de Pesquisa Operacional")
                                        
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
                r: x1 + 2x2 = 10
            ## Arredondamento:
            #### definindo o número de casas decimais para arredondar os resultados: 
                arred: 3
                arredondamento: 1
                se não for declarado arredondamento, o padrão é 5
                """,
    unsafe_allow_html = True)

        st.info("Na aba lateral há exemplos de modelos de programação que apresentam algumas possibilidades e recursos. ")
        st.info("Clique em *Resolver* para solucionar seu modelo")
    
    #st.sidebar.subheader("😸 Exemplos")
    
    with st.expander("😺 Lousa de Exemplos"):
        
        exemplo = st.selectbox("Veja um exemplo modelado:",
                                   ("1) Modelo Básico",
                                    "2) Problema de Transporte",
                                    "3) Programação Binária",
                                    "4) Designação",
                                    "5) Postes nas ruas",
                                    "6) Investimentos",
                                    "7) Exemplo de PL",
                                    "8) Rota Turística"))
        
        exemplo_escolhido = st.text_area('Navegue por exemplos de problemas modelados na barra ao lado!',
                                value = gerar_exemplos(exemplo),
                                height = 500)
    
    texto_input = st.text_area('Desenvolva a modelagem no quadro abaixo:',
                               value = gerar_exemplos("1) Modelo Básico"),
                               height = 500)
    
    df, coef_objetivo, objetivo, metodo, arredondamento  = processar_input(texto_input)

    if st.button("Resolver"): 
        solve_problem(df,
                      coef_objetivo,
                      metodo, objetivo,
                      arredondamento)
    
    if metodo == 'Programação Linear':
        st.subheader("Programação Linear:")
        st.write(f'(PL): engloba problemas de otimização nos quais a função objetivo e as restrições são todas lineares.')
     
    elif metodo == 'Programação Inteira':
        st.subheader("Programação Inteira:")                   # REVISAR
        st.write(f'(PI): engloba problemas de otimização nos quais a função objetivo e as restrições são parcialmente ou totalmente pertencentes ao conjunto dos números inteiros.')

    a_series = pd.Series(coef_objetivo, index = df.columns[:-2])
    
    df_obj = pd.DataFrame(columns = df.columns[:-2])
    df_obj = df_obj.append(a_series, ignore_index=True)

    st.subheader("Objetivo: ")
    st.write((objetivo+"imizar").lower())

    st.subheader("Função Objetivo: ")
    st.dataframe(df_obj)

    st.subheader("Restrições: ")
    st.dataframe(df)

    latex_exp = (objetivo+"imizar Z =").capitalize() 
    lista = [str(item) for item in df_obj.columns]
    #st.write(lista)
    latex_exp = latex_exp + "+".join(lista)
    #st.latex(latex_exp)
    
    st.write("🐯 [Contato para sugestões e dúvidas](https://www.linkedin.com/in/jvpro/)")    
    
if __name__ == "__main__":
    set_streamlit()
    main()


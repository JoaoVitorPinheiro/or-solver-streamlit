import sys, os
from ortools.linear_solver import pywraplp
import numpy as np
from sympy import *
import streamlit as st
import re
import pandas as pd
from typing import List
from pathlib import Path
from IPython.display import display, Math, Latex

# https://github.com/benalexkeen/Introduction-to-linear-programming
# https://aniketjha1304.medium.com/operations-research-with-python-programming-3e9474f12065 
# http://www.universalteacherpublications.com/univ/ebooks/or/Ch1/techniq.htm
# https://towardsdatascience.com/optimization-in-transportation-problem-f8137044b371

# 我听见 我忘记; 我看见 我记住; 我做 我了解 

def set_streamlit():
    st.set_page_config(
    page_title = "solvedOR",
    page_icon = "📉",
    layout = "wide",)

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

def gerar_exemplos(exemplo_escolhido):

    exemplo1 = """problema: linear

max: 8x1 + 10x2

restricao: 0.5x1 + 0.5x2 <= 150
restricao: 0.6x1 + 0.4x2 <= 145

restricao:  x1 >= 30                                            restricao: x1 <= 150
restricao:  x2 >= 40                                            restricao: x2 <= 200 """

    exemplo2 = """problema: inteiro

min: x111 + 2x121 + 3x131 + 2x141 + 2x112 + 4x122 + 6x132 + 4x142 + 2x211 + 4x221 + 1x231 + 2x241 + 4x212 + 8x222 + 2x232 + 4x242 + 1x311 + 3x321 + 5x331 + 3x341

r: x111 + x121 + x131 + x141 <= 150
r: x112 + x122 + x132 + x142 <= 90 
r: x211 + x221 + x231 + x241 <= 200
r: x212 + x222 + x232 + x242 <= 120
r: x311 + x321 + x331 + x341 <= 250
r: x111 + x112 + x211 + x212 + x311 = 150
r: x121 + x122 + x221 + x222 + x321 = 150
r: x131 + x132 + x231 + x232 + x331 = 400
r: x141 + x142 + x241 + x242 + x341 = 100 """
    
    exemplo3 = """p: inteiro

max: 9x1 + 5x2 + 6x3 + 4x4

r: 6x1 + 3x2 + 5x3 + 2x4 <= 10
r: x3 + x4 <= 1 

#Restrições que envolvam variáveis de decisão do lado direito do sinal da equação/inequação devem ser reescritas como:

r: x1 - x3 <= 1                                        r: x2 - x4 <= 1        
 (só para manter as variáveis na esquerda)

 (checar tabela abaixo para conferir o registro da restrição)

#Exemplo de como criar variáveis binárias
restricao: x1 <= 1                                                restricao: x2 <= 1 
restricao: x3 <= 1                                                restricao: x4 <= 1   """

    exemplo4 = """problema: inteiro

MIN:  50x11 + 50x12 + 0x13 + 20x14
        + 70x21 + 40x22 + 20x23 + 30x24                 
        + 90x31 + 30x32 + 50x33 +  0x34                  
        + 70x41 + 20x42 + 60x43 + 70x44                
Simulando uma matriz de designação de tarefas para o problema
problema, função objetivo e restrições podem ser declaradas em qualquer lugar, contanto que as regras de uso sejam obedecidas!        

restricao: x11 + x12 + x14 = 1
restricao: x21 + x22 + x23 + x24 = 1
restricao: x31 + x32 + x33 = 1
restricao: x41 + x42 + x43 + x44 = 1

restricao: x11 + x21 + x31 + x41 = 1
restricao: x12 + x22 + x32 + x42 = 1
restricao: x13 + x23 + x33 + x43 = 1
restricao: x14 + x24 + x34 + x44 = 1 """
 
    exemplo5 = """problema: inteiro

min: x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 

restricao:  x1 + x2 >= 1          RUA A
restricao:  x2 + x3 >= 1          RUA B
restricao:  x4 + x5 >= 1          RUA C
restricao:  x7 + x8 >= 1          RUA D
restricao:  x6 + x7 >= 1          RUA E
restricao:  x6 + x2 >= 1          RUA F
restricao:  x6 + x1 >= 1          RUA G
restricao:  x4 + x7 >= 1          RUA H
restricao:  x4 + x2 >= 1          RUA I
restricao:  x5 + x8 >= 1          RUA J
restricao:  x3 + x5 >= 1          RUA K

restricao:  x1 <= 1                              restricao:  x2 <= 1                                           
restricao:  x3 <= 1                              restricao:  x4 <= 1
restricao:  x5 <= 1                              restricao:  x6 <= 1   
restricao:  x7 <= 1                              restricao:  x8 <= 1 """

    exemplo6 = """problema: inteiro

max: 20x1 + 15x2 + 34x3 + 17x4 + 56x5 + 76x6 + 29x7

restricao: 12x1 + 54x2 + 65x3 + 38x4 + 52x5 + 98x6 + 15x7 <= 200             ANO 0
restricao: 34x1 + 94x2 + 28x3 + 0x4 + 21x5 + 73x6 + 48x7 <= 250             ANO 1 
restricao: 12x1 + 67x2 + 49x3 + 8x4 + 42x5 + 25x6 + 53x7 <= 150            ANO 2

restricao:  x1 <= 1
restricao:  x2 <= 1                                           restricao:  x3 <= 1 
restricao:  x4 <= 1                                           restricao:  x5 <= 1 
restricao:  x6 <= 1                                           restricao:  x7 <= 1 
restricao:  x7 <= 1 """

    exemplo7 = """problema: linear

min: 2x1 + 1x2

restricao: x1 - x2 <= 1
restricao: 3x1 + 2x2 <= 12
restricao: 2x1 + 3x2 >= 3
restricao: -2x1 + 3x2 <= 9"""



    dict_exemplos = {"1) Modelo Básico":exemplo1,
                    "2) Problema de Transporte":exemplo2,
                    "3) Programação Binária":exemplo3,
                    "4) Designação":exemplo4,
                    "5) Postes nas ruas":exemplo5,
                    "6) Investimentos":exemplo6,
                    "7) Exemplo de PL":exemplo7}

    return dict_exemplos[exemplo_escolhido]

def processar_input(texto):

    regra = r"(?:(?:restricao:|r:)(?:(?<!\+|\-|\.)[\+\-\s]+(?:(?:\d+\.\d+)|(?:\d{0,9}))x\d{1,6}[\+\-\s])+(?:[=><]{1,2}[\-\+\s]+(?:(?:\d+\.\d+)|(?:\d{0,9}))+(?!\|;\w|\d)))|(?:(?:min:|max:)(?:(?<!\+|\-)[\+\-\s]+(?:(?:\d+\.\d+)|(?:\d{0,9}))x\d{1,6}[\+\-\s])+(?!\|;\w|\d))|(?:(?:problema:|p:)(?:(?<!\+|\-)[\+\-\s](?:inteiro|linear|int|lin)[\+\-\s]?)+(?!\|;\w|\d))"

    doc = texto

    padrao = re.compile(regra, flags = re.IGNORECASE)

    coletor = [re.sub(r'[^0-9+-xzr. ]', '', item).lower() for item in padrao.findall(doc)]

    restricoes = [item for item in coletor if (('restricao:' in item) or ('r:' in item))]

    func_obj = [item for item in coletor if (('min:' in item) or ('max:' in item))]

    for item in coletor:
        if 'max' in item:
            objetivo = 'max'

        elif 'min' in item:
            objetivo = 'min'

        if (('inteiro' in item) or ('int' in item)):
            metodo = 'Programação Inteira'

        elif (('linear' in item) or ('lin' in item)):
            metodo = 'Programação Linear'

    coletor = set([item[item.find(':')+1:].strip() for item in coletor if len(set(item)) != 1])
    restricoes = [item[item.find(':')+1:].strip() for item in restricoes]
    func_obj = [item[item.find(':')+1:].strip() for item in func_obj]

    #print("\nObjetivo:")
    #print(objetivo.upper()+"imizar".upper())

    #print("\nFunção Objetivo:")
    #print("z = ",func_obj[0])

    #print("\nRestrições:")
    #[print(item) for item in restricoes]

    variaveis = set([item for item in func_obj[0].split() if "x" in item])

    #print(variaveis)

    for restricao in restricoes:
        variaveis.update([item for item in restricao.split() if "x" in item])

    var = []
    for item in list(variaveis):
        if item[0] == 'x':
            number = 1
            var.append(item)
            
        else:
            number = item[:item.find("x")]
            var.append(item[item.find("x"):])

    var = sorted(list(set(var)))
    #print(var)

    df = pd.DataFrame(columns = var)

    termos_restricao = np.array([item.split()[-1] for item in restricoes])
    sinal = [item.split()[-2] for item in restricoes]

    for item in restricoes:

        lista = [i.replace(" ", "") for i in item.split()]

    restr = []
    for item in restricoes:
            
            lista = [i.replace(" ", "") for i in item.split()]
            
            for i in range(len(lista)):

                if lista[i] == '-':
                    lista[i+1] = "-"+str(lista[i+1])
                    lista[i] = ' '
                    
                    i = i + 1

            item = [i for i in lista if 'x' in i]
            restr.append(item)

    lista = [i.replace(" ", "") for i in func_obj[0].split()]

    obj = []
    for i in range(len(lista)):

        if lista[i] == '-':
            lista[i+1] = "-"+str(lista[i+1])
            lista[i] = ' '
                    
            i = i + 1

    obj = [i for i in lista if 'x' in i]
    #print(obj)

    coef_obj = []

    for variavel in var:
        number = 0
        for item in obj:
            if variavel in item:
                    
                if item[0] == 'x':
                    number = 1

                else:
                    number = (item[:item.find("x")])                    

                    if number == "-":
                        number = -1

        coef_obj.append(number)
        
    coef_obj = np.array(coef_obj)

    for variavel in var:

        walker = []
        
        for item in restr:
            
            number = 0
            
            for termo in item:
                
                if variavel in termo:
                    
                    if termo[0] == 'x':
                        number = 1

                    else:
                        number = (termo[:termo.find("x")])
                        
                        if number == "-":
                            number = -1
                    
                    #print(number)
                    
            walker.append(number)
                
        #print(walker)
        
        df[variavel] = np.array(walker)

    df['sinal'] = sinal 
    df['restricao'] = np.array(termos_restricao)
    #print(coef_obj)
    #print(objetivo)
    #print(df)

    return df, coef_obj, objetivo, metodo 

def create_data_model(df, coef_objetivo):
    """Salva os dados das entradas em estruturas para processamento"""

    data = {}

    data['constraint_coeffs'] = np.array(df[df.columns[:-2]], dtype=float)
    data['bounds'] = np.array(df['restricao'],dtype=float)
    data['inequacao'] = df['sinal']
    data['obj_coeffs'] = np.array(coef_objetivo,dtype=float)
    data['num_vars'] = len(df.columns[:-2])
    data['num_constraints'] = len(data['constraint_coeffs'])
    
    #st.write("Coeficientes das Restrições:",data['constraint_coeffs'])
    #st.write("Termos do Lado Direito:",data['bounds'])
    #st.write("Coeficientes da Função Objetivo:", data['obj_coeffs'])
    #st.write("Número de Variáveis:",data['num_vars'])
    #st.write("Número de Restriçoes:",data['num_constraints'])

    return data

def solve_problem(df, coef_objetivo, metodo, objetivo, decimais):

    data = create_data_model(df, coef_objetivo)

    x = {}

    if metodo == 'Programação Linear':
        
        super_solver = pywraplp.Solver.CreateSolver('GLOP')

        for j in range(data['num_vars']):
            x[j] = super_solver.NumVar(0.0, super_solver.infinity(), 'x%i' % (j+1))

    elif metodo == 'Programação Inteira':

        super_solver = pywraplp.Solver.CreateSolver('SCIP')

        for j in range(data['num_vars']):
            x[j] = super_solver.IntVar(0, super_solver.infinity(), 'x%i' % (j+1))

    st.write('Número de Variáveis =', super_solver.NumVariables())
    
    # Restrições de limite de valor das restrições
    for i in range(data['num_constraints']):
       
        if data['inequacao'][i] == ">=":
            limite_inferior = data['bounds'][i]
            limite_superior = super_solver.infinity()
            
        elif data['inequacao'][i] == "<=":
            limite_inferior = -super_solver.infinity()
            limite_superior = data['bounds'][i]

        else: # data['inequacao'][i] == "=="
            limite_inferior = data['bounds'][i]
            limite_superior = data['bounds'][i]

        constraint = super_solver.RowConstraint(limite_inferior, limite_superior, '')

        for j in range(data['num_vars']):
            constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j])

    st.write('Número de Restrições =', super_solver.NumConstraints())

    objective = super_solver.Objective()

    for j in range(data['num_vars']):
        objective.SetCoefficient(x[j], data['obj_coeffs'][j])

    if objetivo == 'max':    
        objective.SetMaximization()

    else:   
        objective.SetMinimization()

    status = super_solver.Solve()
    #st.write(status)
    if status == pywraplp.Solver.OPTIMAL:

        st.balloons()
        st.success('😻 Solução ótima encontrada!!! 😻')
        
        st.write('Valor Otimizado da Função Objetivo =', 
                round(super_solver.Objective().Value(),decimais))
        
        variaveis = np.array(df.columns[:-2])

        for j in range(data['num_vars']):
            st.write(variaveis[j], ' = ', 
                    round(x[j].solution_value(), decimais))
            
        st.write('Problema resolvido em %f ms' % super_solver.wall_time())
        st.write('Problema resolvido em %d iterações' % super_solver.iterations())
        st.write('Problema resolvido em %d nó(s) de branch-and-bound' % super_solver.nodes())

    elif status == pywraplp.Solver.FEASIBLE:
        st.warning('😸 Solução viável encontrada 😸')

        st.write('Valor da Função Objetivo =', 
                round(super_solver.Objective().Value(),decimais))
        
        variaveis = np.array(df.columns[:-2])

        for j in range(data['num_vars']):
            st.write(variaveis[j], ' = ', 
                    round(x[j].solution_value(), decimais))
            
        st.write('Problema resolvido em %f ms' % super_solver.wall_time())
        st.write('Problema resolvido em %d iterações' % super_solver.iterations())
        st.write('Problema resolvido em %d nó(s) de branch-and-bound' % super_solver.nodes())
    
    elif status == pywraplp.Solver.INFEASIBLE:
        st.warning('😿 Não há solução viável pra essa bronca 😿')
    
    elif status == pywraplp.Solver.UNBOUNDED:
        st.warning('🙀 O modelo é um problema ilimitado!!! 🙀')

    elif status == pywraplp.Solver.ABNORMAL:
        st.warning('😿 Algum erro desconhecido e não conseguimos achar uma solução 😿')

    elif status == pywraplp.Solver.MODEL_INVALID:
        st.warning('😾 Modelo Inválido 😾')

    else:
        st.warning('😿 Não há solução pra essa bronca😿')

def main():

    st.title("🙀 Solver de Programação Matemática 🙀")
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

    st.sidebar.subheader("😸 Arredondamento:")
    decimais = int(st.sidebar.select_slider('Selecione a precisão padrão:',
            options = ['1', '2', '3', '4', '5', '6','7','8','9','10'],
            value = '5'))

    st.sidebar.write("🐯 [Contato para sugestões e dúvidas](https://www.linkedin.com/in/jvpro/)")

    texto_input = st.text_area('Preencha no quadro abaixo o modelo com os termos e sinais SEPARADOS POR ESPAÇOS:',value = gerar_exemplos(exemplo), height = 500)

    df, coef_objetivo, objetivo, metodo  = processar_input(texto_input)

    if st.button("Resolver"): 
        solve_problem(df, coef_objetivo, metodo, objetivo, decimais)
    
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
    st.write(lista)
    latex_exp = latex_exp + "+".join(lista)
    st.latex(latex_exp)
        
if __name__ == "__main__":
    set_streamlit()
    main()

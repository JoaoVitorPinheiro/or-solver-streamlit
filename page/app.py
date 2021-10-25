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

def set_streamlit():
    st.set_page_config(
    page_title = "Pesquisa Operacional",
    page_icon = "📉",
    layout = "wide",)

    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    return "initializing..."

def gerar_exemplos(exemplo_escolhido):

    exemplo1 = """Modelo Simples

problema: linear

objetivo: maximizar

funcao: 8x1 + 10x2

restricao: 0.5x1 + 0.5x2 <= 150
restricao: 0.6x1 + 0.4x2 <= 145

restricao:  x1 >= 30                                            restricao: x1 <= 150
restricao:  x2 >= 40                                            restricao: x2 <= 200 """

    exemplo2 = """Transporte

problema: inteiro

obj: minimizar 

funcao: x111 + 2x121 + 3x131 + 2x141 + 2x112 + 4x122 + 6x132 + 4x142 + 2x211 + 4x221 + 1x231 + 2x241 + 4x212 + 8x222 + 2x232 + 4x242 + 1x311 + 3x321 + 5x331 + 3x341

r: x111 + x121 + x131 + x141 <= 150
r: x112 + x122 + x132 + x142 <= 90 
r: x211 + x221 + x231 + x241 <= 200
r: x212 + x222 + x232 + x242 <= 120
r: x311 + x321 + x331 + x341 <= 250
r: x111 + x112 + x211 + x212 + x311 = 150
r: x121 + x122 + x221 + x222 + x321 = 150
r: x131 + x132 + x231 + x232 + x331 = 400
r: x141 + x142 + x241 + x242 + x341 = 100 """
    
    exemplo3 = """Programação Binária

p: inteiro

o: maximizar

f: 9x1 + 5x2 + 6x3 + 4x4
r: 6x1 + 3x2 + 5x3 + 2x4 <= 10
r: x3 + x4 <= 1 

#Restrições que envolvam variáveis de decisão do lado direito do sinal da equação/inequação do tipo 
r: x2 <= x4 + 1 devem ser reescritas como: (só para manter as variáveis na esquerda)
r: x1 - x3 <= 1                                        r: x2 - x4 <= 1        
 (checar tabela abaixo para conferir o registro da restrição)

#Exemplo de como criar variáveis binárias
restricao: x1 <= 1                                                restricao: x2 <= 1 
restricao: x3 <= 1                                                restricao: x4 <= 1  """

    exemplo4 = """Designação

problema: inteiro

funcao:  50x11 + 50x12 + 0x13 + 20x14
        + 70x21 + 40x22 + 20x23 + 30x24                 
        + 90x31 + 30x32 + 50x33 +  0x34                  
        + 70x41 + 20x42 + 60x43 + 70x44                
Simulando uma matriz de designação de tarefas para o problema
problema, objetivo, função objetivo e restrições podem ser declaradas em qualquer lugar, contanto que as regras de uso sejam obedecidas!        
objetivo: minimizar

restricao: x11 + x12 + x14 = 1
restricao: x21 + x22 + x23 + x24 = 1
restricao: x31 + x32 + x33 = 1
restricao: x41 + x42 + x43 + x44 = 1

restricao: x11 + x21 + x31 + x41 = 1
restricao: x12 + x22 + x32 + x42 = 1
restricao: x13 + x23 + x33 + x43 = 1
restricao: x14 + x24 + x34 + x44 = 1 """
    # EXEMPLO COM ERRO DE FORMULAÇÃO
    exemplo5 = """Terceirizar ou não?

problema: inteiro

objetivo: minimizar

funcao: 36x11 + 44x12 + 69x13 + 44x21 + 56x22 + 72x23

restricao: 1.1x11 + 1.1x12 + 1.2x13 <= 4000
restricao: 1.1x11 + 1x12 + 1.1x13 <= 3500
restricao: x11 + x21 = 750
restricao: x12 + x22 = 2000
restricao: x13 + x23 = 1100

Para garantir que as variáveis sejam binárias (o limite inferior já é 0 para problemas de MAX)
As restrições podem ser colocadas na mesma linha, contanto que as regras de uso sejam respeitadas
restricao: x11 <= 1                     restricao: x12 <= 1                     restricao: x13 <= 1
restricao: x21 <= 1                     restricao: x22 <= 1                     restricao: x23 <= 1 """

    dict_exemplos = {"1) Modelo Básico":exemplo1,
                    "2) Problema de Transporte":exemplo2,
                    "3) Programação Binária":exemplo3,
                    "4) Designação":exemplo4,
                    "5) Terceirizar ou não?":exemplo5}

    return dict_exemplos[exemplo_escolhido]

def processar_input(texto):

    regra = r'(?:(?:restricao:|r:)(?:(?<!\+|\-|\.)[\+\-\s]+(?:(?:\d+\.\d+)|(?:\d{0,9}))x\d{1,4}[\+\-\s])+(?:[=><]{1,2}[\-\+\s]+\d+(?!\|;\w|\d)))|(?:(?:funcao:|f:)(?:(?<!\+|\-)[\+\-\s]+(?:(?:\d+\.\d+)|(?:\d{0,9}))x\d{1,3}[\+\-\s])+(?!\|;\w|\d))|(?:(?:objetivo:|obj:|o:)(?:(?<!\+|\-)[\+\-\s](?:maximizar|minimizar|max|min)[\+\-\s])+(?!\|;\w|\d))|(?:(?:problema:|p:)(?:(?<!\+|\-)[\+\-\s](?:inteiro|linear|int|lin)[\+\-\s])+(?!\|;\w|\d))'

    doc = texto

    padrao = re.compile(regra, flags = re.IGNORECASE)

    coletor = [re.sub(r'[^0-9+-xzr. ]', '', item).lower() for item in padrao.findall(doc)]

    restricoes = [item for item in coletor if (('restricao:' in item) or ('r:' in item))]

    func_obj = [item for item in coletor if (('funcao:' in item) or ('f:' in item))]

    for item in coletor:
        if (('maximizar' in item) or ('max' in item)):
            objetivo = 'max'

        elif (('minimizar' in item) or ('min' in item)):
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

def solve_problem(df, coef_objetivo, metodo, objetivo):

    data = create_data_model(df, coef_objetivo)

    x = {}

    if metodo == 'Programação Linear':
        
        super_solver = pywraplp.Solver.CreateSolver('GLOP')

        for j in range(data['num_vars']):
            x[j] = super_solver.NumVar(0, super_solver.infinity(), 'x%i' % (j+1))

    elif metodo == 'Programação Inteira':

        super_solver = pywraplp.Solver.CreateSolver('SCIP')

        for j in range(data['num_vars']):
            x[j] = super_solver.IntVar(0, super_solver.infinity(), 'x%i' % (j+1))

    st.write('Número de Variáveis =', super_solver.NumVariables())

    for i in range(data['num_constraints']):
       
        if data['inequacao'][i] == ">=":
            limite_inferior = data['bounds'][i]
            limite_superior = super_solver.infinity()
            
        elif data['inequacao'][i] == "<=":
            limite_inferior = 0
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

    if status == pywraplp.Solver.OPTIMAL:

        st.markdown('<p class="big-font">😻 Solução ótima encontrada!!! 😻</p>', unsafe_allow_html=True)
        st.write('Valor Otimizado da Função Objetivo =', super_solver.Objective().Value())
        
        variaveis = np.array(df.columns[:-2])

        for j in range(data['num_vars']):
            st.write(variaveis[j], ' = ', x[j].solution_value())

        st.write('Problema resolvido em %f ms' % super_solver.wall_time())
        st.write('Problema resolvido em %d iterações' % super_solver.iterations())
        st.write('Problema resolvido em %d branch-and-bound nodes' % super_solver.nodes())

    else:
        st.markdown('<p class="big-font">😿 Não achamos solução 😿</p>', unsafe_allow_html=True)

def main():

    st.title("😾 Morte ao Solver do Excel 😾")
    st.sidebar.subheader("😸 Exemplos")

    exemplo = st.sidebar.selectbox("Selecione:",("1) Modelo Básico","2) Problema de Transporte","3) Programação Binária","4) Designação","5) Terceirizar ou não?"))

    st.sidebar.subheader("""😺 Regras de Uso
    🐈 Use espaços entre os sinais de operação e as variáveis;
    🐈‍⬛ Os coeficientes das variáveis devem estar "colados" nas variáveis (vide exemplos);
    🐅 Não existe ordem certa para definir o modelo, contanto que tudo seja definido;
    🐆 Variáveis devem ser mantidas no lado esquerdo;
    🦖 Não usar frações;
    🦕 Formas decimais são representadas com '.' (ponto) ao invés de vírgula.""")

    st.sidebar.write("🐯 白玉龙的项目")

    texto_input = st.text_area('Preencha o modelo com os termos e sinais SEPARADOS POR ESPAÇOS',value = gerar_exemplos(exemplo), height = 500)

    df, coef_objetivo, objetivo, metodo  = processar_input(texto_input)

    if metodo == 'Programação Linear':
        
        st.subheader("Programação Linear:")
        st.write(f'(PL): engloba problemas de otimização nos quais a função objetivo e as restrições são todas lineares.')
     
    elif metodo == 'Programação Inteira':
        # REVISAR
        st.subheader("Programação Inteira:")
        st.write(f'(PI): engloba problemas de otimização nos quais a função objetivo e as restrições são parcialmente ou totalmente pertencentes ao conjunto dos números inteiros.')

    a_series = pd.Series(coef_objetivo, index=df.columns[:-2])
    
    df_obj = pd.DataFrame(columns=df.columns[:-2])
    df_obj = df_obj.append(a_series, ignore_index=True)

    st.subheader("Objetivo: ")
    st.write((objetivo+"imizar").upper())

    st.subheader("Função Objetivo: ")
    st.dataframe(df_obj)

    st.subheader("Restrições: ")
    st.dataframe(df)
    
    st.markdown('<p class="big-font">😺 PODE 😼 MANDAR 😾 BALA !!!</p>', unsafe_allow_html=True)
    #data = create_data_model(df, funcao_objetivo)

    #for i,row in enumerate(df['restricao']):

    #    #x, y = symbols('x y')
    #    expression = row
    #    #Use sympy.sympify() method
    #    math_exp = sympify(expression)
    #    st.write(str(i+1),"° restrição: ",math_exp)
    #    #st.write(df['inequacao'].iloc[i])
    #    math_exp = Eq(math_exp, 0)

    if st.button("Resolver"): 

        solve_problem(df, coef_objetivo, metodo, objetivo)
        
    return 0
    
if __name__ == "__main__":
    set_streamlit()
    main()

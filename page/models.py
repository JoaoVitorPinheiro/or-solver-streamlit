import ortools
import numpy as np
import pandas as pd
import streamlit as st
import re
from ortools.linear_solver import pywraplp

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

def processar_input(texto):
    
    regra = r"(?:(?:restricao:|r:)(?:(?<!\+|\-|\.)[\+\-\s]+(?:(?:\d+\.\d+)|(?:\d{0,9}))x\d{1,5}[\+\-\s])+(?:[=><]{1,2}[\-\+\s]+(?:(?:\d+\.\d+)|(?:\d{0,9}))+(?!\|;\w|\d)))|(?:(?:min:|max:)(?:(?<!\+|\-)[\+\-\s]+(?:(?:\d+\.\d+)|(?:\d{0,9}))x\d{1,5}[\+\-\s])+(?!\|;\w|\d))|(?:(?:problema:|p:)(?:(?<!\+|\-)[\+\-\s]+(?:inteiro|linear|int|lin)[\+\-\s]?)+(?!\|;\w|\d))|(?:(?:arredondamento:|arred:)(?:(?<!\+|\-|\.)(?:[\-\+\s]+(?:\d{1,2})(?!\|;\w|\d))))"

    doc = texto

    padrao = re.compile(regra, flags = re.IGNORECASE)

    coletor = [re.sub(r'[^0-9+-xzr. ]', '', item).lower() for item in padrao.findall(doc)]

    restricoes = [item for item in coletor if (('restricao:' in item) or ('r:' in item))]

    func_obj = [item for item in coletor if (('min:' in item) or ('max:' in item))]
    
    arredondamento = [item for item in coletor if  (('arredondamento:' in item) or ('arred:' in item))]

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
    arredondamento = [item[item.find(':')+1:].strip() for item in arredondamento]
    
    try:
        arredondamento = arredondamento[0]
    except:
        arredondamento = 5
        
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
    arredondamento = int(arredondamento)
    #print(coef_obj)
    #print(objetivo)
    #print(df)

    return df, coef_obj, objetivo, metodo, arredondamento 

def solve_problem(df, coef_objetivo, metodo, objetivo, arredondamento):
    
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
                round(super_solver.Objective().Value(),arredondamento))
        
        variaveis = np.array(df.columns[:-2])

        for j in range(data['num_vars']):
            st.write(variaveis[j], ' = ', 
                    round(x[j].solution_value(), arredondamento))
            
        st.write('Problema resolvido em %f ms' % super_solver.wall_time())
        st.write('Problema resolvido em %d iterações' % super_solver.iterations())
        st.write('Problema resolvido em %d nó(s) de branch-and-bound' % super_solver.nodes())

    elif status == pywraplp.Solver.FEASIBLE:
        st.warning('😸 Solução viável encontrada 😸')

        st.write('Valor da Função Objetivo =', 
                round(super_solver.Objective().Value(),arredondamento))
        
        variaveis = np.array(df.columns[:-2])

        for j in range(data['num_vars']):
            st.write(variaveis[j], ' = ', 
                    round(x[j].solution_value(), arredondamento))
            
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


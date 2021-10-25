import ortools
import streamlit as st
from ortools.linear_solver import pywraplp
from sympy import *

def linear_solver(num_var, dataset):

    #Inicializa um solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    #title = st.text_input('Número de variáveis', Symbol('2'))
    #st.write('Vc escolheu:  ', title)

    x1 = solver.NumVar(0, solver.infinity(), 'x1')
    x2 = solver.NumVar(0, solver.infinity(), 'x2')

    print('Número de variáveis =', solver.NumVariables())

    # Restrições
    #1: 
    solver.Add(x1 * 2 + x2 * 5 <= 60)

    #2: 
    solver.Add(x1 + x2 <= 18)

    #3:
    solver.Add(3*x1 + x2 <= 44)

    #4: 
    solver.Add(x2 <= 10)

    #5: Restrição de não-negatividade
    solver.Add(x1 >= 0)
    solver.Add(x2 >= 0)

    print('Número de restrições =', solver.NumConstraints())

    # Função Objetivo
    solver.Maximize(x1 * 2 + x2)

    # Função Objetivo
    solver.Maximize(x1 * 2 + x2)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solução:')
        print('Valor Objetivo =', solver.Objective().Value())
        print('x1 =', x1.solution_value())
        print('x2 =', x2.solution_value())
    else:
        print('O problema não possui uma solução otimizada.')

    print('\nTIME:')
    print('Resolvido em %f ms' % solver.wall_time())
    print('Resolvido em %d iterações' % solver.iterations())


import re
import numpy as np
import pandas as pd

regra = r'(?:(?:restricao:)(?:(?<!\+|\-)[\+\-\s]+\d{0,4}x\d{1,3}[\+\-\s])+(?:[=><]{1,2}[\-\+\s]+\d+(?!\|;\w|\d)))|(?:(?:funcao objetivo:)(?:(?<!\+|\-)[\+\-\s]+\d{0,4}x\d{1,3}[\+\-\s])+(?!\|;\w|\d))|(?:(?:objetivo:)(?:(?<!\+|\-)[\+\-\s](?:maximizar|minimizar)[\+\-\s])+(?!\|;\w|\d))'

doc = """11:32 do teste que 12.12/2012 começara as 28 02 2019.\n
                Em 12 de julho de 2012 ou em 12 12 12 , teste as 02/2/2021 e
   

objetivo: maximizar 
funcao objetivo:  - 2x11 + x32 + x13 - 4x22 + x21 - x31 + x12 
restricao: - x11 + 1x22 - x12 + 3x21 + 4x32 <= 10
restricao: x31 - x12 + 5x11 - x22 <= 20 
restricao: 6x11 - 2x12 + 6x21 - x22 + 4x32 <= 15 
restricao: x22 >= 0

"""

padrao = re.compile(regra, flags = re.IGNORECASE)

coletor = [re.sub(r'[^0-9+-xz ]', '', item).lower() for item in padrao.findall(doc)]

restricoes = [item for item in coletor if 'restricao' in item]

func_obj = [item for item in coletor if 'funcao objetivo' in item]

for item in coletor:
    if 'maximizar' in item:
        objetivo = 'max'

    elif 'minimizar' in item:
        objetivo = 'min'

coletor = set([item[item.find(':')+1:].strip() for item in coletor if len(set(item)) != 1])
restricoes = [item[item.find(':')+1:].strip() for item in restricoes]
func_obj = [item[item.find(':')+1:].strip() for item in func_obj]

print("\nObjetivo:")
print(objetivo.upper()+"imizar".upper())

print("\nFunção Objetivo:")
print("z = ",func_obj[0])

print("\nRestrições:")
[print(item) for item in restricoes]

variaveis = set([item for item in func_obj[0].split() if "x" in item])

print(variaveis)

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

objetivo = np.array([item.split()[-1] for item in restricoes])
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
print(obj)
#print(restr)

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
df['objetivo'] = np.array(objetivo)


print(df)




def gerar_exemplos(exemplo_escolhido):
    
    exemplo1 = """problema: linear

max: 8x1 + 10x2

restricao: 0.5x1 + 0.5x2 <= 150
restricao: 0.6x1 + 0.4x2 <= 145

restricao:  x1 >= 30                                            restricao: x1 <= 150
restricao:  x2 >= 40                                            restricao: x2 <= 200
arredondamento: 3"""

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
r: x141 + x142 + x241 + x242 + x341 = 100
arredondamento: 2"""
    
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
restricao: x3 <= 1                                                restricao: x4 <= 1
arredondamento: 3"""

    exemplo4 = """problema: inteiro

min:  50x11 + 50x12 + 0x13 + 20x14
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
restricao: x14 + x24 + x34 + x44 = 1"""
 
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
restricao:  x7 <= 1                              restricao:  x8 <= 1
"""

    exemplo6 = """problema: inteiro

max: 20x1 + 15x2 + 34x3 + 17x4 + 56x5 + 76x6 + 29x7

restricao: 12x1 + 54x2 + 65x3 + 38x4 + 52x5 + 98x6 + 15x7 <= 200            ANO 0
restricao: 34x1 + 94x2 + 28x3 + 0x4 + 21x5 + 73x6 + 48x7 <= 250             ANO 1 
restricao: 12x1 + 67x2 + 49x3 + 8x4 + 42x5 + 25x6 + 53x7 <= 150             ANO 2

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
restricao: -2x1 + 3x2 <= 9
arredondamento: 6"""

    exemplo8 = """problema: int
min: 104x01 + 110x02 + 122x03 + 559x04 + 462x05 + 104x10 + 8.2x12 + 120x13 + 545x14 + 449x15 + 110x20 + 8.2x21 + 114x23 + 537x24 + 441x25 + 122x30 + 120x31 + 114x32 + 567x34 + 465x35 + 559x40 + 545x41 + 537x42 + 567x43 + 123x45 + 462x50 + 449x51 + 441x52 + 465x53 + 123x54

(RESTRIÇÃO DE SAÍDA)
r: x01 + x02 + x03 + x04 + x05 = 1
r: x10 + x12 + x13 + x14 + x15 = 1
r: x20 + x21 + x23 + x24 + x25 = 1
r: x30 + x31 + x32 + x34 + x35 = 1
r: x40 + x41 + x42 + x43 + x45 = 1 
r: x50 + x51 + x52 + x53 + x54 = 1

(RESTRIÇÃO DE ENTRADA)
r: x10 + x20 + x30 + x40 + x50 = 1
r: x01 + x21 + x31 + x41 + x51 = 1
r: x02 + x12 + x32 + x42 + x52 = 1
r: x03 + x13 + x23 + x43 + x53 = 1
r: x04 + x14 + x24 + x34 + x54 = 1
r: x05 + x15 + x25 + x35 + x45 = 1

(RESTRIÇÃO PARA 2 NÓS)
r: x01 + x10 <= 1
r: x02 + x20 <= 1
r: x03 + x30 <= 1
r: x04 + x40 <= 1
r: x05 + x50 <= 1
r: x12 + x21 <= 1
r: x13 + x31 <= 1
r: x14 + x41 <= 1
r: x15 + x51 <= 1
r: x23 + x32 <= 1
r: x24 + x42 <= 1
r: x25 + x52 <= 1
r: x34 + x43 <= 1
r: x35 + x53 <= 1
r: x45 + x54 <= 1

(RESTRIÇÃO PARA 3 NÓS)
r: x01 + x12 + x20 <= 2
r: x01 + x13 + x30 <= 2
r: x01 + x14 + x40 <= 2
r: x01 + x15 + x50 <= 2
r: x02 + x21 + x10 <= 2
r: x02 + x23 + x30 <= 2
r: x02 + x24 + x40 <= 2
r: x02 + x25 + x50 <= 2
r: x03 + x31 + x10 <= 2
r: x03 + x32 + x20 <= 2
r: x03 + x34 + x40 <= 2
r: x03 + x35 + x50 <= 2
r: x04 + x41 + x10 <= 2
r: x04 + x42 + x20 <= 2
r: x04 + x43 + x30 <= 2
r: x04 + x45 + x50 <= 2
r: x05 + x51 + x10 <= 2
r: x05 + x52 + x20 <= 2
r: x05 + x53 + x30 <= 2
r: x05 + x54 + x40 <= 2

(RESTRIÇÃO PARA 4 NÓS)
r: x01 + x12 + x23 + x30 <= 3 [0 1 2 3]
r: x01 + x12 + x24 + x40 <= 3 [0 1 2 4]
r: x01 + x12 + x25 + x50 <= 3 [0 1 2 5]
r: x01 + x13 + x34 + x40 <= 3 [0 1 3 4]
r: x01 + x13 + x35 + x50 <= 3 [0 1 3 5]
r: x01 + x14 + x45 + x50 <= 3 [0 1 4 5]
r: x02 + x23 + x34 + x40 <= 3 [0 2 3 4]
r: x02 + x23 + x35 + x50 <= 3 [0 2 3 5]
r: x02 + x24 + x45 + x50 <= 3 [0 2 4 5]
r: x03 + x34 + x45 + x50 <= 3 [0 3 4 5]
r: x12 + x23 + x34 + x41 <= 3 [1 2 3 4]
r: x12 + x23 + x35 + x51 <= 3 [1 2 3 5]
r: x12 + x24 + x45 + x51 <= 3 [1 2 4 5]
r: x13 + x34 + x45 + x51 <= 3 [1 3 4 5]
r: x23 + x34 + x45 + x52 <= 3 [2 3 4 5]

(RESTRIÇÃO PARA 5 NÓS)
r: x01 + x12 + x23 + x34 + x40 <= 4 [0 1 2 3 4]
r: x01 + x12 + x24 + x43 + x30 <= 4 [0 1 2 3 5]
r: x01 + x13 + x32 + x24 + x40 <= 4 [0 2 3 4 5]
r: x01 + x13 + x34 + x42 + x20 <= 4 [0 1 2 4 5]
r: x01 + x14 + x42 + x23 + x30 <= 4 [0 1 3 4 5]
r: x12 + x23 + x34 + x45 + x51 <= 4 [1 2 3 4 5] 

(RESTRIÇÃO VARIÁVEIS BINÁRIAS)
r: x01 <= 1 r: x02 <= 1 r: x03 <= 1 r: x04 <= 1 r: x05 <= 1
r: x10 <= 1 r: x12 <= 1 r: x13 <= 1 r: x14 <= 1 r: x15 <= 1  
r: x20 <= 1 r: x21 <= 1 r: x23 <= 1 r: x24 <= 1 r: x25 <= 1  
r: x30 <= 1 r: x31 <= 1 r: x32 <= 1 r: x34 <= 1 r: x35 <= 1  
r: x40 <= 1 r: x41 <= 1 r: x42 <= 1 r: x43 <= 1 r: x45 <= 1
r: x50 <= 1 r: x51 <= 1 r: x52 <= 1 r: x53 <= 1 r: x54 <= 1

arredondamento: 5"""

    dict_exemplos = {"1) Modelo Básico":exemplo1,
                    "2) Problema de Transporte":exemplo2,
                    "3) Programação Binária":exemplo3,
                    "4) Designação":exemplo4,
                    "5) Postes nas ruas":exemplo5,
                    "6) Investimentos":exemplo6,
                    "7) Exemplo de PL":exemplo7,
                    "8) Rota Turística":exemplo8}

    return dict_exemplos[exemplo_escolhido]

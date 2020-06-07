#atenção: antes de carregar o arquivo, abra-o e apaque todos os caracteres
#acentos e símbolos do cabeçalho.

#--------------------
#PARTE 1: COLETAR OS DADOS E IMPRIMIR AS CURVAS
#--------------------

#importa base para tratar dados do arquivo
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#informa o diretorio corrente
curDir = os.getcwd()
print(curDir)

#insere aviso para o arquivo a editar
print("----------\n>>>>ATENÇÃO!<<<<\n----------\n1) NO CABEÇALHO do arquito .txt, substituir ou apagar acentos e pontuações!!!")
print("2) COLOQUE OS ARQUIVOS QUE PRETENDE ABRIR NO MESMO DIRETÓRIO DO ARQUIVO .py"
      "\n----------------")
nome_arquivo = input("informe o nome do arquivo (com a extensão .txt): ")
id_legenda = input("Informe a identificação do CP para a legenda: ")

#insere os dados iniciais do CP e define se o CP eh quadrado, retangular ou circular
comprimento_util = float(input("Informe o comprimento util (mm): "))
geometria = int(input("Geometria do CP: \n >>1<< para cilindrica \n >>2<< para retangular \n >>3<< para quadrada \n Escolha: "))


if geometria == 1:
    diametro = float(input("Diametro (mm): "))
    area_transversal = np.pi*(diametro**2)/4

elif geometria == 2:
    largura = float(input("Insira a largura (mm): "))
    espessura = float(input("Insira a espessura (mm): "))
    area_transversal = largura*espessura

elif geometria == 3:
    largura = float(input("Insira a largura (mm): "))
    area_transversal = largura**2

else:
    print("Entrada invalida")

#no arquivo txt, retirar os caracteres estranhos e acentos.
#chamar as variaveis de tempo (s) Deformacao (mm) e Forca (N)
#dados = pd.read_csv(nome_arquivo, encoding = "UTF-8-sig", header = 0, decimal=",", sep='\t')
dados = pd.read_csv(nome_arquivo, encoding = "latin1", header = 0, decimal=",", sep='\t')


#verifica se os dados estao sendo corretamente lidos
print(dados.head())

#verifica o numero de linhas e colunas
dim_dados = dados.shape
print("Tamanho da base de dados: " + str(dim_dados))

#atribui as variaveis
tempo = dados.iloc[:,0]
desloc = dados.iloc[:,1]
forca = dados.iloc[:,2]

#define as variaveis de tensao e deformacao
deform = desloc/comprimento_util
tensao = forca/area_transversal

#plota o grafico tensao x deformacao
plt.figure(1,figsize=(5, 4), dpi=150)
plt.plot(deform, tensao, 'ro', markersize=2, markerfacecolor=None, label= id_legenda)
plt.title('Curva tensão x deformação')
plt.grid(alpha=0.75,linestyle=':')
plt.axis([0, 1.1*max(deform), 0, 1.1*max(tensao)])
plt.xlabel('Deformação')
plt.ylabel('Tensão (MPa)')
plt.minorticks_on()
plt.legend(loc='best')
plt.show(block=False)

derivada_tensao=np.diff(tensao)
deform_der = deform[:-1]
plt.figure(2,figsize=(5, 4), dpi=150)
plt.title('Derivada da tensão')
plt.plot(deform_der, derivada_tensao, linewidth=0.5,linestyle='-', label= id_legenda)
plt.grid(alpha=0.75,linestyle=':')
plt.axis([0, 1.1*max(deform), -0.05, 1.1*max(derivada_tensao)])
plt.xlabel('Deformação')
plt.ylabel('Derivada da tensão (MPa)')
plt.minorticks_on()
plt.legend(loc = 'best')
plt.show(block=False)
plt.show()


#--------------------
#PARTE 2: LINEARIZA O REGIME ELASTICO E CALCULA O LIMITE DE ESCOAMENTO
#--------------------

#escolhe o intervalo para linearizar e criar a paralela de calculo do LE
intervalo_inferior_tensao = float(input("Valor inferior de tensao para linearizacao (MPa): "))
intervalo_superior_tensao = float(input("Valor superior de tensao para linearizacao (MPa): "))

#para evitar o erro ao detectar pontos na outra parte da curva
lr = max(tensao)
indices_maximo = [inicio for inicio, fim in enumerate(tensao) if fim == lr]
p_indice_maximo = indices_maximo[0]
print(indices_maximo)


#determina o indice do valor mais proximo aquele informado
indice_inferior = min(range(len(tensao[0:p_indice_maximo])), key=lambda i: abs(tensao[i]-intervalo_inferior_tensao))
indice_superior = min(range(len(tensao[0:p_indice_maximo])), key=lambda i: abs(tensao[i]-intervalo_superior_tensao))

#cria uma lista do intervalo e faz o ajuste linear
corte_deform = deform[indice_inferior:indice_superior+1]
corte_tensao = tensao[indice_inferior:indice_superior+1]
#faz o aluste da reta em funcao dos pontos
modelo = np.polyfit(corte_deform, corte_tensao, 1)
print("coeficientes de ajuste: " + str(modelo))

#informa os coeficientes a e b
plt.figure(3,figsize=(5, 4), dpi=150)
plt.plot(corte_deform, corte_tensao, 'b*', markersize=6, markerfacecolor=None, label= id_legenda)
plt.plot(corte_deform,modelo[0]*corte_deform+modelo[1],linewidth=2,color='red',linestyle='-')
plt.title('Reta de ajuste da região elástica')
plt.grid(alpha=0.75,linestyle=':')
plt.axis([0.99*min(corte_deform), 1.01*max(corte_deform), 0.99*min(corte_tensao), 1.01*max(corte_tensao)])
plt.xlabel('Deformação')
plt.ylabel('Tensão (MPa)')
plt.minorticks_on()
plt.legend()
plt.show(block=False)

#calcula os residuais e plota para comparacao
residuais = (modelo[0]*corte_deform+modelo[1])-corte_tensao
#plota o grafico
plt.figure(4,figsize=(5, 4), dpi=150)
plt.plot(corte_deform, residuais, 'ro', markersize=3, markerfacecolor=None, label= id_legenda)
plt.plot(corte_deform,0*residuais,linewidth=2)
plt.title('Residuais')
plt.grid(alpha=0.75,linestyle=':')
#plt.axis([0.95*min(corte_deform), 1.1*max(corte_deform), 0.95**min(residuais), 1.1*max(residuais)])
plt.xlabel('Deformação')
plt.ylabel('Residuais da tensão (MPa)')
plt.minorticks_on()
plt.legend()
plt.show(block=False)
plt.show()


#determina o ponto onde as curvas se encontram para calcular o limite de escoamento

diferencas_curvas = tensao - (modelo[0]*(deform-0.002)+modelo[1])
for indle in range(len(diferencas_curvas) - 1):
    if diferencas_curvas[indle] == 0. or diferencas_curvas[indle] * diferencas_curvas[indle + 1] < 0.:
        limite_escoamento = tensao[indle]
        print("-----------------")
        print("Limite de escoamento: %.2f MPa" % limite_escoamento)
        print("Limite de resistencia: %.2f MPa" % max(tensao))
        print("-----------------")

#determina o indice mais proximo ao valor de limite de escoamento
indice_limite_escoamento = min(range(len(tensao)), key=lambda i: abs(tensao[i]-limite_escoamento))


#cria uma reta com a mesma inclinacao e desloca 0.0002

plt.figure(5,figsize=(5, 4), dpi=150)
plt.plot(deform, tensao, linewidth=1, color='red', linestyle='-', label='Curva Tensão x Deformação')
plt.plot(deform,modelo[0]*(deform-0.002)+modelo[1], linewidth=1,
         color='blue',linestyle='-', label='Curva pelo método do offset')
plt.plot(deform[indice_limite_escoamento], tensao[indice_limite_escoamento], 'ro')
plt.title('Curva Tensão x Deformação')
plt.grid(alpha=0.75,linestyle=':')
plt.axis([0.7*deform[indice_limite_escoamento], 1.2*deform[indice_limite_escoamento],
          0.7*tensao[indice_limite_escoamento], 1.2*tensao[indice_limite_escoamento]])
plt.xlabel('Deformação')
plt.ylabel('Residuais da tensão (MPa)')
plt.minorticks_on()
plt.legend()
plt.show(block=False)
plt.show()

#--------------------
#PARTE 3: FAZ A CORREÇÃO DA CURVA SEGUNDO O MÓDULO DE ELASTICIDADE REAL DO MATERIAL
#--------------------

#entrada do valor do modulo de elasticidade
modulo_elasticidade = float(input("Inserir o módulo de elasticidade real do material (GPa): "))

#define a curva do modulo
tensao_modulo = (modulo_elasticidade*1000)*deform

#determina o indice mais proximo ao valor de limite de escoamento
indice_limite_escoamento_me = min(range(len(tensao_modulo)), key=lambda ime: abs(tensao_modulo[ime]-limite_escoamento))
delta_deform = deform[indice_limite_escoamento] - deform[indice_limite_escoamento_me]
#print("delta: " + str(delta_deform))

deform_corrigida = pd.concat([deform[0:indice_limite_escoamento_me],
                              (deform[indice_limite_escoamento:]-delta_deform)], ignore_index=True)

tensao_corrigida = pd.concat([tensao_modulo[0:indice_limite_escoamento_me],
                              tensao[indice_limite_escoamento:]], ignore_index=True)

#apresenta a curva tensão x deformação já corrigida
plt.figure(6,figsize=(5, 4), dpi=150)
plt.plot(deform_corrigida, tensao_corrigida, 'bo-', markersize=2, markerfacecolor='none', label= id_legenda)
plt.title('Curva tensão x deformação com módulo corrigido')
plt.grid(alpha=0.75,linestyle=':')
plt.axis([0, 1.1*max(deform), 0, 1.1*max(tensao)])
plt.xlabel('Deformação')
plt.ylabel('Tensão (MPa)')
plt.minorticks_on()
plt.legend(loc='best')
plt.show()

#--------------------
#PARTE 4: CRIAR AS CURVAS VERDADEIRAS
#--------------------
#calcula as listas de tensao verdadeira e deformacao verdadeira

deformacao_verdadeira = np.log(deform_corrigida+1)
tensao_verdadeira = [a * b for a, b in zip(tensao_corrigida, (deform_corrigida+1))]

#determina o indice da curva corrigida do primeiro lr
lr_corrigido = max(tensao_corrigida)
indices_maximo_corrigida = [inicio2 for inicio2, fim2 in enumerate(tensao_corrigida) if fim2 == lr]
p_indice_max_corr = indices_maximo_corrigida[0]

plt.figure(7,figsize=(5, 4), dpi=150)
plt.plot(deformacao_verdadeira[0:p_indice_max_corr], tensao_verdadeira[0:p_indice_max_corr],
         'g*-', markersize=1.5, linewidth=0.5, markerfacecolor='none', label= 'Curva Verdadeira')
plt.plot(deform_corrigida, tensao_corrigida, 'bo-', markersize=1.5, linewidth=0.5, markerfacecolor='none', label= 'Curva de Engenharia')
plt.title('Curva tensão verdadeira x deformação verdadeira')
plt.grid(alpha=0.75,linestyle=':')
plt.axis([0, 1.1*max(deform_corrigida), 0, 1.1*max(tensao_verdadeira)])
plt.xlabel('Deformação verdadeira')
plt.ylabel('Tensão Verdadeira (MPa)')
plt.minorticks_on()
plt.legend(loc='best')
plt.show()

#escolhe se quer salvar o arquivo salva a curva corrigida para arquivo .csv
resultado = input("Quer salvar o arquivo? \n responder s ou n:")

while True:
    if resultado == "s":
        dict = {'Deformacao_corrigida': deform_corrigida, 'Tensao_corrigida_MPa': tensao_corrigida,
                'Deformacao_verdadeira': deformacao_verdadeira, 'Tensao_Verdadeira_MPa': tensao_verdadeira}
        arquivo_exportar = pd.DataFrame(dict)
        prefixo_arquivo = input("Definir nome do arquivo (sem o .csv): ")
        arquivo_exportar.to_csv(prefixo_arquivo + '.csv', decimal=',', sep=' ')
        break
    elif resultado == "n":
        print("ok")
        break
    else:
        print("resposta desconhecida")
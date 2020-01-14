import dataset
import numpy as np

NPAD = 862
NENT = 25
NSAI = 1

x = np.zeros((NPAD, NENT))
y = np.zeros((NPAD, NSAI))

dataset.criar_dataset(x, y)

#Variáveis para balanceamento
treino01 = 422
treino02 = 152
teste01 = 212
teste02 = 76
balanc = True

#Treino
arq = open('treino.py', 'w')

treino = []

treino.append('def criar_treino(x, y):\n')
'''for i in range(int(NPAD*(2/3))):
    for j in range(NENT):
        treino.append('\tx['+str(i)+']['+str(j)+'] = '+str(x[i,j])+';\n')
    treino.append('\n')
for i in range(int(NPAD*(2/3))):
    for j in range(NSAI):
        treino.append('\ty['+str(i)+']['+str(j)+'] = '+str(y[i,j])+';\n')
arq.writelines(treino)
arq.close()'''

#Teste
arq2 = open('teste.py', 'w')

teste = []

teste.append('def criar_teste(x, y):\n')
'''for i in range(int(NPAD*(2/3)), NPAD):
    for j in range(NENT):
        teste.append('\tx['+str(i)+']['+str(j)+'] = '+str(x[i,j])+';\n')
    teste.append('\n')
for i in range(int(NPAD*(2/3)), NPAD):
    for j in range(NSAI):
        teste.append('\ty['+str(i)+']['+str(j)+'] = '+str(y[i,j])+';\n')
arq.writelines(teste)
arq.close()'''

#Treino e Teste com balanceamento
treino_cont01 = treino_cont02 = teste_cont01 = teste_cont02 = k = w = 0
flag = False
for i in range(NPAD):
    for j in range(NSAI):
        if y[i, j] == 0.0 and treino_cont01 < treino01:
            treino_cont01 += 1
            for z in range(NENT):
                treino.append('\tx['+str(k)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            treino.append('\n\ty['+str(k)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            k += 1
            flag = True
        elif y[i, j] == 0.0 and teste_cont01 < teste01 and flag == False:
            teste_cont01 += 1
            for z in range(NENT):
                teste.append('\tx['+str(w)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            teste.append('\n\ty['+str(w)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            w += 1
        flag = False

        if y[i, j] == 1.0 and treino_cont02 < treino02:
            treino_cont02 += 1
            for z in range(NENT):
                treino.append('\tx['+str(k)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            treino.append('\n\ty['+str(k)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            k += 1
            flag = True
        elif y[i, j] == 1.0 and teste_cont02 < teste02 and flag == False:
            teste_cont02 += 1
            for z in range(NENT):
                teste.append('\tx['+str(w)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            teste.append('\n\ty['+str(w)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            w += 1
        flag = False

arq.writelines(treino)
arq.close()
arq2.writelines(teste)
arq2.close()

import dataset
import numpy as np

NPAD = 1000
NENT = 25
NSAI = 1

x = np.zeros((NPAD, NENT))
y = np.zeros((NPAD, NSAI))

dataset.criar_dataset(x, y)

'''
#D1
arq = open('d1.txt', 'w')

d1 = []

for i in range(250):
    for j in range(NENT):
        d1.append('x['+str(i)+']['+str(j)+'] = '+str(x[i,j])+';\n')
    d1.append('\n')
for i in range(250):
    for j in range(NSAI):
        d1.append('y['+str(i)+']['+str(j)+'] = '+str(y[i,j])+';\n')
arq.writelines(d1)

#D2
arq = open('d2.txt', 'w')

d2 = []
k = 0
for i in range(250, 500):
    for j in range(NENT):
        d2.append('x['+str(k)+']['+str(j)+'] = '+str(x[i,j])+';\n')
    k += 1
    d2.append('\n')
k = 0
for i in range(250, 500):
    for j in range(NSAI):
        d2.append('y['+str(k)+']['+str(j)+'] = '+str(y[i,j])+';\n')
    k += 1
arq.writelines(d2)

#D3
arq = open('d3.txt', 'w')

d3 = []
k = 0
for i in range(500, 750):
    for j in range(NENT):
        d3.append('x['+str(k)+']['+str(j)+'] = '+str(x[i,j])+';\n')
    k += 1
    d3.append('\n')
k = 0
for i in range(500, 750):
    for j in range(NSAI):
        d3.append('y['+str(k)+']['+str(j)+'] = '+str(y[i,j])+';\n')
    k += 1
arq.writelines(d3)

#D4
arq = open('d4.txt', 'w')

d4 = []
k = 0
for i in range(750, 1000):
    for j in range(NENT):
        d4.append('x['+str(k)+']['+str(j)+'] = '+str(x[i,j])+';\n')
    k += 1
    d4.append('\n')
k = 0
for i in range(750, 1000):
    for j in range(NSAI):
        d4.append('y['+str(k)+']['+str(j)+'] = '+str(y[i,j])+';\n')
    k += 1
arq.writelines(d4)'''

#Variáveis para balanceamento
d101 = d201 = d301 = d401 = 175
d102 = d202 = d302 = d402 = 75

d1 = []
d2 = []
d3 = []
d4 = []

arq = open('d1.py', 'w')
arq2 = open('d2.py', 'w')
arq3 = open('d3.py', 'w')
arq4 = open('d4.py', 'w')

d1.append('def criar_d1(x, y):\n')
d2.append('def criar_d2(x, y):\n')
d3.append('def criar_d3(x, y):\n')
d4.append('def criar_d4(x, y):\n')

#K-Fold com balanceamento
d1_cont01 = d1_cont02 = d2_cont01 = d2_cont02 = d3_cont01 = d3_cont02 = d4_cont01 = d4_cont02 = kd1 = kd2 = kd3 = kd4 = 0
flag = False
for i in range(NPAD):
    for j in range(NSAI):
        if y[i, j] == 0.0 and d1_cont01 < d101:
            d1_cont01 += 1
            for z in range(NENT):
                d1.append('\tx['+str(kd1)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            d1.append('\n\ty['+str(kd1)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            kd1 += 1
            flag = True
        elif y[i, j] == 0.0 and d2_cont01 < d201 and flag == False:
            d2_cont01 += 1
            for z in range(NENT):
                d2.append('\tx['+str(kd2)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            d2.append('\n\ty['+str(kd2)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            kd2 += 1
            flag = True
        elif y[i, j] == 0.0 and d3_cont01 < d301 and flag == False:
            d3_cont01 += 1
            for z in range(NENT):
                d3.append('\tx['+str(kd3)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            d3.append('\n\ty['+str(kd3)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            kd3 += 1
            flag = True
        elif y[i, j] == 0.0 and d4_cont01 < d401 and flag == False:
            d4_cont01 += 1
            for z in range(NENT):
                d4.append('\tx['+str(kd4)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            d4.append('\n\ty['+str(kd4)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            kd4 += 1
        flag = False

        if y[i, j] == 1.0 and d1_cont02 < d102:
            d1_cont02 += 1
            for z in range(NENT):
                d1.append('\tx['+str(kd1)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            d1.append('\n\ty['+str(kd1)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            kd1 += 1
            flag = True
        elif y[i, j] == 1.0 and d2_cont02 < d202 and flag == False:
            d2_cont02 += 1
            for z in range(NENT):
                d2.append('\tx['+str(kd2)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            d2.append('\n\ty['+str(kd2)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            kd2 += 1
            flag = True
        elif y[i, j] == 1.0 and d3_cont02 < d302 and flag == False:
            d3_cont02 += 1
            for z in range(NENT):
                d3.append('\tx['+str(kd3)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            d3.append('\n\ty['+str(kd3)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            kd3 += 1
            flag = True
        elif y[i, j] == 1.0 and d4_cont02 < d402 and flag == False:
            d4_cont02 += 1
            for z in range(NENT):
                d4.append('\tx['+str(kd4)+']['+str(z)+'] = '+str(x[i,z])+';\n')
            d4.append('\n\ty['+str(kd4)+']['+str(j)+'] = '+str(y[i,j])+';\n\n')
            kd4 += 1
        flag = False

arq.writelines(d1)
arq.close()
arq2.writelines(d2)
arq2.close()
arq3.writelines(d3)
arq3.close()
arq4.writelines(d4)
arq4.close()

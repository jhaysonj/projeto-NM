from random import randint

# etapa 1 - escolher o numero aleatorio
randomico_esoj = 15
randomico_jhayson = 13


# etapa 2 calcular o (x ** randomico) mod y, sendo x e y numeros publicos, acordados anteriormente.
calcula_esoj = (3**15) % 17
calcula_jhayson = (3**13) % 17

print(calcula_esoj,calcula_jhayson)


# etapa 3 - ambas as partes utilizam o resultado do outro
print(calcula_esoj**randomico_jhayson % 17)
print(calcula_jhayson**randomico_esoj % 17)

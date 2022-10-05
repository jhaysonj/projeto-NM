# representacao do ip em binario
ip = 0b11000000101010000000000000001010

# representacao da mascara em binario
mascara = 0b11111111111111111111111100000000

# resultado do and bit a bit entre o ip e a mascara
resultado_and_binario = bin(ip&mascara)


print("Resultado do AND bit a bit")

# estrutura para printar bonitinho, divindo os binarios em 4 octetos
print("binario: ", end="")
for c in range(0, 4):
    if c == 0:
        print(resultado_and_binario[2:10], end=" . ")
        
    elif(c != 3):
        print(resultado_and_binario[(8*c)+2:8*(c+1)+2], end=" . ")
        
    else:
        print(resultado_and_binario[(8*c)+2:8*(c+1)+2])
        

# estrutura para printar em decimal
octeto1 = resultado_and_binario[2:10]   # [2:10] ignora o "0b" inicial e copia apenas os 8 digitos binarios
octeto1 = int(octeto1, 2)       # converte o primeiro octeto de binario para decimal

octeto2 = resultado_and_binario[10:18]   # [10:18] copia 8 digitos binarios
octeto2 = int(octeto2, 2)        # converte o segundo octeto de binario para decimal

octeto3 = resultado_and_binario[18:26]   # [18:26] copia 8 digitos binarios
octeto3 = int(octeto3, 2)        # converte o terceiro octeto de binario para decimal

octeto4 = resultado_and_binario[26:32]   # [26:32] copia 8 digitos binarios
octeto4 = int(octeto4, 2)        # converte o quarto octeto de binario para decimal

resultado_and_decimal = str(octeto1) + " . " +  str(octeto2) + " . " + str(octeto3) + " . " + str(octeto4)
print(f"decimal: {resultado_and_decimal}")
# 11000000 10100010 00000000 00000000
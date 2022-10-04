# representacao do ip em binario
ip = 0b11000000101000100000000000001010

# representacao da mascara em binario
mascara = 0b11111111111111111111111100000000

# resultado do and bit a bit entre o ip e a mascara
print(bin(ip&mascara))

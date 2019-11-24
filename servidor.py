from socket import *
from math import gcd
from random import randint

def gerar_primos(numero_final):
    primos = [2,3]

    for novo_primo in range(5, numero_final + 1, 2):
        is_primo = False
        teste = []

        for primo in primos:
            if is_primo:
                break

            mdc = gcd(primo,novo_primo)

            if primo ** 2 > novo_primo and mdc == 1:
                primos.append(novo_primo)
                break

            elif mdc != 1:
                is_primo = True

    return primos

def escolher_primo(numeros_primos):
    primo_aleatorio = numeros_primos[randint(22,len(numeros_primos) -1)]
    return primo_aleatorio

def escolher_gerador(primo):

    gerador_true = 0
    while gerador_true == 0:
        p_aleatorio = randint(2, primo)

        for expoente in range(2,primo+1):
            g = 0
            mod = (p_aleatorio ** expoente) % primo
            if mod == 1 and expoente != primo-1:
                break
            else:
                g = p_aleatorio

        if g > 0:
            gerador_true = g
            return gerador_true

def gerar_chaves(numeros_primos):
    p = escolher_primo(numeros_primos) #Numero primo
    g = escolher_gerador(p)            #Raiz primitiva modulo p (gerador)
    a = randint(2,p-2)                 #Chave privada
    r = (g ** a) % p                   #Elemento da chave publica
    chave_publica = [p,g,r]
    chave_privada = a
    print("|p: {:>6}|\n|g: {:>6}|\n|r: {:>6}|\n|a: {:6}|".format(p,g,r,a))
    return [chave_publica,a]

def tab_conversao():
    conversao = {"a":10, "b":11, "c":12, "d":13,"e":14, "f":15, "g":16, "h":17, "i":18, "j":19, "k":20, "l":21, "m":22, "n":23, "o":24, "p":25, "q":26, "r":27, "s":28, "t":29, "u":30, "v":31, "w":32, "x":33, "y":34, "z":35, " ":36, "0":37, "1":38, "2":39, "3":40, "4":41, "5":42, "6":43, "7":44, "8":45, "9":46, "A":47, "B":48, "C":49, "D":50, "E":51, "F":52, "G":53, "H":54, "I":55, "J":56, "K":57, "L":58, "M":59, "N":60, "O":61, "P":62, "Q":63, "R":64, "S":65, "T":66, "U":67, "V":68, "W":69,"X":70, "Y":71, "Z":72}
    return conversao

def criptografar(chave_publica,mensagem,tabela_conversao):
    p = int(chave_publica[0])
    g = int(chave_publica[1])
    r = int(chave_publica[2])
    k = randint(2, p-2)

    mensagem_criptografada_bytes = b''

    y = (g ** k) % p
    delta = []
    mensagem_criptografada_bytes += str(y).encode("UTF-8")+";".encode("UTF-8")

    for caracter in mensagem:
        m = tabela_conversao[caracter]
        m = m * (r ** k) % p
        mensagem_criptografada_bytes += str(m).encode("UTF-8")+";".encode("UTF-8")
        delta.append(m)

    return [mensagem_criptografada_bytes]

def descriptografar(chave_publica,chave_privada,mensagem_criptografada,tabela_conversao):
    p = int(chave_publica[0])
    a = chave_privada

    mensagem_criptografada = mensagem_criptografada.decode()
    mensagem_criptografada = mensagem_criptografada[:-1]
    mensagem_criptografada = mensagem_criptografada.split(";")

    y = int(mensagem_criptografada[0])

    y = y ** (p - 1 - a) % p
    mensagem = mensagem_criptografada[1:]
    mensagem_descripto = []

    for m in mensagem:
        descifragem = y * int(m) % p
        mensagem_descripto.append(descifragem)

    return converter_para_texto(mensagem_descripto,tabela_conversao)

def converter_para_texto(mensagem_descriptografada,tabela_conversao):
    mensagem = []

    for ma in mensagem_descriptografada:

        for caract, num in tabela_conversao.items():
            if ma == num:
                mensagem.append(caract)

    return "".join(mensagem)

def main():

    numeros_primos = gerar_primos(2887)
    chaves = gerar_chaves(numeros_primos)
    tabela_conversao = tab_conversao()
    chave_publica = chaves[0]
    minha_chave = chave_publica
    chave_privada = chaves[1]

    meu_host = ""
    minha_porta = 5555

    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.bind((meu_host, minha_porta))
    sockobj.listen(5)
    conexao, endereco = sockobj.accept()
    client_chave_publica = conexao.recv(1024)
    server_chave_publica = str(str(chave_publica[0])+"."+str(chave_publica[1])+"."+str(chave_publica[2])).encode("UTF-8")

    for linha in [server_chave_publica]:
        conexao.send(linha)

    client_chave_publica = client_chave_publica.decode().split(".")
    chave_publica = [int(client_chave_publica[0]),int(client_chave_publica[1]),int(client_chave_publica[2])]

    while True:

        print("Cliente conectado IP: {}".format(endereco[0]))

        while True:
            data = conexao.recv(1024)
            print("Mensagem criptografada:",data)
            data = descriptografar(minha_chave,chave_privada,data,tabela_conversao)
            print("Alice:",data, end="\n\n")

            mensagem = input("Bob: ")
            mensagem = criptografar(chave_publica,mensagem,tabela_conversao)

            for linha in mensagem:
                conexao.send(linha)

    conexao.close()

main()

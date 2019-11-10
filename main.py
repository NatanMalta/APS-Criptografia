from random import randint

def gerar_numero_primo():

    is_primo = False
    while is_primo == False:
        numero_aleatorio = randint(10 ** 10, 20 ** 20)
        if numero_aleatorio % 2 > 0 and numero_aleatorio % 3 > 0 and numero_aleatorio % 5 > 0 and numero_aleatorio % 7 > 0:
            is_primo = True
        """if numero_aleatorio % 2 > 0:
            if numero_aleatorio % 3 > 0:
                if numero_aleatorio % 5 > 0:
                    if numero_aleatorio % 7 > 0:
                        is_primo = True
        """
    return numero_aleatorio

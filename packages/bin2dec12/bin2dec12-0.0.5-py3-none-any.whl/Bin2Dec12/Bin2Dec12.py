def conversao():

    numero = list(input("Digite o número binário: "))
    reducao = len(numero) - 1
    resultado =[]
    for x in numero:
        resultado.append(int((int(x)*(2**reducao))))
        reducao -= 1

    return print(sum(resultado))
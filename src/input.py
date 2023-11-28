def write_file(data):
    nome_arquivo = "../in/teste"
    with open(nome_arquivo, 'a') as arquivo:
        # Escreve os dados no arquivo
        arquivo.write(data)


def clear_file():
    nome_arquivo = "../in/teste"
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write("")


def save_line(valores):
    # Concatena os valores da lista com espaços entre eles
    linha = ' '.join(map(str, valores))

    # Abre o arquivo no modo de escrita ('w')
    write_file(linha+"\n")


clear_file()

# Minimizar ou maximizar
func = input("Minimizar (1) ou Maximizar (2)?")
write_file(func+"\n")

# Variaveis de decisao
qnt_vars = int(input("Quantas variaveis de decisão (que influenciam na função objetivo): "))

# Variaveis de restricao
qnt_rest = int(input("Quantidade de restrições (sem contar com a função objetivo): "))

# Salvando no arquivo
qnt_colunas = qnt_vars + qnt_rest + 1 # variaveis de decisão + 1 termo pra cada restrição + LD
qnt_linhas = qnt_rest + 1
write_file(str(qnt_linhas)+" "+str(qnt_colunas)+"\n")


# Função Objetivo
j=1
values = []
while j <= qnt_vars:
    aux = input("Função Objetivo. Valor de x"+ str(j) +": ")
    values.append(aux)
    j += 1
j=1
while j <= qnt_vars+2:
    values.append(0)
    j += 1
save_line(values)

# Restrições
i = 2
while i <= qnt_linhas:
    j = 1
    values = []
    while j <= qnt_colunas:
        aux = input(str(i)+". Valor de x"+ str(j) +": ")
        values.append(aux)
        j += 1
    save_line(values)

    i += 1

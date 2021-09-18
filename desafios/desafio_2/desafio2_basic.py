#conceito de leitura de arquivo
list_salarys_arq = open ('lista_de_nomes.csv', 'r')
list_salarys_metadata = list_salarys_arq.read().split("\n")
list_salarys_arq.close()

#conceito de template string
template_string = "nome:{}, Idade: {}, Salario: {}"

#conceito iteração em objetos.
for user_metadata in list_salarys_metadata:
    user_format_metadata = user_metadata.split(";")
    print (template_string.format(user_format_metadata[0], user_format_metadata[1], user_format_metadata[2]))
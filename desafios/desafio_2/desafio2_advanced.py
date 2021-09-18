import json

#conceito de leitura de arquivo
list_salarys_arq = open ('lista_de_nomes.csv', 'r')
list_salarys_metadata = list_salarys_arq.read().split("\n")
list_salarys_arq.close()


list_salarys_arq_json = open ('lista_salario.json', 'w')
list_salarys_arq_json.close()

final_list_objetcts = []

#conceito iteração em objetos.
for user_metadata in list_salarys_metadata:
    user_format_metadata = user_metadata.split(";")
    final_list_objetcts.append({
        "nome": str(user_format_metadata[0]), 
        "Idade": str(user_format_metadata[1]),
        "Salario": str(user_format_metadata[2]),
    })


#gravação de objeto formatado.
list_salarys_arq_json = open ('lista_salario.json', 'a')
list_salarys_arq_json.write(json.dumps(final_list_objetcts, indent=4, sort_keys=False))
list_salarys_arq_json.close()

print (json.dumps(final_list_objetcts, indent=4, sort_keys=False)) 
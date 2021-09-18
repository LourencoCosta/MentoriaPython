variavel_numero = 20


string_comum = "ALGUMA COISA COM VALOR: " + str(variavel_numero) + " ALGUMA COISA COM VALOR: " + str(variavel_numero + 2) + " ALGUMA COISA COM VALOR: " + str(variavel_numero + 4)

string_template = "ALGUMA COISA COM VALOR: {}, ALGUMA COISA COM VALOR: {}, ALGUMA COISA COM VALOR: {}"

print(string_template.format(variavel_numero, variavel_numero + 2, variavel_numero + 4))



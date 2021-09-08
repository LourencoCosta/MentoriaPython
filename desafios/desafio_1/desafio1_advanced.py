import requests
import json

response = requests.request("GET", "https://viacep.com.br/ws/1305810/json/unicode/")

if (response.status_code == 200):
    response_json = json.loads(response.text)
    string_template = "Logradouro: {}, Bairro: {}, Cidade: {}, Estado: {}, CEP: {}"
    print(string_template.format(str(response_json['logradouro']), str(response_json['bairro']), str(response_json['localidade']), str(response_json['uf']), str(response_json['cep'])))
else:
    print ("Houve um erro ao consultar o cep")


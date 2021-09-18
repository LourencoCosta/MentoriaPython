import requests
import json

response = requests.request("GET", "https://viacep.com.br/ws/1305810/json/unicode/")

if (response.status_code == 200):
    response_json = json.loads(response.text)
    string_template = "Logradouro: {}, Bairro: {}, Cidade: {}, Estado: {}, CEP: {}"
    print(string_template.format(response_json['logradouro'], response_json['bairro'], response_json['localidade'], response_json['uf'], response_json['cep']))
else:
    print ("Houve um erro ao consultar o cep")


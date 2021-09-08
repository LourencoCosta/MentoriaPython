import requests

response = requests.request("GET", "https://viacep.com.br/ws/1305810/json/unicode/")

print(response.text)
import json
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from pyjavaproperties import Properties

#ID da planilha 
sheet_id = "1dkfxvJjBu4VArdKh4QO7j6LEUKzjawdQYPkU3TxrQPE"

#ID da apesentação 
id_presenstation_template = "11Wfe_fSxLjjfDebyUmbCnLizTLlSJfP-Qa_Cl2EN7Is"

#Essa variavel será utilizada para armazenar as credenciais
credentials = None

#Essa variavel será utilizada armazenar o idioma do properties
pt_br_properties = None



#gerador de credenciais
#Na primeira vez que esse metodo for executado será necesário realizar a uma autenticação no google e 
#habilitar a permissão para utilizar os recurso do Google utilizados na conta

#OBS 1: APÓS a primeira execução desse método será gerado um arquivo token.pickle que armazenará as credencias 
#para não ser preciso gerar as credencias para todas as chamadas

#OBS 2: O arquivo client_secret.json é obrigatório para que esse método funcione, esse arquivo é extraido da plataforma, 
#após a configuração das credencias no console do Google
def generate_google_credentials():
    #se for necessário mais APIs podem ser adicionadas no Escopo da Plataforma
    scopes = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/spreadsheets']
    
    global credentials

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', scopes)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

#atualizador de planilha
def update_sheet(metrics, client):
    service = build('sheets', 'v4', credentials=credentials)

    #Abre arquivos com metadados que serão preenchidos nas planilhas
    with open('sheet_request_body.json', 'r') as sheet_request_body_file:
        body = sheet_request_body_file.read().replace("CUSTOMER_NAME", client)
        body = json.loads(body)

    #Insere as informações em um formato valido para ser adicionado a Planilha
    for api in metrics:
        body["data"][0]["values"].append(
            [api["key"], api["doc_count"]]
        )

    #Atualiza a planilha
    service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body=body).execute()

#Funcao especial para carregar o idioma do properties
def load_properties_file(language):
    global pt_br_properties
    switcher = {
        "pt_br": pt_br_properties
    }

    if not switcher[language]:
        switcher[language] = Properties()
        switcher[language].load(open('pt_br.properties'))

    return switcher.get(language, None)


#atualizador de Apresentação
def update_presentation(presentation_id):
    #configuração de credencias para acessos necessários
    slide_service = build('slides', 'v1', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)

    resource_bundle = load_properties_file("pt_br")

    body = {
        'name': resource_bundle["presentation.name"].format("V1")
    }

    #Criação de copia do template onde serão incluidas as informações
    drive_response = drive_service.files().copy(fileId=presentation_id, body=body, supportsAllDrives=True).execute()
    
    presentation_copy_id = drive_response.get('id')

    #Abre o template que carregará os labels customizados para dentro da apresentação
    with open('presentation_request_body.json', 'r') as f:
        presentation_request_body = json.loads(f.read())

    #Formata os labels da apresentação de acordo com os labels presentes no arquivo de properties
    for item in presentation_request_body:
        key = item["replaceAllText"]["containsText"]["text"]
        resource_bundle_value = resource_bundle.get(key)
        if resource_bundle_value or resource_bundle_value == 0:
            item["replaceAllText"]["replaceText"] = str(resource_bundle_value)

    body = {
        'requests': presentation_request_body
    }

    #Atualiza o a apresentação com os labels corretos
    slide_service.presentations().batchUpdate(presentationId=presentation_copy_id, body=body).execute()
    
    #Recupera o ID dos slides para realizar os UPDATDE DE SLIDES
    new_presentation_slides = slide_service.presentations().get(presentationId=presentation_copy_id).execute().get('slides')
    refresh_charts_body = []

    #formata os dados da requisição para a API do Google para atualizar os slides 
    for slide in new_presentation_slides:
        for element in slide.get('pageElements'):
            if element.get("sheetsChart"):
                refresh_charts_body.append({
                    "refreshSheetsChart": {
                        "objectId": str(element.get("objectId"))
                    }
                })

    body["requests"] = refresh_charts_body

    #Atualiza a apresentação.
    try:
        slide_service.presentations().batchUpdate(presentationId=presentation_copy_id, body=body).execute()
    except Exception as e:
        print("Unable to refresh charts of " + " presentation: " + str(e))


def main():
    #Datos que serao escritos na planilha
    metadata = []
    metadata.append ({"key": "CHAVE 310", "doc_count": "25000"})
    metadata.append ({"key": "CHAVE 320", "doc_count": "17"})

    #Gera credenciais para as realizar as chamadas as APIs do Google
    generate_google_credentials()

    #Realizar Update na planilha do Google
    update_sheet(metadata, "TEST_ESCRITA")

    #Realizar Update na apresentção do Google
    update_presentation(id_presenstation_template)


main()


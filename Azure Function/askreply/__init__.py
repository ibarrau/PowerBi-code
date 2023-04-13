import logging
import requests
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the request body
    req_body = req.get_body()

    # Convert the request body from bytes to string
    req_body_str = req_body.decode('utf-8')

    try:
        res = json.loads(req_body_str)
        pregunta = res["message"]["text"]
    except:
        pregunta = None

    logging.info(f'La pregunta es: {pregunta} y el Request body: {req_body_str}')

    def ask_gpt(pregunta):
        if pregunta == None:
            rta = "No se pudo leer la pregunta"
        else:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer [KEY]'
            }    
            data = '{"model": "text-davinci-003", "prompt": "'+pregunta+'", "temperature": 0, "max_tokens": 2048}'
            try:
                response = requests.post('https://api.openai.com/v1/completions', headers=headers, data=data)
                rta = response.json()["choices"][0]["text"]
            except:
                rta = "No se pudo obtener una respuesta"
        return rta

    def send_text(rta):
        url = 'https://api.telegram.org/bot5877593639:AAEIxkpCEv0tvhYcWnqztK77cSoHx444n9o/sendMessage?chat_id=5844708880&parse_mode=Markdown&text={}'.format(rta)
        requests.get(url)
        
    rta = ask_gpt(pregunta)

    send_text(rta)

    return func.HttpResponse(f'La pregunta fue: {pregunta} y su respuesta es: {rta}')


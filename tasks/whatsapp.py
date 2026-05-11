import requests
from urllib.parse import quote

def enviar_whatsapp(numero, mensagem, api_key):
    # CallMeBot: número no formato 5534999998888 (sem + ou espaços)
    url = (
        f"https://api.callmebot.com/whatsapp.php"
        f"?phone={numero}&text={quote(mensagem)}&apikey={api_key}"
    )
    resp = requests.get(url, timeout=10)
    return resp.status_code == 200
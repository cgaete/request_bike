import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# URL del sitio web de Canyon, sección Outlet
url = 'https://www.canyon.com/es-cl/outlet-bicicletas/?prefn1=pc_welt&prefv1=Triatl%C3%B3n&searchType=bikes&srule=outlet_high_stock'

# Función para enviar SMS usando Twilio
def send_sms(body, to_phone):
    account_sid = ''
    auth_token = ''
    from_phone = ''
    
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=body,
            from_=from_phone,
            to=to_phone
        )
        print(f"SMS enviado exitosamente: SID {message.sid}")
    except Exception as e:
        print(f"Error al enviar SMS: {e}")

# Función para verificar bicicletas de triatlón
def check_triatlon_bikes():
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al acceder a la página.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    triatlon_bikes = []
    for bike in soup.find_all('div', class_='productTileDefault__productSummary'):
        bike_name_tag = bike.find('div', class_='productTileDefault__productNameWrapper')
        bike_price_tag = bike.find('div', class_='productTile__priceSale')

        # Verificar si la bicicleta es de triatlón
        if bike_name_tag and ('Triatlón' in bike_name_tag.text or 'Speedmax' in bike_name_tag.text):
            bike_name = bike_name_tag.text.strip()
            bike_price = bike_price_tag.text.strip() if bike_price_tag else "Precio no disponible"
            triatlon_bikes.append((bike_name, bike_price))

    if triatlon_bikes:
        print("Bicicletas de triatlón disponibles en el outlet:")
        message = "Bicicletas de triatlón disponibles en el outlet:\n"
        for bike in triatlon_bikes:
            bike_info = f"Nombre: {bike[0]}, Precio: {bike[1]}"
            print(bike_info)
            message += bike_info + "\n"

        send_sms(message, "")
    else:
        print("No hay bicicletas de triatlón en el outlet en este momento.")

if __name__ == "__main__":
    check_triatlon_bikes()

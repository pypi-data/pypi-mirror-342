import requests

def get_weather(city: str):

    url = f"http://wttr.in/{city}?format=%l:+%t,+%C"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"Ошибка при получении данных: {str(e)}"
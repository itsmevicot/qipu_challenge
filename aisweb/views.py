from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import requests
from datetime import datetime


def home(request):
    return redirect('aisweb:aerodrome')


def get_busca_value():
    try:
        response = requests.get('https://aisweb.decea.mil.br/?i=aerodromos&p=sol')
        response.raise_for_status()  # Raise an error for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find('input', {'name': 'busca'})['value']

    except requests.RequestException:
        return {"error": "There was an issue connecting to the website while fetching busca value."}
    except Exception as e:
        return {"error": f"An error occurred while fetching busca value: {str(e)}"}


def get_sunrise_sunset_info(icaocode):
    try:
        busca_value = get_busca_value()
        current_date = datetime.now().strftime('%d/%m/%y')
        data = {
            'icaocode': icaocode,
            'dt_i': current_date,
            'dt_f': current_date,
            'busca': busca_value
        }
        response = requests.post('https://aisweb.decea.mil.br/?i=aerodromos&p=sol', data=data)
        response.raise_for_status()  # Raise an error for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table table-striped mt-4')
        if table:
            row = table.find('tbody').find('tr')
            columns = row.find_all('td')
            context = {
                'icaocode': icaocode,
                'date': columns[0].text,
                'day_of_week': columns[1].text,
                'sunrise': columns[2].text,
                'sunset': columns[3].text
            }

            return context
        return {"error": "No data found for the provided ICAO code."}

    except requests.RequestException:
        return {"error": "There was an issue connecting to the website."}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def get_card_info(icaocode_string):
    try:
        icaocodes = [code.strip() for code in icaocode_string.split(',')]
        cards = []

        for icaocode in icaocodes:
            post_data = {
                'icaocode': icaocode,
                'tipo': '0',
                'carta': '',
                'pe': '0',
                'amdt': '0',
                'uso': 'all',
                'busca': get_busca_value()
            }

            response_cards = requests.post('https://aisweb.decea.mil.br/?i=cartas', data=post_data)
            response_cards.raise_for_status()

            soup = BeautifulSoup(response_cards.content, 'html.parser')
            table = soup.find('table', {'id': 'datatable'})

            if table:
                rows = table.find_all('tr')[1:]  # Exclude header row
                for row in rows:
                    cols = row.find_all('td')

                    localidade = cols[1].find('a').text.strip()
                    tipo = cols[2].find('a').text.strip()
                    carta = cols[3].find('a').text.strip()
                    amdt = cols[4].find('a').text.strip()
                    data_efetivacao = cols[5].find('a').text.strip()
                    uso = cols[6].text.strip()

                    card_data = {
                        'localidade': localidade,
                        'tipo': tipo,
                        'carta': carta,
                        'amdt': amdt,
                        'data_efetivacao': data_efetivacao,
                        'uso': uso
                    }
                    cards.append(card_data)

        return cards

    except requests.RequestException:
        return {"error": "There was an issue connecting to the website while fetching card info."}
    except Exception as e:
        return {"error": f"An error occurred while fetching card info: {str(e)}"}


def get_metar_taf(icaocode):
    try:
        url = f"https://aisweb.decea.mil.br/?i=aerodromos&codigo={icaocode}#met"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Get METAR
        metar_tag = soup.find('h5', text="METAR")
        metar = None
        if metar_tag:
            metar = metar_tag.find_next('p').text.strip()

        # Get TAF
        taf_tag = soup.find('h5', text="TAF")
        taf = None
        if taf_tag:
            taf = taf_tag.find_next('p').text.strip()

        context = {
            'METAR': metar,
            'TAF': taf
        }

        return context

    except requests.RequestException:
        return {"error": "There was an issue connecting to the website while fetching METAR/TAF info."}
    except Exception as e:
        return {"error": f"An error occurred while fetching METAR/TAF info: {str(e)}"}


def get_aerodrome_info(request):
    context = {}

    if request.method == 'POST':
        icaocode = request.POST.get('icaocode')

        # Get sunrise and sunset info
        sun_info = get_sunrise_sunset_info(icaocode)
        if "error" in sun_info:
            context["error"] = sun_info["error"]
            return render(request, 'aisweb/aerodrome.html', context)
        context.update(sun_info)

        # Get METAR and TAF info
        metar_taf_info = get_metar_taf(icaocode)
        if "error" in metar_taf_info:
            context["error"] = metar_taf_info["error"]
            return render(request, 'aisweb/aerodrome.html', context)
        context.update(metar_taf_info)

        # Get card information
        cards = get_card_info(icaocode)
        if "error" in cards:
            context["error"] = cards["error"]
            return render(request, 'aisweb/aerodrome.html', context)
        context['cards'] = cards
        context['card_count'] = len(cards)

        return render(request, 'aisweb/aerodrome.html', context)

    return render(request, 'aisweb/aerodrome.html')



from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import requests
from datetime import datetime


def home(request):
    return redirect('aisweb:aerodrome')


def get_busca_value():
    try:
        response = requests.get('https://aisweb.decea.mil.br/?i=aerodromos&p=sol')
        response.raise_for_status()  # Levanta um erro para bad requests

        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find('input', {'name': 'busca'})['value']

    except requests.RequestException:
        return {"error": "Houve um problema ao conectar ao site ao buscar o valor de busca."}
    except Exception as e:
        return {"error": f"Ocorreu um erro ao buscar o valor de busca: {str(e)}"}


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
        response.raise_for_status()  # Levanta um erro para bad requests

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
        return {"error": "Nenhum dado encontrado para o código ICAO fornecido."}

    except requests.RequestException:
        return {"error": "Houve um problema ao conectar ao site."}
    except Exception as e:
        return {"error": f"Ocorreu um erro: {str(e)}"}


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
                rows = table.find_all('tr')[1:]  # Exclui a linha do cabeçalho
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
        return {"error": "Houve um problema ao conectar ao site ou ao buscar informações dos cartões aeronáuticos."}
    except Exception as e:
        return {"error": f"Ocorreu um erro ao buscar informações do cartão aeronáutico: {str(e)}"}


def get_metar_taf(icaocode):
    try:
        url = f"https://aisweb.decea.mil.br/?i=aerodromos&codigo={icaocode}#met"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Pega o METAR
        metar_tag = soup.find('h5', text="METAR")
        metar = None
        if metar_tag:
            metar = metar_tag.find_next('p').text.strip()

        # Pega o TAF
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
        return {"error": "Houve um problema ao buscar pelo METAR/TAF."}
    except Exception as e:
        return {"error": f"Ocorreu um erro ao buscar informações METAR/TAF: {str(e)}"}


def get_aerodrome_info(request):
    context = {}

    if request.method == 'POST':
        icaocodes_input = request.POST.get('icaocode')
        icaocodes = [code.strip() for code in icaocodes_input.split(',')]

        all_sun_info = []
        all_metar_taf_info = []
        all_cards = []

        for icaocode in icaocodes:
            # Pega informações de nascer e pôr do sol
            sun_info = get_sunrise_sunset_info(icaocode)
            if "error" in sun_info:
                context["error"] = sun_info["error"]
                return render(request, 'aisweb/aerodrome.html', context)
            all_sun_info.append(sun_info)

            # Pega informações METAR e TAF
            metar_taf_info = get_metar_taf(icaocode)
            if "error" in metar_taf_info:
                context["error"] = metar_taf_info["error"]
                return render(request, 'aisweb/aerodrome.html', context)
            all_metar_taf_info.append(metar_taf_info)

            # Pega informações do cartão
            cards = get_card_info(icaocode)
            if "error" in cards:
                context["error"] = cards["error"]
                return render(request, 'aisweb/aerodrome.html', context)
            all_cards.append(cards)

        combined_data = zip(all_sun_info, all_metar_taf_info, all_cards)
        context['combined_data'] = combined_data

        return render(request, 'aisweb/aerodrome.html', context)

    return render(request, 'aisweb/aerodrome.html')

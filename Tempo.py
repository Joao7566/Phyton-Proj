import requests
import json
from datetime import date
## impoort pprint

accuweatherAPIKey = 'arlQSLXlcyzq0MlPTmSv1X3JTzkY0yGB'
dias_semana = ['Domingo','Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado']

def pegarcoordenadas():
    r = requests.get('http://www.geoplugin.net/json.gp')

    if (r.status_code != 200):
        print ('Não foi possivel obter a localização.')
        return None
    else:
        try:
            localizacao = json.loads(r.text)
            coordenadas = {}
            coordenadas['lat'] = localizacao['geoplugin_latitude']
            coordenadas['long'] = localizacao['geoplugin_longitude']
            return coordenadas
        except:
            return None

def pegarcodigolocal(lat, long):
    locationapiurl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/"\
    +"search?apikey=" + accuweatherAPIKey\
    +"&q=" + lat + "%2C"+ long +"&language=pt-br"

    r = requests.get(locationapiurl)
    if (r.status_code != 200):
        print ('Não foi possivel obter o codigo do local.')
        return None
    else:
        try:
            locationresponse = json.loads(r.text)
            infolocal = {}
            infolocal['nomelocal'] = locationresponse['LocalizedName'] + ", " \
                        +locationresponse['AdministrativeArea']['LocalizedName'] + ". "\
                        +locationresponse['Country']['LocalizedName']
            infolocal['codigolocal'] = locationresponse['Key']
            return infolocal
        except:
            return None

def pegartempoagora(codigolocal, nomelocal):

    currentconditionsapiurl = "http://dataservice.accuweather.com/currentconditions/v1/"\
                              +codigolocal+"?apikey="+accuweatherAPIKey + "&language=pt-br"
    r = requests.get(currentconditionsapiurl)
    if (r.status_code != 200):
        print ('Não foi possivel obter o clima atual.')
        return None
    else:
        try:
            currentconditionsresponse = json.loads(r.text)
            infoclima = {}
            infoclima['textoclima'] = currentconditionsresponse[0]['WeatherText']
            infoclima['temperatura'] = currentconditionsresponse[0]['Temperature']['Metric']['Value']
            infoclima['nomelocal'] = nomelocal
            return infoclima
        except:
            return None


def pegarprevisao5dias(codigolocal):

    dailyapiurl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" \
                              + codigolocal+"?apikey="+accuweatherAPIKey + "&language=pt-br&metric=true"
    r = requests.get(dailyapiurl)
    if (r.status_code != 200):
        print ('Não foi possivel obter o clima atual.')
        return None
    else:
        try:
            dailyresponse = json.loads(r.text)
            infoclima5dias =  []
            for dia in dailyresponse['DailyForecasts']:
                climadia = {}
                climadia['max'] = dia ['Temperature']['Maximum']['Value']
                climadia['min'] = dia ['Temperature']['Minimum']['Value']
                climadia['clima'] = dia ['Day']['IconPhrase']
                diasemana = int(date.fromtimestamp(dia['EpochDate']).strftime('%w'))
                climadia['dia'] = dias_semana[diasemana]
                infoclima5dias.append(climadia)
            return infoclima5dias   
            
        except:
            return None



def mostrarprevisao(lat, long):
    try:
        local = pegarcodigolocal(lat, long)
        climaatual = pegartempoagora(local ['codigolocal'], local['nomelocal'])
        print ('Clima atual em: ' + climaatual['nomelocal'])
        print (climaatual['textoclima'])
        print ('Temperatura: ' + str(climaatual['temperatura']) + '\xb0' + 'C')
    except:
        print ('Erro ao obter o clima atual.')
    opcao = input('Deseja ver a previsão para os próximos dias? (s ou n): ').lower()

    if opcao == 's':
        print ('\nClima para hoje e para os próximos dias:\n')

        try:
            previsao5dias = pegarprevisao5dias(local ['codigolocal'])
            for dia in previsao5dias:
                print (dia['dia'])
                print ('Mínima: ' + str (dia['min'])+ '\xb0' + 'C')
                print ('Máxima: ' + str (dia['max'])+ '\xb0' + 'C')
                print ('Clima: ' + dia['clima'])
                print ('----------------------------')
        except:
            print ('Erro ao obter a previão para os próximos dias.')

 

try:
    coordenadas = pegarcoordenadas()
    mostrarprevisao (coordenadas['lat'], coordenadas['long'])
        
except:
    print ('Erro ao processar a solicitação. Entre em contato com o suporte.')



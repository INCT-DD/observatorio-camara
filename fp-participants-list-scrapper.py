import pandas as pd
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import math

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

fpurl = "https://www.camara.leg.br/internet/deputado/frentes.asp"
urlprefix = "https://www.camara.leg.br/internet/deputado/"

fplist = {'name': [], 'link': []}

useragent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
http = urllib3.PoolManager(10, headers=useragent)

print('Loading webpage source...')

fpsource = http.request('GET', fpurl)
fpsoup = BeautifulSoup(fpsource.data, features="html.parser")

print('Searching for required tables...')

fptable = fpsoup.find('table')
fprows = fptable.findAll('a')

print('Loading participant tables...')

fpsize = math.floor(len(fprows) / 2)

with tqdm(total=fpsize, position=0, leave=True) as pbar:
    for element in fprows:
        if "integra" not in element['href'] and "dcd" not in element['href']:
            fpname = re.sub(r'\W+', '', element.getText())
            fpname = (fpname[:255] + '..') if len(fpname) > 255 else fpname
            fplink = urlprefix + element['href']

            fpremotesource = http.request('GET', fplink)
            fpremotesoup = BeautifulSoup(fpremotesource.data, features="html.parser")

            participanttable = fpremotesoup.find_all('table')[0]

            df = pd.read_html(str(participanttable))[0]
            df.drop([0], axis=0, inplace=True)
            df.drop(df.tail(1).index, inplace=True)
            df['Frente Parlamentar'] = fpname
            df.to_csv('./fp-participant-list/' + fpname + '.csv')

            pbar.update(1)

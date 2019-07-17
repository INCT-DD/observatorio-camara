import pandas as pd
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm

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

print('Loading names and URLs...')

fpsize = len(fprows)

with tqdm(total=fpsize, position=0, leave=True) as pbar:
    for element in fprows:
        if "integra" not in element['href'] and "dcd" not in element['href']:
            fplist['name'].append(element.getText())
            fplist['link'].append(urlprefix + element['href'])
        pbar.update(1)

print('Saving list to table...')

df = pd.DataFrame(fplist)
df.to_csv('./fplist/fplist.csv')

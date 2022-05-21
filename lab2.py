import json
import boto3 as boto3
import pandas as pd
import requests
import matplotlib.pyplot as plt

# отримуємо данні щодо курсів валют
request = requests.get(
    url="https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&sort=exchangedate&order=desc&json")

# конвертуємо обьект в строку джсон
jsonD = json.dumps(request.json())

# створюємо з джсону csv файл
df = pd.read_json(jsonD)
df.to_csv(r'info.csv', index=None)


# завантажуємо файл з данними в бакет та с бакету
s3 = boto3.client('s3')
s3.upload_file('info.csv', 'cloudtech123123', 'info.csv')
s3.download_file('cloudtech123123', 'info.csv', 'info_downloaded.csv')

# отримуємо дані по євро та доллару
data = pd.read_csv('info_downloaded.csv')
eur = data.where(data['cc'] == 'EUR').sort_values(by='exchangedate').dropna()
usd = data.where(data['cc'] == 'USD').sort_values(by='exchangedate').dropna()

# будуємо графік та завантажуємо його в бакет
fig, ax = plt.subplots()
ax.plot(eur['exchangedate'], eur['rate'], label='EUR')
ax.plot(usd['exchangedate'], usd['rate'], label='USD')
fig.set_figheight(32)
fig.set_figwidth(32)
ax.set_xlabel('Timeline')
ax.set_ylabel('Rate')
ax.legend()
fig.savefig('chart.png')
s3.upload_file('chart.png', 'cloudtech123123', 'chart.png')
plt.show()


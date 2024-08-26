dict={}
# headers = {
#     'Content-Type': 'application/json',
#     'X-OPENFIGI-APIKEY': '025c78bd-1473-4862-8db9-98d08e1618f2',
# }

# data = '[{"idType":"ID_ISIN","idValue":"INF204KB15V2"}]'

# response = requests.post('https://api.openfigi.com/v3/mapping', headers=headers, data=data)
# print(response.json()[0]['data'][0]['ticker'])
# for row in data:
#    dict[row[1]]=row[0]

# headers = {
#     'Content-Type': 'application/json',
#     'X-OPENFIGI-APIKEY': '025c78bd-1473-4862-8db9-98d08e1618f2',
# }
# name=[]
# OpenFIGI_ticker=[]
# Actual_ticker=[]
# Isin_number=[]
# count=0
# for isin in dict:
#     if count == 1993:
#         break
#     if count%100 == 0:
#         time.sleep(6)
#     if isin != "ISIN NUMBER":
#         data = f'[{{"idType":"ID_ISIN","idValue":"{isin}"}}]'

#         response = requests.post('https://api.openfigi.com/v3/mapping', headers=headers, data=data)
        
#         res = response.json()
#         if dict[isin] != res[0]['data'][0]['ticker']:
#             print(res[0]['data'][0]['name'],dict[isin],res[0]['data'][0]['ticker'])
#             name.append(res[0]['data'][0]['name'])
#             OpenFIGI_ticker.append(res[0]['data'][0]['ticker'])
#             Actual_ticker.append(dict[isin])
#             Isin_number.append(isin)
#     count=count+1


# df=pd.DataFrame({'Name':name,'ISIN':Isin_number,'OpenFIGI Ticker':OpenFIGI_ticker,'Actual Ticker':Actual_ticker})
# df.to_csv('Ticket_Diff.csv',index=False)
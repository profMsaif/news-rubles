import requests

class MOEXParser:

   def flatten(j: dict, blockname: str):
        return [{k: r[i] for i, k in enumerate(j[blockname]['columns'])} for r in j[blockname]['data']]

   def query(url):
      try:
         headers = {
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.2.644 Yowser/2.5 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            }
         r = requests.get(url, headers)
         r.encoding = 'utf-8'
         j = r.json()
         return j
      
      except Exception as e:
         print("query error %s" % str(e))
         return None


   def getPars():
      urlEUR = "https://iss.moex.com/iss/engines/currency/markets/selt/boardgroups/13/securities/EUR_RUB__TOD.json?marketdata.columns=LAST,SECID,UPDATETIME&iss.meta=off"
      urlUSD = "https://iss.moex.com/iss/engines/currency/markets/selt/boardgroups/13/securities/USD000000TOD.json?marketdata.columns=LAST,SECID,UPDATETIME&iss.meta=off"
      eur = MOEXParser.query(urlEUR)
      usd = MOEXParser.query(urlUSD)
      eurDict = MOEXParser.flatten(eur, 'marketdata')
      usdDict = MOEXParser.flatten(usd, 'marketdata')
      return eurDict, usdDict
   
# class 


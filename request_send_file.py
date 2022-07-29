import requests
from datetime import datetime

files = {'file': open('somefile.zip', 'rb')}
r = requests.post('http://localhost:8188/', files=files)
startt = datetime.now()
try:
    print(r.request.headers)
except Exception as e:
    print(e)
endd = datetime.now()
print("durasi: {}".format(endd - startt))
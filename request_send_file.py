import requests
from datetime import datetime

filename= 'mov_bbb.mp4'
filepath = '/base-path/service-upload-file/{}'.format(filename)
files = {'file': (filename, open(filepath, 'rb'), 'text/xml'),
         'Content-Disposition': 'form-data; name="file"; filename="' + filename + '"',
         'Content-Type': 'text/xml'}
r = requests.post('http://localhost:8188/', files=files)
startt = datetime.now()
try:
    print(r.request.headers)
except Exception as e:
    print(e)
endd = datetime.now()
print("durasi: {}".format(endd - startt))
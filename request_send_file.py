import requests
from datetime import datetime

headers = {
    'Authorizetion': 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==',
}
filename= 'mov_bbb.mp4'
filepath = '/Users/hilmankholik/Desktop/HILMAN_KHOLIK/1_SIDE/1_FILESERVICE/service-upload-file/{}'.format(filename)
files = {'file': (filename, open(filepath, 'rb'), 'text/xml'),
         'Content-Disposition': 'form-data; name="file"; filename="' + filename + '"',
         'Content-Type': 'text/xml'}
r = requests.post('http://localhost:8188/', files=files, headers=headers)

startt = datetime.now()
try:
    print(r.request.headers)
    print(r.json())
except Exception as e:
    print(e)
endd = datetime.now()
print("durasi: {}".format(endd - startt))
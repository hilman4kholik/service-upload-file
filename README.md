# service-upload-file

Terdapat 4 file:
- fileserver.ini
    Untuk setting static folder tempat dimana file yang akan kita upload disimpan.
    File ini dibaca oleh program utama fileserver.py sebagai config.
- fileserver.py
    File program utama yang dijalankan serbagai service/Backend.
- upload_form.html
    Untuk contoh penggunaan upload file menggunakan form html.
- request_send.py
    Untuk contoh penggunaan upload file melalui request program.

default port: 8188

Cara menjalankan program:
```
python3 fileserver.py
```
buka localhost:8188 di browser

<img width="430" alt="Screen Shot 2022-07-29 at 15 07 12" src="https://user-images.githubusercontent.com/5362063/181714158-60e18c55-9f95-485d-a2d9-3699a24f9359.png">

Cara akses file yang telah diupload:

```
http://localhost:8188/{namafilenya}
```


## Untuk testnya

1. Sesuaikan isi file request_send.py lalu jalankan.
```
python3 -m pip install requests

python3 request_send.py
```

2. Buka file upload_form.html menggunakan browser, lalu pilih file yang akan diupload dan klik button upload.


## SS
Pilih File:

<img width="724" alt="Screen Shot 2022-07-29 at 15 12 19" src="https://user-images.githubusercontent.com/5362063/181715517-3d121ed1-0663-45af-9120-d0552c6bcd52.png">

Klik Upload:

<img width="795" alt="Screen Shot 2022-07-29 at 15 12 42" src="https://user-images.githubusercontent.com/5362063/181715585-4855bfdb-0ac7-41ba-a2cb-4cd5bafba42e.png">

Response:

<img width="661" alt="Screen Shot 2022-07-29 at 15 13 12" src="https://user-images.githubusercontent.com/5362063/181715724-7187bef2-d8d2-496a-99e7-58750de82e41.png">

Log service:

<img width="866" alt="Screen Shot 2022-07-29 at 15 14 03" src="https://user-images.githubusercontent.com/5362063/181715805-40563fc4-9b5f-4979-b078-e6538c21f068.png">

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

## Untuk testnya

1. Sesuaikan isi file request_send.py lalu jalankan.
```
python3 -m pip install requests

python3 request_send.py
```

2. Buka file upload_form.html menggunakan browser, lalu pilih file yang akan diupload dan klik button upload.

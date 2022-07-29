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

## Untuk testnya

1. Sesuaikan isi file request_send.py lalu jalankan.
```
python3 -m pip install requests

python3 request_send.py
```

2. Buka file upload_form.html menggunakan browser, lalu pilih file yang akan diupload dan klik button upload.

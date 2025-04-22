# SMTP Checker CLI

**smtp-checker-cli** adalah alat baris perintah (CLI) untuk memeriksa status server SMTP. Alat ini berguna untuk memverifikasi apakah server SMTP berfungsi dengan baik dan dapat mengirim email tanpa masalah. Dengan menggunakan **smtp-checker-cli**, Anda dapat memeriksa server SMTP secara cepat dan mudah melalui terminal.

---

## Fitur

- **Cek Server SMTP:** Memverifikasi apakah server SMTP dapat menghubungi dan mengirim email.
- **Support TLS/SSL:** Mendukung koneksi aman menggunakan protokol TLS dan SSL.
- **Pengaturan Kustom:** Dapat dikonfigurasi untuk menggunakan server SMTP tertentu dan kredensial pengguna.
- **Pemrograman Modular:** Menyediakan API dan fungsionalitas yang dapat digunakan dalam proyek lain.

---

## Instalasi

### Persyaratan

- Python 3.6+ (disarankan untuk menggunakan `virtualenv` atau `venv`).
- `pip` untuk menginstal dependensi.

### Langkah-langkah Instalasi

1. **Clone repository ini:**
    ```bash
    git clone https://github.com/Mrv3n0m666/smtp-checker-cli.git
    cd smtp-checker-cli
    ```

2. **Buat virtual environment (opsional tetapi disarankan):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Untuk Linux/macOS
    venv\Scripts\activate      # Untuk Windows
    ```

3. **Instal dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Jalankan alat:**
    ```bash
    python -m smtp_checker.cli
    ```

---

## Penggunaan

### Cek Server SMTP
Untuk memeriksa status server SMTP, jalankan perintah berikut:
```bash
python -m smtp_checker.cli --server smtp.example.com --port 587 --username user@example.com --password yourpassword

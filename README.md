# BypasnksBOT 🤖

BOT BYPAS ALL TYPE - Telegram Bot untuk bypass verification page, shortlink, dan download otomatis.

## ✨ Fitur Utama

- ✅ **Bypass Verification Page** - Lewati verification yang menghalangi download
- 📌 **Bypass Shortlink** - Resolve shortlink seperti bit.ly, tinyurl, dll
- 💾 **Download Otomatis** - Download file langsung dari link yang sudah di-bypass
- 🔍 **Link Detection** - Otomatis mendeteksi tipe link
- ⚡ **Fast Processing** - Proses link cepat dan efisien

## 🚀 Cara Menggunakan

### 1. Setup Bot

```bash
# Clone repository
git clone https://github.com/alfiedafa3/BypasnksBOT.git
cd BypasnksBOT

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env dan masukkan TELEGRAM_TOKEN Anda
```

### 2. Dapatkan Bot Token

1. Buka [@BotFather](https://t.me/botfather) di Telegram
2. Ketik `/newbot` dan ikuti instruksi
3. Copy token bot Anda
4. Masukkan ke file `.env`

### 3. Jalankan Bot

```bash
python bot.py
```

### 4. Gunakan Bot

- Buka bot di Telegram
- Ketik `/start`
- Kirim link yang ingin di-bypass
- Bot akan memproses dan memberikan link hasil bypass
- Download atau copy link sesuai kebutuhan

## 📋 Perintah Bot

| Perintah | Fungsi |
|----------|--------|
| `/start` | Mulai bot dan tampilkan welcome message |
| `/help` | Tampilkan bantuan penggunaan |
| `/about` | Info tentang bot |
| `/stats` | Statistik penggunaan bot |

## 🔗 Tipe Link yang Support

### ✅ Supported
- **Shortlink**: bit.ly, tinyurl, adf.ly, etc
- **Verification Page**: Any site with verification step
- **Download Links**: MediaFire, MEGA, Google Drive, dll
- **Redirect Links**: HTTP/HTTPS redirects

### ⏳ In Progress
- CAPTCHA bypass
- JavaScript-rendered page
- Cloudflare bypass

## 📁 Struktur Project

```
BypasnksBOT/
├── bot.py              # Main bot handler
├── bypasser.py         # Link bypasser module
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## 🛠️ Dependencies

- `python-telegram-bot` - Telegram Bot API wrapper
- `requests` - HTTP library
- `beautifulsoup4` - HTML parser
- `selenium` - Browser automation (untuk advanced bypass)
- `python-dotenv` - Environment variables

## ⚠️ Disclaimer

Bot ini **hanya untuk edukasi** dan **penggunaan pribadi**. Penggunaan untuk kegiatan ilegal atau melanggar ToS platform akan menjadi tanggung jawab pengguna.

**Gunakan dengan bijak!**

## 📝 Fitur yang Akan Datang

- [ ] Database untuk tracking links
- [ ] Advanced CAPTCHA bypass
- [ ] Support untuk lebih banyak platform
- [ ] Statistics & analytics dashboard
- [ ] Multi-language support
- [ ] Admin panel

## 🐛 Bug Report & Saran

Jika menemukan bug atau punya saran, buat issue di [GitHub Issues](https://github.com/alfiedafa3/BypasnksBOT/issues)

## 📄 Lisensi

This project is open source and available under the MIT License.

## 👨‍💻 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📞 Kontak

- GitHub: [@alfiedafa3](https://github.com/alfiedafa3)
- Telegram: [@alfiedafa3](https://t.me/alfiedafa3)

---

**Made with ❤️ by alfiedafa3**

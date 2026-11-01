# NCK Operations Control Center — pilot lokal

Aplikasi Django + PostgreSQL untuk mencoba alur operasional NCK di MacBook. Semua data diberi label **Data contoh**. Awan Media Indonesia adalah pelanggan B2B eksternal, bukan divisi NCK.

## Membuka aplikasi

Alamat: http://127.0.0.1:8000

Jika server belum berjalan, buka `start.command` dari Finder atau jalankan dari Terminal:

```sh
cd '/Users/ademuhamadfaisal/Documents/ChatGPT/CEO NCK/apps/nck-operations'
./start.command
```

Pilih akun demo di layar masuk. Password semua akun: `nck-demo-2026`.

| Akun | Hak utama |
|---|---|
| admin | Order, alokasi, semua pencatatan, keputusan restock, prioritas, pembatalan |
| warehouse | Alokasi FIFO, picking, terima transfer, usulan restock |
| operator | Hasil produksi, transfer, rework produksi, hambatan |
| qc | Hasil QC, rework QC, penerimaan ke QC, packing, serah-terima |
| finance | Monitoring dan laporan biaya / ekspor |
| management | Monitoring dan laporan biaya / ekspor |

Tutup proses web dengan Ctrl+C pada Terminal. PostgreSQL menyimpan data di `.data/postgres`. Untuk menghentikan database setelah web ditutup, jalankan `./stop-database.command`. Seed hanya berjalan saat database belum memiliki order; membuka ulang tidak mereset pekerjaan.

## Alur yang dapat dicoba

1. Masuk sebagai admin → **Order & Pengiriman → Order baru**. Isi resi, referensi sumber, seller dan beberapa SKU. Resi atau referensi ganda ditolak.
2. Stok eligible direservasi FIFO. **Detail order → Picking** memindahkan barang ke pekerjaan QC. Kekurangan stok dengan desain siap masuk printing; desain belum siap menunggu konfirmasi admin di Stok & PPIC.
3. **Pekerjaan Saya / Produksi & Vendor**: catat baik, hold, scrap dan nama pelaksana. Hasil baik dapat diserahkan sebagian. Penerima mengonfirmasi jumlah aktual sebelum tahap berikutnya mendapat input.
4. DTF: printing → press → QC. Jersey: printing → press → cutting → jahit vendor → QC. Hasil vendor dapat kembali sebagian; belum menjadi barang siap sebelum QC.
5. **Detail order → Konfirmasi packing** baru tersedia jika seluruh item lulus QC. **Serah-terima ekspedisi** memerlukan bukti; pickup 18.00 harus dikonfirmasi. Resi tercetak saja bukan pengiriman.
6. **Stok & PPIC → Usul restock**: masukkan forecast total kebutuhan yang belum terpenuhi dalam horizon 7 hari, WIP yang dipastikan selesai tepat waktu, dan dasar keputusan. WIP tidak boleh melebihi catatan eligible. Rumus `max(K, F) − stok bruto − WIP tepat waktu`, minimal 0. Forecast mencakup K, tidak ditambah lagi ke K.
7. **Keputusan Admin**: setujui menjadi produksi restock atau tolak dengan alasan. Perubahan data membuat usulan lama perlu dihitung ulang. Barang restock baru masuk stok ketika QC baik.
8. **Laporan**: periksa aktivitas pencatat/pelaksana, output, estimasi biaya per seller, dan ekspor CSV berlabel demo. Biaya tidak dikirim ke browser akun produksi.

## Definisi angka

- Order hari ini: paket non-batal dengan tanggal penerimaan WIB hari ini.
- Same-day: paket dari kohort hari ini yang benar-benar diserahkan hari ini / total paket kohort. Angka hari berjalan sementara. Denominator kosong ditampilkan `—`.
- Pending: paket non-batal yang belum diserahkan, termasuk backlog hari sebelumnya.
- Nilai order bukan kas masuk atau omzet yang diakui. Estimasi HPP memakai snapshot standar saat order dibuat; biaya hilang tidak diganti nol untuk menghitung margin lengkap.
- Stok siap, reservasi, dan WIP terpisah. Stok eksklusif hanya eligible bagi sellernya. Indikator 60 hari tanpa penjualan adalah contoh ambang review, bukan kebijakan diskon otomatis.
- Rekomendasi restock bukan ETA atau janji same-day. PPIC wajib mengonfirmasi jadwal WIP; forecast belum dihasilkan model prediksi.

## Teknologi dan pengujian

Runtime lokal tersimpan di `../../.tools/nck-runtime`: Python 3.12, PostgreSQL 17. Dependensi Python dikunci dalam `requirements.lock.txt`. Skema database menggunakan migrasi Django. Server web port 8000; PostgreSQL port 55432. Keduanya hanya bind ke loopback.

```sh
../../.tools/nck-runtime/bin/python manage.py test core --noinput
```

Pengujian memakai database terpisah `test_nck_operations`, bukan database demo. Transaksi command memakai lock global pilot, transaksi atomic, idempotency key, validasi versi, pemeriksaan role server-side dan CSRF. Lock global sengaja sederhana; belum benchmark untuk 100.000 pcs/bulan.

## Batas iterasi pertama

Ini pilot yang dapat dipakai untuk review alur, **belum rilis untuk transaksi operasional nyata**. BRD/PRD/FRD/TRD tetap menjadi arah pengembangan; seluruh cakupannya belum diimplementasikan.

- BigSeller, impor CSV/staging, sinkronisasi saldo, write-back, worker/outbox, AI, WhatsApp dan layanan eksternal belum aktif.
- Tidak ada forecast otomatis, ETA kapasitas finite, komitmen jadwal vendor berversi, master bahan baku/BOM, purchasing, pembukuan double-entry atau profit aktual.
- Perubahan SKU/seller, alih stok eksklusif, diskon dead stock, revisi order dan pemulihan WIP dari order batal belum memiliki formulir. Data master awal dibuat oleh seed. WIP batal tetap ada dan terlihat pada detail order; jangan menganggapnya otomatis kembali ke stok.
- Scrap dicatat dan membuat kekurangan tetap terlihat; penggantian scrap menjadi produksi tambahan belum otomatis. Prioritas admin tidak mencabut reservasi/WIP yang sudah dibuat.
- Dashboard diperbarui setelah aksi dan melalui tombol Perbarui; belum push realtime. Filter periode lanjutan, pagination, notifikasi dengan PIC, OKR, CRM dan marketing ditunda.
- Role operator masih kelompok produksi, belum scope per stasiun. Login demo memakai password diketahui; database loopback memakai trust untuk lingkungan lokal. Jangan mengekspos port ke LAN/internet atau memasukkan data pelanggan nyata sebelum hardening autentikasi, backup, HTTPS, dan kontrol operasi disiapkan.
- PostgreSQL menyimpan data setelah restart, tetapi backup terjadwal / uji restore belum disiapkan. Font Syne dan Plus Jakarta Sans disimpan lokal beserta lisensi OFL.

File rancangan berada di `../../output/nck-planning`. Lihat `IMPLEMENTATION.md` untuk ringkasan verifikasi dan batasnya.

## Asisten NCK — ChatGPT dan Gemini

Tombol **Asisten NCK** di kanan bawah tersedia setelah login pada semua halaman. Default ChatGPT (OpenAI), pilihan kedua Gemini. Chat memiliki saran pertanyaan, status koneksi, sumber konteks, error yang dapat dicoba ulang, dan tombol Chat baru. Riwayat hanya berada di memori tab, terpisah per penyedia, serta dihapus ketika akun/peran berganti atau halaman direload.

Asisten menggunakan `knowledge/nck.md`, potongan relevan BRD/PRD/FRD dari folder planning, serta snapshot operasional terbaru yang telah difilter menurut peran server-side. Konteks detail dibatasi 40 order/pool/job dan 20 keputusan; ringkasan mencakup seluruh order non-batal. Pengetahuan bukan seluruh vault Obsidian. Sumber yang tidak ada atau data di luar cakupan tidak boleh diklaim diketahui. Asisten tidak punya tool mutasi.

**Tanpa API key dan model, panel berjalan dalam mode referensi lokal, bukan AI generatif.** Tidak ada permintaan ke penyedia. Setelah dikonfigurasi, pesan, riwayat singkat, referensi bisnis, dan snapshot sesuai akses dikirim ke penyedia yang dipilih. Tidak ada fallback diam-diam ke penyedia lain.

Untuk mengaktifkan model, jalankan `./configure-ai.command` di Terminal dari direktori aplikasi. Pilih `openai` atau `gemini`, isi ID model yang tersedia di akun API, kemudian masukkan API key pada prompt tersembunyi. Ulangi untuk penyedia kedua. Key disimpan pada `.ai-config.json` dengan permission 0600, diabaikan Git, tidak tersedia lewat static server, dan tidak dikirim ke browser. Jangan masukkan API key melalui percakapan asisten. Buka ulang panel untuk memperbarui status, tanpa restart server.

Alternatif konfigurasi melalui environment server: `OPENAI_API_KEY` + `OPENAI_MODEL`, atau `GEMINI_API_KEY` + `GEMINI_MODEL`. Model harus dipilih eksplisit, tidak di-hardcode. Konfigurasi lengkap berarti siap dicoba, bukan bukti kredensial/kuota valid. Status kegagalan ditampilkan saat penyedia menolak atau timeout.

Konektor menggunakan [OpenAI Responses API](https://developers.openai.com/api/docs/guides/text) dan [Gemini generateContent](https://ai.google.dev/api/generate-content). OpenAI request memakai `store: false`; riwayat aplikasi tidak disimpan ke database. Kebijakan penyimpanan penyedia tetap mengikuti akun/layanan yang digunakan.

Verifikasi penambahan: tes tanpa koneksi memeriksa tidak ada network call, role login, penolakan system-role dari klien, penyaringan biaya operator, kerahasiaan key pada status/error, format request kedua provider dan parsing hasil dengan respons tiruan. Koneksi live belum diuji karena API key belum dipasang.

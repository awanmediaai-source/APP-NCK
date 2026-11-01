# BRD — NCK Operations Control Center

Versi: 0.1 · Tanggal: 1 November 2026 (Asia/Jakarta)

Status: draft untuk review pemilik. Dokumen perencanaan, bukan persetujuan implementasi atau janji hasil. Keputusan eksplisit pemilik dibedakan dari usulan dan kebutuhan validasi.

## 1. Ringkasan bisnis

PT. NUSA CIPTA KREASI (NCK) adalah manufaktur fashion B2B yang melayani seller dan brand melalui produksi serta dropship. Awan Media Indonesia merupakan pelanggan B2B, bukan unit internal dalam cakupan aplikasi.

NCK membutuhkan pusat kendali internal yang menghubungkan order, produksi, persediaan, vendor, pengiriman, keuangan, dan tanggung jawab tim. Tujuan utamanya meningkatkan pengiriman hari yang sama dan mengurangi pending tanpa menambah persediaan secara berlebihan. Transparansi margin dan kemandirian tim menjadi hasil pendamping.

Target 100.000 pcs/bulan pada 2030 menjadi arah skalabilitas bisnis; bukan kapasitas saat ini atau kebutuhan kapasitas teknis yang otomatis disepakati.

## 2. Masalah dan hipotesis penyebab

| Masalah | Hipotesis penyebab yang perlu dibuktikan | Dampak |
|---|---|---|
| Order tertunda saat SKU tidak tersedia | Kebijakan stok belum membedakan SKU stabil, baru, viral, dan menurun | Pengiriman terlambat |
| Stok tren tersisa | Keputusan restock belum cukup mempertimbangkan penurunan permintaan, produksi berjalan, dan risiko modal | Dead stock dan margin turun |
| Antrean tidak seimbang | Kapasitas, serah-terima parsial, dan kesiapan pekerjaan belum terlihat bersama | Waktu tunggu dan pekerjaan menumpuk |
| Pemilik menjadi pusat koordinasi | Prioritas, PIC, dan aturan pengecualian belum cukup eksplisit | Ketergantungan operasional |
| Margin belum transparan | Biaya belum konsisten terhubung ke order | Keputusan harga/pelanggan kurang terukur |

Dashboard saja tidak menyelesaikan masalah ini. Aplikasi harus membantu keputusan stok, penjadwalan pekerjaan, dan estimasi serah-terima ekspedisi berdasarkan data yang sama.

## 3. Kondisi operasional sebagai dasar

- Seller mengirim resi; satu paket dapat memuat beberapa SKU, ukuran, dan jumlah. Semua item harus siap sebelum paket dinyatakan siap kirim.
- Order umumnya masuk sekitar pukul 10.00. Pickup pukul 13.00 dan 16.00; pickup 18.00 hanya jika diminta dan dikonfirmasi.
- Ready stock: picking → QC → packing → serah-terima ekspedisi.
- DTF tanpa stok jadi: desain jika diperlukan → printing → press ke kaos polos → QC → packing → ekspedisi. Desain baru diperkirakan sekitar satu hari.
- Jersey tanpa stok jadi: desain jika diperlukan → printing → press → cutting → jahit vendor → QC → packing → ekspedisi.
- Cutting/jahit melibatkan vendor eksternal. Batas lokasi dan tanggung jawab serah-terima cutting masih perlu dirinci.
- Hasil produksi dapat diteruskan secara parsial; minimum transfer belum ditetapkan.
- Kapasitas ideal total divisi: printing jersey ±50 pcs/jam; press jersey ±25 pcs/jam; printing DTF ±50 pcs/jam; press DTF ±60 pcs/jam. Ini referensi historis, bukan kecepatan yang dijamin.
- Output normal historis jersey ±125 pcs/hari dan DTF ±250 pcs/hari; perlu dicocokkan dengan realisasi terbaru.
- Vendor jahit mengalokasikan ±300 pcs/hari untuk NCK; lead time keluar sampai kembali sekitar 24 jam. Estimasi 10 menit/pcs tidak digunakan untuk menghitung kapasitas serial.
- Kapasitas cutting dan ukuran batch untuk durasi 3–6 jam belum diketahui. Durasi tersebut tidak dipakai sebagai durasi baku setiap order.
- Data order tersedia sejak Mei 2026 melalui Sheets, BigSeller, dan n8n; kelengkapan belum diaudit.
- Review restock saat ini setiap Rabu dengan perhatian utama pada histori tujuh hari.
- Sekitar dua bulan tanpa penjualan/pergerakan keluar menjadi pemicu evaluasi stok mati. Ambang formal dan jenis pergerakan yang dihitung perlu disepakati.

## 4. Tujuan dan ukuran keberhasilan

| Tujuan | Ukuran | Status target |
|---|---|---|
| Meningkatkan same-day | Rasio paket masuk pada suatu hari yang diserahkan ke ekspedisi pada hari itu; dilengkapi rasio pcs | Baseline dan target numerik belum ditetapkan |
| Mengurangi pending | Jumlah paket/pcs belum terkirim pada cut-off, umur pending, alasan keterlambatan | Definisi cut-off dan target perlu disetujui |
| Menjaga efisiensi stok | Nilai persediaan, umur stok, stok berisiko, kekurangan stok, kerugian pelepasan stok | Batas modal dan toleransi belum ditetapkan |
| Menjaga profitabilitas | Estimasi dan aktual margin per order/pelanggan, kelengkapan biaya | Kebijakan biaya dan pengakuan omzet perlu ditetapkan |
| Meningkatkan kemandirian | Hambatan dengan PIC/tindakan, kelengkapan serah-terima, intervensi pemilik yang tercatat | Cara pencatatan dan baseline perlu disepakati |

Keberhasilan tidak dinilai dari same-day saja. Perbaikan pengiriman harus dibaca bersama persediaan, kapasitas/lembur, kualitas, dan margin. Tidak menetapkan target persentase tanpa baseline yang konsisten.

## 5. Keputusan pemilik yang disepakati

| ID | Keputusan |
|---|---|
| D01 | Cakupan hanya operasional internal NCK; Awan adalah pelanggan |
| D02 | BigSeller tetap sumber resmi stok pada tahap awal |
| D03 | Admin berwenang menyetujui restock, perubahan prioritas produksi, pengalihan stok eksklusif, dan diskon dead stock |
| D04 | Urutan masuk order menjadi prioritas dasar; deadline pickup menjadi pertimbangan |
| D05 | Aplikasi mendukung shared stock dan exclusive stock |
| D06 | Setiap divisi memperbarui pekerjaan melalui komputer bersama dengan identitas pencatat |
| D07 | Rekomendasi stok membantu keputusan internal; tidak otomatis mengeksekusi restock |
| D08 | Pengembangan dilakukan bertahap; saat ini hanya perencanaan |

Interpretasi operasional D04 yang diusulkan: alokasi mendahulukan order valid paling awal; pekerjaan siap dapat berjalan saat order sebelumnya terhambat; paket lengkap dapat dikirim pada pickup terdekat. Admin mencatat alasan penyimpangan prioritas. Definisi waktu antrean untuk order yang baru dilengkapi perlu difinalkan.

## 6. Pemangku kepentingan dan tanggung jawab

| Peran | Tanggung jawab |
|---|---|
| Pemilik/manajemen | Tujuan bisnis, kebijakan, evaluasi hasil, keputusan pengecualian di luar kewenangan yang ditetapkan |
| Admin | Validasi order, prioritas, persetujuan restock/pengalihan eksklusif/diskon, koordinasi pengiriman |
| PPIC/Gudang | Usulan rencana produksi dan stok, ketersediaan, mutasi, opname, rekonsiliasi |
| Desain | Kesiapan dan versi desain; PIC aktual perlu dikonfirmasi |
| Printing/Press | Penerimaan pekerjaan, hasil parsial, reject/rework, hambatan, serah-terima |
| Picker/QC/Packing | Pengambilan, hasil pemeriksaan, kelengkapan paket, kesiapan pengiriman |
| Koordinator vendor | Serah-terima keluar/kembali, kapasitas yang dijadwalkan, keterlambatan; jabatan aktual perlu dikonfirmasi |
| Finance | Kebijakan biaya, transaksi, rekonsiliasi, validasi margin; pengguna aktual perlu dikonfirmasi |

Kewenangan admin tidak menghapus ketentuan kontrak seller. Hak penggunaan stok eksklusif, kepemilikan ekonomis, pembayaran, dan penanggung risiko perlu dicatat terpisah.

## 7. Cakupan bertahap

### Tahap fondasi

Pemetaan master SKU dan seller, audit sampel histori, definisi metrik, observasi cutting/transfer, validasi kapasitas, pembagian PIC, serta pemeriksaan mekanisme integrasi BigSeller. Tidak menganggap API tersedia sebelum diperiksa.

### Versi pertama: kendali pemenuhan dan keputusan stok dasar

Order per item; alokasi shared/exclusive; antrean dan progres parsial; serah-terima vendor; QC; pickup; hambatan/PIC; rekomendasi stok dengan alasan; persetujuan admin; dashboard harian; biaya standar dan estimasi margin; rekonsiliasi stok dan jejak perubahan.

### Versi berikutnya: akurasi biaya dan perencanaan

Pemakaian bahan lebih rinci, biaya aktual, invoice/pembayaran/piutang/utang sesuai desain finance, analisis umur stok lebih lengkap, evaluasi forecast, dan estimasi proses berbasis realisasi.

### Pengembangan pertumbuhan

CRM B2B, pipeline/follow-up, marketing dan views, atribusi lead/order, OKR, simulasi kapasitas, dan AI rekomendasi lebih lanjut. Modul ini tetap dalam visi produk; kedalamannya tidak dipaksakan masuk versi pertama.

Di luar versi pertama: portal seller, operasional Awan, penggantian penuh BigSeller, pembukuan formal lengkap, payroll, pembelian/diskon otomatis, dan janji same-day untuk semua jenis produk.

## 8. Risiko dan pengendalian rancangan

| Risiko | Respons yang direncanakan |
|---|---|
| Selisih antara alokasi aplikasi dan stok BigSeller | Tetapkan batas sumber data, rekonsiliasi, umur snapshot, serta penanganan transaksi ganda sebelum operasional |
| Forecast menganggap penjualan rendah sebagai permintaan rendah saat stockout | Gunakan order/pending bila tersedia; tandai histori yang tidak lengkap |
| Kapasitas ideal dianggap kapasitas aktual | Tampilkan asumsi, antrean, downtime, dan hasil observasi |
| Restock menggeser order pelanggan | Satu rencana kapasitas untuk order aktual dan restock |
| Shared stock menimbulkan perebutan seller | Alokasi terurut, riwayat, dan persetujuan perubahan |
| Admin menjadi bottleneck persetujuan baru | Pantau antrean keputusan; backup/delegasi belum ditetapkan |
| KPI salah atribusi pada komputer bersama | Pisahkan pencatat dari pelaksana; simpan riwayat koreksi |
| Same-day naik tetapi biaya/stok memburuk | Evaluasi layanan, persediaan, biaya, dan kualitas bersama |

## 9. Syarat kesiapan pilot dan evaluasi

- Cakupan seller/SKU pilot dipilih pemilik; tidak mengasumsikan seluruh operasi dipindahkan sekaligus.
- Master data dan sampel transaksi dapat direkonsiliasi dengan sumber asal.
- Skenario penerimaan PRD lolos, termasuk alokasi stok terakhir, impor ulang, produksi parsial, dan stok eksklusif.
- Pengguna per divisi dapat melakukan pekerjaan inti di komputer bersama.
- Estimasi dan rekomendasi dibandingkan terlebih dahulu dengan keputusan aktual tanpa otomatis menjalankan tindakan.
- Evaluasi baseline dan hasil memakai definisi/periode sebanding. Lama pilot, target angka, pemilik evaluasi, dan kriteria perluasan ditentukan sebelum pilot.

## 10. Keputusan yang masih terbuka

1. Mekanisme dan frekuensi sinkronisasi BigSeller; lokasi pencatatan reservasi dan mutasi.
2. Kapasitas cutting, kalender kerja/vendor, minimum transfer, waktu transport/QC/packing.
3. Jam cut-off, perlakuan pembatalan, order tidak lengkap, dan perubahan setelah validasi.
4. Standar biaya, pengakuan omzet, dan cakupan finance versi pertama.
5. Hak stok eksklusif, penanggung risiko, dan batas kewenangan berdasarkan kontrak.
6. Batas modal stok, ambang peringatan, target layanan, dan target pilot.
7. PIC desain/vendor/finance dan pengganti admin bila tidak tersedia.

## 11. Referensi dan prioritas sumber

Keputusan terbaru pemilik dalam percakapan mengungguli catatan historis. Sumber dokumen:

- [Detail alur operasional](</Users/ademuhamadfaisal/.codex/attachments/5051d7e1-ff3a-4e43-bff7-8fb15ae9e232/Teks tempel.txt>)
- [Klarifikasi teknis](</Users/ademuhamadfaisal/.codex/attachments/ae3a9480-de6f-4840-875f-2d0f6ea60e31/Teks tempel.txt>)
- [Kapasitas, pending, QC](</Users/ademuhamadfaisal/Desktop/OBSIDIAN FAISAL/wiki/topics/Kapasitas Pending dan QC NCK.md>)
- [Sistem data dan laporan](</Users/ademuhamadfaisal/Desktop/OBSIDIAN FAISAL/wiki/topics/Sistem Data dan Laporan NCK.md>)
- [Harga dan keuangan](</Users/ademuhamadfaisal/Desktop/OBSIDIAN FAISAL/wiki/topics/Harga dan Keuangan Internal NCK.md>)

Sumber lokal ini adalah laporan/konteks bisnis, bukan audit transaksi atau pemeriksaan integrasi yang sudah selesai.

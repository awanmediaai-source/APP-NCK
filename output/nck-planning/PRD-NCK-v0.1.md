# PRD — NCK Operations Control Center

Versi: 0.1 · Tanggal: 1 November 2026 (Asia/Jakarta)

Status: usulan produk untuk review, belum implementasi. Dibaca bersama [BRD-NCK-v0.1.md](BRD-NCK-v0.1.md). Rincian teknis integrasi dan aturan yang ditandai terbuka harus difinalkan sebelum fitur terkait dioperasikan.

## 1. Visi dan prinsip produk

Satu aplikasi internal tempat tim NCK mengetahui pekerjaan berikutnya, stok yang benar-benar dapat dipakai, risiko keterlambatan, dan keputusan yang diperlukan. Manajemen dapat menelusuri angka dashboard sampai transaksi dan aktivitas sumbernya.

Prinsip:

1. Kecepatan pengiriman dan risiko stok dinilai bersama.
2. Satu paket siap kirim hanya jika semua item lengkap dan lolos pemeriksaan.
3. Stok fisik, reservasi, produksi berjalan, reject, dan stok vendor tidak dicampur sebagai stok siap jual.
4. Hasil parsial dapat mengalir ke tahap berikutnya tanpa menunggu seluruh batch.
5. Angka tidak tersedia ditampilkan sebagai belum tersedia, bukan nol.
6. Estimasi menyertakan sumber, asumsi, dan waktu pembaruan; bukan janji otomatis kepada seller.
7. Input divisi dibuat singkat dan menghasilkan laporan tanpa rekap ulang.

## 2. Pengguna dan pekerjaan utama

| Pengguna | Kebutuhan |
|---|---|
| Admin | Validasi order, lihat kekurangan, tentukan pengecualian, setujui rekomendasi, pantau paket |
| PPIC/Gudang | Lihat kebutuhan nyata, alokasi, produksi berjalan, rencana restock, dan selisih stok |
| Printing/Press | Lihat antrean yang siap, mulai kerja, laporkan hasil/hambatan, serahkan hasil |
| Picker/QC/Packing | Ambil barang benar, catat hasil QC, lengkapi paket, siapkan pickup |
| Koordinator vendor | Catat pekerjaan keluar/kembali dan keterlambatan |
| Manajemen | Pantau layanan, persediaan, estimasi/aktual margin, dan masalah dengan PIC |
| Finance | Periksa sumber angka biaya/pendapatan; cakupan transaksi rinci masih terbuka |

## 3. Struktur tampilan

- **Ringkasan NCK:** paket/pcs hari ini, pending dan umurnya, pickup, risiko stok, antrean hambatan, keuangan berlabel estimasi/aktual.
- **Order & Pengiriman:** daftar per seller/usia/status, detail item, alokasi, riwayat, estimasi, bukti serah-terima.
- **Pekerjaan Divisi:** antrean siap, pekerjaan aktif, hasil parsial, tombol mulai/selesai sebagian/terhambat/serahkan.
- **Produksi & Vendor:** pekerjaan order/restock, tahapan, jumlah WIP, kirim/kembali vendor.
- **Stok & PPIC:** stok sumber, reservasi, eksklusivitas, kekurangan, usulan restock, risiko stok mati, rekonsiliasi.
- **Keputusan Admin:** usulan, dampak pada order/kapasitas/modal, setujui/tolak/ubah dengan alasan.
- **Laporan & Pengaturan:** definisi metrik, master, kapasitas, kalender, hak akses, audit.

AI ringkasan dapat ditempatkan pada dashboard setelah sumber angka tervalidasi; keberadaannya tidak menjadi penghalang fungsi operasional inti.

## 4. Objek data konseptual

| Objek | Isi minimum |
|---|---|
| Pelanggan B2B | ID, nama, ketentuan stok/layanan yang relevan |
| Produk/varian | ID SKU baku, desain/versi, ukuran, kategori, satuan, status aktif |
| Order/paket/item | ID internal, ID sumber, seller, resi dan riwayatnya, waktu diterima/valid, SKU, jumlah, status |
| Kelompok stok | SKU, lokasi, kelayakan jual, shared/exclusive, seller yang berhak, kepemilikan/risiko bila diketahui |
| Reservasi | Order/item, kelompok stok, jumlah, status, waktu, alasan pelepasan/perubahan |
| Pekerjaan produksi | Untuk order/restock, SKU, jumlah, rute, prioritas, sumber kebutuhan |
| Aktivitas tahap | Masuk, mulai, hasil baik, reject/rework, transfer, hambatan, pencatat, pelaksana, waktu |
| Pekerjaan vendor | Vendor, jumlah keluar/diterima, estimasi kembali, jumlah kembali/hasil QC, sisa, waktu |
| Pickup/pengiriman | Jadwal, konfirmasi, paket, waktu serah-terima, bukti |
| Rekomendasi/keputusan | Versi data, asumsi, usulan, dampak, pembuat, keputusan admin, alasan |
| Biaya | Standar/aktual, versi berlaku, komponen, order/SKU, kelengkapan |
| Sinkronisasi/audit | Sumber, ID eksternal, waktu data, hasil, selisih, perubahan dan aktor |

Ini model konseptual, bukan keputusan database. Satu batch produksi dapat memenuhi beberapa order; satu item order dapat dipenuhi dari beberapa hasil produksi/stok. Relasi alokasi harus mencegah hitung ganda.

## 5. Persyaratan fungsional versi pertama

### F01 — Penerimaan dan validasi order

- Terima data dari mekanisme yang ditetapkan setelah audit sumber; impor terkontrol dapat menjadi tahap awal.
- Simpan identitas sumber agar pengulangan input tidak membuat order baru.
- Pisahkan waktu order diterima dan waktu data lengkap/valid.
- Validasi seller, SKU/ukuran/jumlah, informasi pengiriman, serta kebutuhan desain.
- Resi bukan satu-satunya identitas internal; perubahan/cetak ulang memiliki riwayat.
- Order tidak lengkap masuk antrean koreksi, bukan diam-diam dianggap siap produksi.
- Pembatalan/perubahan melepaskan atau menghitung ulang reservasi. Barang yang telanjur diproduksi tetap tercatat dan memerlukan keputusan, bukan dihapus.

### F02 — Stok dan reservasi

- BigSeller menjadi sumber resmi stok fisik pada tahap awal.
- Aplikasi menampilkan sumber dan waktu snapshot; batas umur data yang dapat dipakai untuk komitmen harus ditentukan sebelum pilot.
- Stok eksklusif tidak dapat dialokasikan ke seller lain tanpa keputusan admin sesuai kesepakatan.
- Usulan dasar: stok yang dapat dialokasikan = stok layak jual yang sesuai hak seller dikurangi komitmen yang belum tercermin pada angka sumber.
- Jika data sumber sudah mengurangi reservasi, sistem tidak menguranginya lagi. Definisi tiap field sumber wajib dipetakan dahulu.
- Alokasi bersamaan tidak boleh menggunakan unit terakhir dua kali.
- Stok negatif/selisih/snapshot usang menjadi pengecualian untuk pemeriksaan, bukan ditutup dengan angka buatan.

### F03 — Prioritas dan rencana kerja

- Urutan masuk order menjadi aturan dasar; timestamp urutan setelah koreksi data perlu difinalkan.
- Order siap diproses boleh berjalan ketika order sebelumnya terhambat.
- Tampilkan sisa tahap, pickup, umur pending, kesiapan desain/bahan, dan item yang melengkapi paket.
- Restock dan order pelanggan menggunakan rencana kapasitas yang sama.
- Admin dapat mengubah prioritas; wajib ada alasan dan riwayat. Tampilkan dampak terhadap order yang bergeser bila dapat dihitung.
- Sistem menandai order lama yang terus terlewat; ambang eskalasi belum ditetapkan.

### F04 — Progres parsial dan QC

- Divisi mencatat jumlah diterima, mulai, selesai baik, reject/rework, dan diserahkan.
- Tahap berikutnya dapat menerima sebagian hasil. Tidak menyamakan selesai dengan sudah diserahkan.
- Kuantitas yang keluar dari tahap tidak boleh melebihi kuantitas yang tersedia tanpa koreksi berwenang.
- Reject dipisahkan dari barang baik; rework mempertahankan hubungan ke pekerjaan asal agar tidak dihitung sebagai output jual tambahan.
- Rute barang jadi, DTF, dan jersey berbeda. Produk yang membutuhkan desain ditahan sampai desain siap.
- Pelaksana dapat berupa tim; pencatat bukan otomatis orang yang mengerjakan seluruh jumlah.

### F05 — Vendor

- Catat jumlah/waktu keluar, penerimaan vendor bila tersedia, estimasi kembali, dan pengembalian parsial.
- Gunakan ±300 pcs/hari serta ±24 jam sebagai parameter awal yang dapat diperbarui, bukan jaminan penyelesaian.
- Kalender kerja, antrean yang telah dijadwalkan, transport, dan keterlambatan memengaruhi estimasi.
- Barang di vendor bukan ready stock. Barang kembali melewati QC sesuai aturan produk.
- Batas pencatatan cutting dan jahit perlu disepakati agar proses tidak terhitung dua kali atau hilang.

### F06 — Estimasi dan pengiriman

- Hitung estimasi per item lalu paket mengikuti item terakhir siap ditambah waktu QC/packing yang belum dijalani.
- Pilih pickup yang tersedia setelah paket diperkirakan siap; pickup 18.00 bersifat kondisional sampai dikonfirmasi.
- Status estimasi: dapat diperkirakan, berisiko, menunggu konfirmasi, atau data belum cukup.
- Kapasitas cutting/transfer yang belum terukur tidak diganti angka rekaan; PPIC dapat memasukkan estimasi manual dengan alasan.
- Paket hanya siap jika semua item lengkap dan lolos QC. Split shipment bukan alur default versi pertama.
- Resi tercetak, siap kirim, dan diserahkan kepada ekspedisi memiliki waktu berbeda.
- Estimasi yang dimaksud adalah pengiriman dari NCK, bukan waktu tiba di penerima.

### F07 — Rekomendasi stok dan dead stock

- Review rutin Rabu, menggunakan histori tujuh hari dengan pembanding periode lebih panjang bila tersedia.
- Kategori awal: stabil, naik/viral, baru, menurun, dan jarang/custom; aturan klasifikasi masih perlu dikalibrasi.
- Tampilkan kebutuhan selama replenishment dan sampai review berikutnya, pending, reservasi, stok siap, dan produksi yang akan selesai tepat waktu.
- Jangan menghitung pending yang sama dua kali di forecast dan kebutuhan pasti.
- Produksi berjalan yang terlambat tidak dianggap tersedia untuk memenuhi kebutuhan lebih awal.
- Stok baru/viral dapat diberi usulan batch uji dan evaluasi berikutnya; tidak mengklaim jumlah optimal tanpa validasi.
- Tampilkan jumlah/nilai usulan, kapasitas yang diperlukan, risiko sisa, asumsi, dan data yang hilang.
- Permintaan menggunakan order valid bila tersedia, bukan hanya pengiriman. Pembatalan dan stockout perlu dibedakan sesuai kualitas data.
- Mutasi antar lokasi tidak dianggap permintaan pelanggan. Umur stok dan jumlah tersisa tetap diperiksa meski ada satu penjualan kecil.
- Sekitar dua bulan tanpa gerakan penjualan menjadi pemicu evaluasi; definisi formal, peringatan dini, dan batas modal masih terbuka.
- Usulan tidak otomatis menjadi produksi, pembelian, atau diskon sebelum keputusan admin.

### F08 — Dashboard, KPI, dan estimasi margin

- Filter tanggal, seller, kategori, SKU, tahap, dan status.
- Angka dashboard dapat ditelusuri ke daftar paket/item/transaksi pembentuknya.
- Tampilkan waktu data, kelengkapan, dan perbedaan estimasi/aktual.
- Nilai order dibedakan dari omzet yang diakui, invoice, dan kas masuk. Jangan menampilkan salah satunya sebagai pengganti yang lain tanpa label.
- Versi pertama mendukung harga jual order dan biaya standar berversi untuk estimasi margin; biaya tidak lengkap ditandai.
- Estimasi margin = nilai penjualan neto yang relevan dikurangi biaya standar yang dicakup, dengan komponen/cakupan terlihat. Tidak diberi label laba bersih.
- Margin aktual, pengakuan omzet, biaya bersama, ongkir, retur, diskon, dan biaya rework memerlukan kebijakan finance sebelum menjadi laporan final.
- KPI divisi menampilkan output baik, reject/rework, antrean, dan hambatan; jangan menilai individu berdasarkan jumlah pcs semata.

### F09 — Persetujuan dan akses

- Admin menyetujui restock, perubahan prioritas, pengalihan eksklusif, dan diskon dead stock.
- PPIC/divisi dapat membuat usulan atau mencatat pekerjaan sesuai peran; tidak otomatis mendapatkan kewenangan admin.
- Komputer bersama mendukung pergantian identitas pencatat yang ringan tetapi terautentikasi; metode final di TRD.
- Riwayat koreksi mencatat nilai sebelum/sesudah, waktu, alasan, dan aktor.
- Data pelanggan dan biaya dibatasi sesuai kebutuhan peran; akses finance/manajemen dirinci sebelum pilot.
- Diskon di aplikasi pada versi pertama merupakan keputusan tercatat; tidak otomatis mengubah harga di kanal eksternal.

### F10 — AI pendukung

- Ringkasan dan rekomendasi merujuk data yang dapat dibuka kembali, lengkap dengan waktu dan asumsi.
- Perhitungan jumlah, stok, dan KPI dilakukan oleh aturan sistem yang dapat diuji; AI membantu menjelaskan dan membandingkan opsi.
- AI tidak otomatis mengubah stok, harga, prioritas, atau mengirim pesan kepada seller/vendor.
- Jika data kurang, jelaskan bagian yang belum diketahui. Operasional inti tetap berjalan saat AI tidak tersedia.

## 6. Status konseptual

Jangan gunakan satu status untuk mewakili seluruh kondisi. Pisahkan:

- **Order:** perlu validasi / valid / dibatalkan / ditutup.
- **Pemenuhan item:** belum dialokasikan / dialokasikan sebagian / dialokasikan penuh / produksi / siap.
- **Tahap kerja:** menunggu kesiapan / siap / dikerjakan / selesai sebagian / selesai / terhambat.
- **Pengiriman paket:** belum lengkap / QC-packing / siap kirim / diserahkan ke ekspedisi.
- **Reservasi:** aktif / dilepas / digunakan.

Daftar status final dan transisi menjadi bagian FRD. Status paket dihasilkan dari fakta item dan kejadian pengiriman; tidak sekadar dipilih bebas.

## 7. Kontrak metrik awal

Semua waktu bisnis memakai Asia/Jakarta. Definisi berikut usulan untuk review.

| Metrik | Definisi awal dan batasnya |
|---|---|
| Order masuk | Jumlah paket unik berdasarkan tanggal diterima; order tidak valid dan batal ditampilkan terpisah |
| Same-day paket | Paket dari cohort tanggal masuk yang diserahkan hari yang sama ÷ paket cohort yang masuk cakupan perhitungan; perlakuan batal perlu disahkan dan jumlah mentah tetap terlihat |
| Same-day pcs | Pcs dalam cohort yang diserahkan hari yang sama ÷ pcs cohort dengan aturan pembatalan yang sama |
| Pending | Paket/pcs yang belum diserahkan pada cut-off pelaporan; tampilkan total backlog dan pending cohort hari ini secara terpisah |
| Umur pending | Waktu dari penerimaan order ke waktu laporan selama belum dikirim; waktu tunggu validasi dapat ditampilkan terpisah |
| Output baik | Jumlah lolos tahap terkait, tanpa menghitung ulang rework sebagai unit tambahan |
| Risiko stok mati | Stok tersisa dengan indikator tanpa penjualan, umur lot bila tersedia, penurunan permintaan, dan cakupan stok berlebih |
| Kinerja vendor | Jumlah dijanjikan/kembali, waktu keluar/kembali, keterlambatan terhadap estimasi yang tersimpan, dan hasil QC |

Jika kemudian ada layanan same-day eligible, laporkan kinerjanya terpisah dari seluruh order. Jangan menyembunyikan jersey MTO/desain baru hanya untuk memperbaiki persentase total.

## 8. Integrasi dan migrasi: batas yang wajib diselesaikan

BigSeller adalah sumber resmi stok, Sheets/n8n adalah sumber historis/input yang perlu diperiksa. Belum ada klaim API, koneksi, atau sinkronisasi aktif.

Sebelum pilot, petakan untuk setiap jenis data: tempat membuat/mengubah, ID unik, waktu efektif, cara sinkronisasi, penanganan gagal/ulang, dan penanggung jawab rekonsiliasi.

Khusus reservasi: tentukan apakah reservasi dicatat di BigSeller atau lapisan aplikasi, dan bagaimana transaksi di luar aplikasi terlihat. Penguncian di aplikasi saja tidak menjamin stok aman apabila sumber eksternal berubah tanpa pembaruan. Bila sinkronisasi belum memadai, alokasi bersifat sementara dan perlu konfirmasi stok oleh PIC sebelum komitmen.

Migrasi histori mempertahankan sumber dan kualitas data; jangan mengarang waktu proses yang tidak pernah tercatat. Audit sampel harus mendeteksi SKU tidak cocok, order ganda, status kosong, dan jumlah yang berbeda.

## 9. Kebutuhan nonfungsional

- Tampilan desktop sederhana untuk perangkat bersama; operasi inti tidak bergantung pada chat AI.
- Pembaruan input sendiri segera terlihat setelah tersimpan; data integrasi menampilkan umur snapshot. Target latensi numerik ditentukan setelah mekanisme integrasi diketahui.
- Input ulang setelah gangguan tidak menggandakan hasil produksi atau transaksi.
- Hak akses, sesi pengguna, dan riwayat perubahan wajib ada sebelum pilot.
- Backup dan uji pemulihan harus direncanakan; frekuensi, retensi, RPO/RTO ditentukan di TRD.
- Data dapat diekspor untuk rekonsiliasi dan audit dengan pembatasan akses yang sesuai.
- Beban uji teknis diturunkan dari jumlah order/item, aktivitas, pengguna bersamaan, dan kebutuhan pertumbuhan; bukan hanya target pcs bulanan.
- Gangguan integrasi atau koneksi terlihat jelas. Prosedur pencatatan sementara dan input susulan harus ditetapkan; dukungan offline penuh bukan janji versi pertama.

## 10. Kriteria penerimaan inti

| ID | Skenario | Hasil wajib |
|---|---|---|
| AC01 | Resi/order sumber diimpor dua kali | Satu order; pengulangan tercatat tanpa pengurangan stok ganda |
| AC02 | Dua order meminta stok bersama terakhir | Unit hanya dialokasikan sekali; kebutuhan sisanya terlihat |
| AC03 | Order seller B mencoba stok eksklusif A | Tidak dialokasikan otomatis; perubahan hanya oleh admin dengan alasan dan ketentuan yang sesuai |
| AC04 | Paket berisi tiga SKU, satu belum siap | Paket tidak dapat dinyatakan siap kirim |
| AC05 | Printing menyelesaikan sebagian batch | Hasil baik parsial dapat diserahkan; sisa tetap terlacak |
| AC06 | Vendor mengembalikan sebagian dan ada reject | Jumlah baik, reject, serta sisa vendor cocok dengan histori keluar/kembali |
| AC07 | Order lebih awal terhambat desain | Order siap berikutnya dapat berjalan; order awal tetap terlihat beserta alasan/PIC |
| AC08 | Estimasi mengandalkan pickup 18.00 belum dikonfirmasi | Ditampilkan kondisional, bukan jadwal pasti |
| AC09 | Cutting belum terukur | Sistem tidak membuat durasi palsu; estimasi diberi keterbatasan/konfirmasi manual |
| AC10 | Permintaan SKU melambat saat restock berjalan | Usulan evaluasi muncul tanpa otomatis membatalkan pekerjaan |
| AC11 | Order batal setelah reservasi/produksi | Reservasi disesuaikan; barang yang telanjur diproduksi tetap tercatat |
| AC12 | Data stok eksternal usang atau berselisih | Sumber/umur/selisih terlihat; konfirmasi mengikuti kebijakan yang disetujui |
| AC13 | Biaya order belum lengkap | Margin diberi label estimasi/tidak lengkap; tidak tampil sebagai laba bersih |
| AC14 | Operator mencatat pekerjaan tim | Identitas pencatat dan pelaksana tidak disamakan otomatis |
| AC15 | Paket baru dicetak resinya | Belum dihitung terkirim tanpa kejadian serah-terima ekspedisi |

## 11. Validasi rekomendasi dan peluncuran bertahap

1. Audit histori sejak Mei 2026; tentukan bagian yang layak dipakai dan keterbatasannya.
2. Bandingkan rekomendasi dengan praktik review Rabu/penjualan tujuh hari menggunakan urutan waktu. Jangan menggunakan data masa depan untuk keputusan masa lalu.
3. Jika histori stok atau kejadian stockout tidak tersedia, jangan mengklaim simulasi pending/dead stock akurat; lakukan pengamatan prospektif.
4. Jalankan rekomendasi sebagai pembanding keputusan manual terlebih dahulu. Catat usulan, keputusan admin, alasan, serta realisasi.
5. Pilot pada cakupan yang disetujui. Nilai pengiriman, stok, biaya, kualitas, dan beban input tim bersama.
6. Perluas setelah rekonsiliasi dan skenario penerimaan berhasil; target angka serta durasi pilot ditetapkan terpisah.

## 12. Tahap dokumen berikutnya

FRD merinci transisi status, rumus, validasi input, matriks hak akses, pengecualian, dan pemetaan kriteria penerimaan. TRD dibuat setelah sumber data/integrasi diperiksa, mencakup arsitektur, skema, mekanisme sinkronisasi, keamanan, backup, dan pengujian kapasitas. Belum ada teknologi yang dikunci pada versi ini.

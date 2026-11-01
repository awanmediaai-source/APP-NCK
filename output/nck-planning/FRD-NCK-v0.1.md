# FRD — NCK Operations Control Center

Functional Requirements Document · Versi 0.1 · 1 November 2026 · Asia/Jakarta

**Status: draft untuk review, belum persetujuan coding atau pengoperasian.**

Dokumen induk: [BRD v0.1](BRD-NCK-v0.1.md) dan [PRD v0.1](PRD-NCK-v0.1.md). FRD ini merinci perilaku yang dapat diuji tanpa mengunci framework, database, atau kemampuan API BigSeller. Keputusan pemilik dalam BRD tetap berlaku.

## 1. Cakupan dan cara membaca

Prioritas versi pertama: order sampai pengiriman, alokasi stok, produksi parsial, vendor, rekomendasi stok dasar, persetujuan admin, KPI operasional, serta estimasi margin. AI penjelasan merupakan pendukung dan bukan prasyarat operasional.

Penanda aturan:

- **Disepakati:** keputusan eksplisit pemilik, terutama cakupan internal NCK, BigSeller sebagai sumber resmi stok, kewenangan admin, shared/exclusive stock, dan prioritas urutan order masuk.
- **Usulan:** rincian perilaku dalam FRD ini, untuk direview sebelum implementasi terkait.
- **TBD:** membutuhkan keputusan/data; tidak boleh diam-diam diberi angka/default bisnis. Daftar dan dampaknya ada di bagian 17.

Kecuali disebut disepakati, rincian baru adalah usulan. Contoh angka pengujian merupakan data sintetis, bukan kapasitas atau kebijakan NCK.

Di luar versi pertama: portal seller, pembukuan formal lengkap, payroll, CRM/marketing/OKR lengkap, optimasi otomatis tanpa persetujuan, penggantian penuh BigSeller, split shipment standar, dan estimasi tiba di alamat penerima.

## 2. Kontrak umum data dan transaksi — FR-00

### FR-00.1 Identitas dan waktu

- Setiap order, paket, item, pekerjaan, transfer, reservasi, dan keputusan memiliki ID internal tetap. Nomor resi dapat berubah tanpa mengganti identitas order.
- Waktu bisnis ditampilkan dalam Asia/Jakarta. Simpan waktu kejadian dan waktu pencatatan secara terpisah untuk input terlambat.
- Waktu order diterima dari sumber, waktu diterima aplikasi, dan waktu validasi tidak disamakan. Sumber waktu antrean mengikuti TBD-02.
- Input historis boleh memiliki field kosong jika memang tidak tercatat; UI menampilkan “belum tersedia”. Jangan mengisi waktu produksi dari waktu impor.
- Kuantitas produk jadi/WIP dalam pcs berupa bilangan bulat positif pada transaksi masuk/keluar. Saldo boleh nol; koreksi menggunakan transaksi pembalik/penyesuaian beralasan, bukan input kuantitas negatif sembarang.
- Bahan dapat memakai satuan lain. Konversi bahan ke pcs memerlukan satuan dan aturan yang ditetapkan, bukan asumsi satu banding satu.

### FR-00.2 Penyimpanan dan koreksi

- Klik ulang, retry koneksi, atau impor ulang kejadian yang sama menghasilkan satu efek bisnis.
- Jika data berubah sejak form dibuka, tampilkan konflik dan minta pengguna memuat ulang sebelum menyimpan keputusan yang memakai saldo/versi lama.
- Simpan aktor, peran, pencatat, pelaksana bila relevan, waktu, sumber, alasan, serta nilai sebelum/sesudah.
- Koreksi kejadian yang sudah dipakai tahap berikutnya tidak boleh menghilangkan barang/riwayat. Tampilkan dampak, buat penyesuaian berwenang, dan hitung ulang status/estimasi terkait.
- Data gagal validasi tidak membuat transaksi parsial tersembunyi. Untuk impor banyak baris, tampilkan hasil per order; satu order multi-item hanya dipromosikan sebagai valid setelah seluruh itemnya konsisten.
- Transaksi bisnis yang sudah berjalan tidak dihapus permanen melalui layar operasional.

## 3. Aktor dan matriks akses — FR-09

Disepakati: **admin menyetujui restock, perubahan prioritas, pengalihan stok eksklusif, dan diskon dead stock.** Tidak diperlukan persetujuan pemilik kedua untuk empat tindakan tersebut. Sistem tetap memeriksa ketentuan seller yang berlaku.

Matriks berikut usulan; peran dapat dirangkap orang yang sama dengan hak eksplisit.

| Fungsi | Admin | PPIC/Gudang | Divisi produksi | Picker/QC/Packing | Koordinator vendor | Finance | Manajemen |
|---|---|---|---|---|---|---|---|
| Validasi/koreksi order | Kelola | Baca kebutuhan | Baca kebutuhan kerja | Baca paket terkait | Baca pekerjaan terkait | Baca nilai | Baca |
| Alokasi sesuai aturan stok | Kelola | Kelola | Baca terkait | Baca terkait | — | — | Baca |
| Usul restock/prioritas | Usul & putuskan | Usul | Usul hambatan | Usul hambatan | Usul hambatan | Baca biaya sesuai hak | Baca |
| Alih eksklusif/diskon | Putuskan | Usul | — | — | — | Baca sesuai hak | Baca |
| Hasil/transfer produksi | Baca; koreksi berwenang | Baca/rencanakan | Catat tahap sendiri | Catat tahap sendiri | Catat vendor | — | Baca |
| Vendor keluar/kembali | Baca | Baca/rencanakan | Baca terkait | Catat QC kembali | Catat | Baca biaya | Baca |
| Paket/pickup/handover | Kelola | Baca | Baca terkait | Catat | — | Baca | Baca |
| Biaya standar/laporan margin | Baca | Nilai usulan sesuai hak | — | — | — | Kelola | Baca |
| Audit/rekonsiliasi | Operasional | Stok | Riwayat sendiri | Riwayat sendiri | Riwayat sendiri | Keuangan | Baca lintas fungsi |

Pengelolaan akun/konfigurasi ditugaskan kepada pengelola sistem yang ditunjuk pemilik; penunjukan ini tidak otomatis memberi kewenangan bisnis admin. PIC finance, desain, vendor, pengganti admin, serta persetujuan koreksi saldo final masih TBD-07/TBD-08.

Pada komputer bersama:

1. Pengguna memilih/masuk identitas terautentikasi; metode autentikasi di TRD.
2. Identitas aktif terlihat sebelum konfirmasi transaksi.
3. Pelaksana dapat berbeda dari pencatat dan dapat berupa tim.
4. Pergantian pengguna tidak mewariskan hak pengguna sebelumnya.
5. Pembatasan berlaku juga pada pencarian, ekspor, unduhan, dan jawaban AI, bukan hanya menu.

## 4. Master dan formulir minimum

| Form/objek | Field wajib untuk digunakan | Validasi utama |
|---|---|---|
| Seller | ID, nama, status | ID unik; seller nonaktif tidak untuk order baru tanpa aktivasi |
| SKU | ID baku, kategori, ukuran/varian, satuan, rute/versi | Alias sumber dipetakan ke satu SKU; SKU ambigu masuk koreksi |
| Desain | ID/versi, SKU terkait, status kesiapan, pencatat konfirmasi | Desain baru tidak dianggap siap hanya karena file ada |
| Order/paket | ID sumber jika impor, seller, waktu/sumber penerimaan, identitas paket/resi, ekspedisi, informasi kirim yang diperlukan | Resi teks mempertahankan nol awal; konflik ditinjau, tidak digabung otomatis |
| Item | ID baris, SKU, jumlah, kebutuhan desain | Jumlah >0; seluruh item harus dikenal sebelum order valid |
| Pool stok | SKU, lokasi, shared/exclusive, hak seller, kondisi layak jual | Eksklusif wajib seller; kepemilikan ekonomis boleh belum diketahui tetapi ditandai |
| Hasil tahap | Pekerjaan, tahap, jumlah baik/hold/scrap, waktu, pencatat, pelaksana | Total keluaran tidak melebihi jumlah yang diproses |
| Transfer | Asal/tujuan, SKU/pekerjaan, jumlah, waktu keluar, pengirim | Penerimaan terpisah; perbedaan jumlah menjadi kasus selisih |
| Vendor | ID, pekerjaan/transfer, jumlah keluar/kembali, estimasi, waktu kejadian | Kembali tidak melebihi sisa yang dipertanggungjawabkan tanpa koreksi |
| Handover | Paket, pickup/ekspedisi, waktu aktual, pencatat, bukti/referensi | Paket lengkap, lolos QC, dikemas, belum diserahkan sebelumnya |
| Keputusan | Jenis, objek/versi, usulan, dampak, alasan, admin | Tidak menyetujui data usang tanpa evaluasi ulang |

Harga/biaya yang belum tersedia tidak menghalangi pencatatan produksi, tetapi menghalangi penyajian margin sebagai lengkap. Rincian data pribadi penerima mengikuti kebutuhan picking/label/pengiriman, bukan dibuka ke seluruh divisi.

## 5. Order, perubahan, dan pembatalan — FR-01

### FR-01.1 Penerimaan dan deduplikasi

Alur: terima/impor → periksa sumber dan duplikasi → petakan seller/SKU → validasi seluruh item → tandai valid → periksa stok dan kebutuhan produksi.

- Kunci deduplikasi utama: sistem sumber + ID order/paket sumber yang stabil; pemetaan disahkan pada audit integrasi.
- Resi sama dengan data sama dianggap kandidat pengulangan. Resi sama dengan seller/item berbeda ditahan untuk tinjauan, bukan ditimpa.
- Bila sumber tidak menyediakan ID stabil, buat batch impor/ID baris dan tampilkan kandidat duplikat berdasarkan seller, resi, dan isi; keputusan penggabungan oleh admin dengan audit.
- Resi cetak ulang tidak membuat order baru. Penggantian resi menyimpan riwayat dan menandai resi aktif.
- Impor ulang dengan isi berubah menjadi usulan revisi, bukan overwrite order yang sudah berjalan.

### FR-01.2 Validasi

Admin melihat seluruh kesalahan per order: seller tidak dikenal, SKU ambigu, jumlah tidak valid, informasi pengiriman kurang, atau kebutuhan desain belum ditentukan. Data order dapat valid meski desain belum siap; kondisi desain menahan kesiapan produksi, bukan menyembunyikan order dari laporan masuk.

### FR-01.3 Revisi dan pembatalan

- Sebelum pekerjaan berjalan: admin merevisi, memvalidasi ulang, dan menghitung ulang alokasi/kebutuhan.
- Sesudah berjalan: tampilkan jumlah teralokasi, WIP, selesai, dan biaya potensial; revisi menghasilkan penyesuaian, bukan menghapus kejadian lama.
- Batal sebelum handover: hentikan kebutuhan order yang belum dikerjakan, lepaskan reservasi yang aman dilepas, tandai WIP/hasil jadi untuk keputusan admin. Pekerjaan gabungan bagi order lain tetap berjalan.
- Barang sudah dipicking harus dikembalikan/ditinjau sebelum kembali menjadi stok tersedia; pembatalan tidak otomatis mengubah lokasi fisiknya.
- Sesudah handover: tidak boleh membatalkan kejadian kirim melalui status order. Catat kasus retur/komplain terpisah; proses retur penuh belum termasuk versi pertama.
- Pembatalan sebagian item memerlukan versi jumlah; kuantitas historis dan alasan tetap tersedia untuk laporan.

## 6. Model status dan transisi

Status tidak digabung menjadi satu kolom besar. Ketersediaan item, status pekerjaan, dan status kirim dapat berbeda pada waktu yang sama.

### 6.1 Order

| Dari → ke | Pemicu/aktor | Syarat dan efek |
|---|---|---|
| Baru → Perlu validasi | Impor/admin | Simpan data sumber, belum komit stok |
| Perlu validasi → Valid | Admin | Semua field wajib order lengkap; desain dapat masih menunggu |
| Valid → Perlu validasi | Revisi admin | Perubahan berdampak ditinjau; pekerjaan aktif diberi tanda evaluasi, bukan dihapus |
| Perlu validasi/Valid → Dibatalkan | Admin | Belum handover; jalankan penyesuaian FR-01.3 |
| Valid → Ditutup | Sistem dari kejadian handover | Seluruh paket aktif telah diserahkan; penutupan operasional tidak berarti pembayaran lunas |

### 6.2 Pemenuhan item

Gunakan kuantitas terpisah: kebutuhan aktif, reserved fisik, dipicking, WIP terhubung, barang baik siap, dan terkirim. Label **belum/parsial/penuh** berasal dari cakupan jumlah, sedangkan **menunggu desain/produksi/vendor/QC** merupakan penanda proses; keduanya boleh tampil bersama. WIP tidak dihitung sebagai ready stock.

### 6.3 Pekerjaan tahap

| Status | Syarat masuk | Tindakan berikutnya |
|---|---|---|
| Menunggu kesiapan | Input/desain/bahan belum tersedia | Terima input atau tandai hambatan |
| Siap | Ada jumlah yang dapat diproses dan prasyarat terpenuhi | Mulai oleh divisi |
| Dikerjakan | Mulai dicatat | Catat hasil parsial/hambatan |
| Selesai sebagian | Sebagian input diselesaikan, masih ada sisa | Transfer hasil baik, lanjutkan sisa |
| Selesai | Semua jumlah yang ditugaskan telah dipertanggungjawabkan | Hasil baik tetap menunggu transfer jika belum diserahkan |

**Terhambat** adalah penanda tambahan dengan jumlah terdampak, alasan, PIC, waktu mulai, dan tindakan berikutnya. Sebagian batch dapat berjalan sementara bagian lain terhambat. Selesai tahap tidak berarti kebutuhan order terpenuhi jika ada scrap; kebutuhan pengganti dibuat terpisah.

### 6.4 Transfer, reservasi, paket, dan persetujuan

- Transfer: disiapkan → dikirim → diterima sebagian/diterima penuh; selisih memiliki kasus tersendiri. Lokasi dalam perjalanan dipisahkan dari asal/tujuan.
- Reservasi: sementara → terkonfirmasi → dipicking → digunakan; sisa yang belum digunakan dapat dilepas. Pemakaian saat handover harus cocok dengan kejadian stok sumber, bukan mengurangi stok dua kali.
- Paket: belum lengkap → QC/packing → siap kirim → diserahkan. Kegagalan QC/koreksi sebelum handover dapat mengembalikan kesiapan; alasan tercatat. Sesudah handover, koreksi melalui kejadian pembalik berwenang bila pencatatan salah, bukan edit bebas.
- Rekomendasi: draft → diajukan → disetujui/ditolak/perlu revisi → dilaksanakan sebagian/penuh. Persetujuan kadaluarsa secara logis jika input material berubah; perlu evaluasi ulang, bukan eksekusi otomatis.

## 7. Persediaan, reservasi, dan rekonsiliasi — FR-02

### FR-02.1 Jenis saldo

UI memisahkan saldo fisik sumber, kondisi layak jual, shared/exclusive, reservasi, sudah dipicking, dalam perjalanan, WIP internal, WIP vendor, dan reject. Satu unit berada pada satu lokasi/kondisi fisik pada suatu waktu; reservasi merupakan hubungan komitmen, bukan stok fisik tambahan.

### FR-02.2 Rumus ketersediaan

Sebelum koneksi produksi, field BigSeller harus dinormalisasi menjadi **B = saldo layak jual sesuai hak seller yang belum mengurangi komitmen mana pun**, pada waktu snapshot tertentu. Jika sumber hanya menyediakan saldo neto, gunakan pemetaan yang membuktikan komitmen mana sudah dikurangi; jangan menambahkan kembali tanpa bukti.

Untuk model saldo bruto tersebut:

`saldo alokasi = B + delta fisik tervalidasi yang belum tercermin di snapshot − komitmen aktif yang belum tercermin dalam perubahan fisik`

- Delta hanya berasal dari kejadian dengan identitas dan status rekonsiliasi yang jelas; bukan tebakan untuk menutup selisih.
- Ketika snapshot baru sudah memuat suatu kejadian, efek lokalnya berhenti diterapkan pada snapshot baru itu.
- Saldo negatif ditampilkan sebagai selisih; jumlah yang boleh dialokasikan maksimal nol sampai diperiksa. Jangan menyembunyikan selisih dengan hanya menampilkan nol.
- Jika bruto/neto/komitmen sumber tidak dapat dipetakan, sistem hanya memberi **alokasi sementara**, memerlukan verifikasi PPIC sebelum komitmen. Tidak mengklaim aman dari overselling eksternal.

### FR-02.3 Alokasi

Prasyarat: order valid, SKU terpetakan, hak seller cocok, sumber stok cukup dapat dipercaya atau telah dikonfirmasi PPIC.

1. Urutkan order sesuai aturan antrean yang disetujui.
2. Periksa pool yang boleh dipakai seller. Usulan: gunakan stok eksklusif seller tersebut lebih dahulu, lalu shared; urutan pool perlu disahkan dalam TBD-05.
3. Alokasikan maksimal kebutuhan aktif yang belum tercakup reservasi fisik.
4. Kekurangan menjadi kebutuhan produksi, dengan pemeriksaan WIP yang sudah dihubungkan agar tidak dibuat dua kali.
5. WIP dapat dialihkan ke order atas keputusan berwenang, tetapi hanya menjadi reservasi barang jadi setelah hasil layak jual tercatat dan direkonsiliasi.

Permintaan bersamaan pada unit terakhir harus menghasilkan satu pemenang sesuai urutan transaksi/antrean; order lain menerima kekurangan, bukan saldo fiktif.

### FR-02.4 Stok eksklusif dan selisih

Pengalihan eksklusif menampilkan seller asal/tujuan, SKU, jumlah bebas, reservasi terdampak, referensi ketentuan, dan alasan. Admin dapat menyetujui hanya jika penggunaan baru sesuai ketentuan; barang yang sudah terikat order lain tidak dipindahkan diam-diam.

Opname/selisih dicatat PPIC sebagai usulan penyesuaian. Sumber resmi tetap BigSeller; aplikasi tidak menimpa saldo resmi tanpa mekanisme yang disepakati. Status selisih: terbuka → diperiksa → koreksi sumber/pemetaan → direkonsiliasi, dengan bukti dan PIC.

## 8. Penjadwalan dan produksi parsial — FR-03 / FR-04

### FR-03.1 Urutan kerja

Urutan dasar yang diusulkan: pengecualian admin aktif → waktu antrean order → ID internal sebagai pemecah seri. Hanya jumlah yang siap diproses masuk antrean siap divisi. Deadline pickup memberi peringatan dan usulan perubahan; tidak diam-diam mengambil alokasi order lebih awal.

Pekerjaan restock menampilkan kelas terpisah tetapi memakai kapasitas divisi yang sama. Slot restock disetujui admin; bukan otomatis lebih tinggi daripada order aktual. Penggabungan SKU/rute/versi desain hanya diperbolehkan jika spesifikasi kompatibel dan setiap alokasi ke order tetap terlacak.

### FR-03.2 Hambatan

Kategori awal: data order, desain, bahan, stok tidak cocok, antrean, mesin, tenaga kerja, vendor, kualitas, pickup, lainnya. Field: jumlah terdampak, uraian, PIC, mulai, tindakan, tenggat tindak lanjut bila ada. Hambatan selesai memiliki waktu dan resolusi; mengubah status saja tidak menciptakan hasil produksi.

### FR-04.1 Pencatatan hasil

Form default: pekerjaan terpilih, tahap, jumlah input tersedia, hasil baik, ditahan untuk evaluasi/rework, scrap, pelaksana, waktu, catatan. Pilihan kategori detail cacat dapat dikembangkan tanpa mewajibkan operator mengetik laporan panjang.

Untuk satu kelompok unit yang diproses pertama kali:

`input unik = belum diproses + sedang diproses + baik + hold/rework + scrap`

Hasil baik yang sudah ditransfer tetap termasuk keluaran tahap tersebut; saldo baik belum ditransfer = keluaran baik − transfer keluar neto. Rework memindahkan unit dari hold ke proses ulang lalu baik/hold/scrap, tanpa menambah input unik. Jumlah percobaan proses ulang dapat dicatat sebagai aktivitas, terpisah dari unit baik unik.

### FR-04.2 Serah-terima

- Pengirim memilih jumlah baik yang belum ditransfer dan tujuan.
- Penerima mengonfirmasi jumlah aktual; selisih masuk pemeriksaan.
- Jumlah diterima menjadi input tahap berikutnya; barang yang baru dikirim belum dianggap diterima.
- Transfer minimum belum ditetapkan: sistem mendukung jumlah parsial positif dan tidak memaksakan minimum rekaan.
- Rute desain/printing/press/cutting/vendor/QC mengikuti kategori dan versi rute. Perubahan rute pekerjaan aktif harus ditinjau admin/PPIC dengan alasan.

## 9. Vendor keluar dan kembali — FR-05

1. PPIC/koordinator memilih pekerjaan dan jumlah yang siap dikirim.
2. Catat waktu keluar NCK, jumlah, transport/referensi, vendor, dan estimasi kembali versi awal.
3. Catat penerimaan vendor jika tersedia; jangan mengarang waktu dari waktu keluar.
4. Penerimaan kembali dapat parsial; simpan waktu/jumlah setiap kedatangan.
5. Jumlah kembali masuk antrean QC, bukan langsung barang siap jual.

`sisa tanggung jawab vendor = jumlah keluar neto − jumlah kembali neto − penyelesaian kehilangan/scrap yang disetujui dan terdokumentasi`

Parameter awal ±300 pcs/hari adalah alokasi khusus NCK, bukan kapasitas yang dikalikan mesin/karyawan. Kalender, sisa slot, dan realisasi harus tampil. Estimasi ±24 jam mencakup rentang keluar sampai kembali; jangan menambah transport sekali lagi apabila sudah tercakup. Titik awal pengukuran dan hari kerja vendor dikonfirmasi melalui TBD-03.

Simpan estimasi awal dan revisi. Keterlambatan terhadap janji awal tidak hilang ketika estimasi digeser. Jika belum kembali saat estimasi lewat, tampilkan overdue berjalan, PIC, dan tindak lanjut; bukan waktu selesai nol.

## 10. Estimasi dan pengiriman — FR-06

### FR-06.1 Estimasi

Per item/kuantitas yang diperlukan, tentukan jalur berdasarkan ready stock, DTF, jersey, dan kesiapan desain. Jadwal memakai prasyarat, kalender, antrean, serta ketersediaan sumber daya. Untuk tahap yang telah tervalidasi, waktu proses dapat diturunkan dari jumlah dan laju relevan; laju ideal diberi label dan tidak dianggap laju aktual terjamin.

Tahap berikutnya dapat dijadwalkan atas transfer parsial yang tersedia. Jangan menjumlahkan durasi batch seluruh tahap secara serial jika alirannya tumpang tindih, dan jangan menganggap semuanya paralel tanpa batas sumber daya.

`perkiraan paket siap = waktu semua item lolos kebutuhan QC + sisa pekerjaan packing pada jadwal yang tersedia`

Secara agregat, ambil waktu item terakhir yang siap; QC yang sudah selesai tidak dihitung ulang. Perkiraan pickup adalah jadwal terkonfirmasi pertama yang masih dapat dicapai setelah paket siap dan sebelum batas penerimaan pickup yang disepakati. Buffer packing/handover tidak diberi angka sampai diukur.

Jika cutting, transfer, atau kalender penting belum diketahui: tampilkan “data belum cukup” atau estimasi PPIC dengan sumber/alasan. Jangan menghasilkan waktu presisi otomatis. Perubahan stok, batch, hambatan, jadwal vendor/pickup, dan hasil aktual memicu evaluasi ulang serta menyimpan versi estimasi yang dibandingkan.

### FR-06.2 Packing dan handover

- Picking memeriksa SKU/ukuran/jumlah dan mengikat barang ke paket.
- QC gagal menahan jumlah terkait dan mengembalikan kebutuhan pengganti/rework ke perencanaan; paket belum siap.
- Packing mengonfirmasi semua item, resi aktif, identitas seller pada paket, dan jumlah.
- Pickup 13.00/16.00 ditampilkan berdasarkan kalender operasional yang dikonfirmasi. Pickup 18.00 berstatus diminta/terkonfirmasi/dibatalkan.
- Handover membutuhkan kejadian aktual dan bukti/referensi; jadwal pickup yang lewat tidak otomatis membuat paket terkirim.
- Paket siap yang melewatkan pickup tetap siap tetapi belum terkirim; estimasi berpindah ke pickup berikutnya dengan alasan.
- Mode kirim parsial tidak disediakan sebagai jalan pintas untuk menandai paket belum lengkap sudah terkirim.

## 11. Rekomendasi stok dan keputusan — FR-07

### FR-07.1 Input dan horizon

Input minimum: SKU/pool, permintaan historis yang diketahui, umur SKU, stock snapshot, komitmen order, WIP dan waktu siap, lead time, serta waktu review berikutnya. Tampilkan kelengkapan setiap input.

Histori tujuh hari memakai jendela yang dinyatakan jelas; usulan baseline tujuh hari kalender lengkap sebelum waktu evaluasi. Hari tanpa data berbeda dari hari dengan nol permintaan. Pembatalan diketahui dikeluarkan dari permintaan aktif dan dilaporkan terpisah; data batal yang tidak lengkap diberi catatan bias.

Untuk stok bersama, agregasikan permintaan seller yang berhak memakai pool itu. Eksklusif dihitung terpisah; jangan mengurangkan seluruh stok eksklusif dari kebutuhan bersama atau menduplikasi kebutuhan seller pada kedua pool.

### FR-07.2 Perhitungan usulan baseline

Usulan awal memakai bucket waktu harian selama lead time replenishment + waktu sampai peninjauan berikutnya:

- `K_b`: kebutuhan order aktif belum terkirim yang dialokasikan ke bucket b.
- `F_b`: perkiraan total permintaan untuk bucket b; asumsi metode dan versi tersimpan.
- `U_b = max(0, F_b − K_b)` jika forecast mencakup order yang sudah diketahui pada bucket yang sama. Jika forecast memang khusus order baru yang belum diketahui, `U_b = F_b`; pilih satu semantik yang eksplisit, bukan mencampur keduanya.
- `D_b = K_b + U_b`. Pending sebelum horizon dimasukkan sebagai kebutuhan awal satu kali.
- `S`: stok layak jual pool, bruto terhadap order K yang ikut dihitung. Reservasi bagi order di luar cakupan dikurangi dari S; reservasi bagi K tidak dikurangi lagi.
- `W_b`: hasil produksi lain yang diperkirakan siap dan lolos QC tepat pada bucket b; usulan baru ini tidak termasuk W.
- `P_b = S + Σ(W_i − D_i)` hingga bucket b.

Usulan jumlah bruto pada akhir horizon: `Q = ceil(max(0, target_saldo_akhir − P_akhir))`. Target saldo akhir/safety stock harus berasal dari kebijakan yang disetujui; jika belum ada, tampilkan skenario saldo akhir nol sebagai pembanding, bukan default resmi.

Saldo negatif sebelum waktu hasil restock bisa tersedia tetap ditampilkan sebagai kekurangan yang tidak dapat diselamatkan oleh usulan tersebut. Jumlah usulan tidak otomatis berarti layak diproduksi: periksa kapasitas, bahan, waktu siap, dan risiko modal. Pembulatan batch hanya jika aturan batch sudah ditetapkan.

Contoh sintetis: kebutuhan pasti 12, forecast total horizon 20 yang sudah mencakup kebutuhan pasti, stok bruto 10, WIP tepat waktu 5, target akhir 0. Kebutuhan total 20, bukan 32; usulan bruto 5. Jika WIP datang setelah deadline, kebutuhan lebih awal tetap berisiko meskipun jumlah akhir tampak cukup.

### FR-07.3 Klasifikasi, risiko, dan admin

- Kategori stabil/viral/baru/menurun/jarang dapat ditetapkan PPIC dengan alasan pada versi awal; ambang otomatis belum disetujui.
- SKU baru tidak dipaksa memiliki forecast numerik jika data pembanding tidak memadai. Sajikan batch uji yang diusulkan manusia beserta risiko.
- Kartu rekomendasi memuat jumlah, nilai jika biaya tersedia, waktu siap, kapasitas terpakai, pending yang terbantu, risiko sisa, sumber/versi data, dan alternatif.
- Saat diajukan, admin dapat setujui/tolak/ubah dengan alasan. Perubahan stok/order/biaya yang material memicu evaluasi ulang sebelum pelaksanaan; ambang material perlu ditetapkan, sementara versi pertama menandai setiap perubahan input pembentuk keputusan.
- Persetujuan membuat otorisasi pekerjaan restock, bukan bukti hasil produksi atau stok masuk. Satu persetujuan tidak boleh menghasilkan pekerjaan ganda saat retry.
- Usulan penghentian restock hanya memengaruhi bagian belum dikerjakan setelah admin memutuskan; WIP dan biaya terlanjur terjadi tetap tercatat.

### FR-07.4 Dead stock

Indikator: hari sejak penjualan terakhir, umur stok/lot jika ada, stok tersisa, laju permintaan, dan cakupan stok. `cakupan hari = stok tersedia / rata-rata permintaan harian` hanya bila penyebut >0 dan datanya cukup; jika nol, tampilkan “tidak ada permintaan pada jendela”, bukan nol hari.

Sekitar dua bulan tanpa penjualan adalah kebijakan evaluasi awal, bukan otomatis 60 hari atau dua bulan kalender sampai TBD-06 disahkan. Transfer lokasi, koreksi saldo, dan pindah pool tidak mengatur ulang tanggal penjualan terakhir. SKU belum pernah terjual memakai tanggal pertama tersedia bila diketahui, bukan tanggal impor.

Diskon/lelang memerlukan keputusan admin dengan SKU/jumlah, dasar harga, dampak margin bila diketahui, alasan, dan masa berlaku. Versi pertama mencatat persetujuan; tidak menerbitkan harga atau listing eksternal.

## 12. Dashboard, metrik, dan margin — FR-08

### FR-08.1 Kohort dan waktu laporan

Semua metrik memiliki periode, waktu cut-off/as-of, versi definisi, waktu data, dan tautan rincian. Laporan akhir hari berbeda dari laporan siang yang masih berjalan.

Usulan lapisan transparansi:

- Kohort bruto: seluruh paket unik yang diterima pada tanggal d, termasuk yang kemudian tidak valid/batal; duplikat terbukti tidak termasuk.
- Tampilkan jumlah paket bruto, valid, belum valid, batal, diserahkan hari sama, dan belum diserahkan.
- `same-day bruto = paket kohort yang diserahkan pada tanggal d / paket kohort bruto × 100%`.
- Rasio operasional neto pembatalan dapat ditambahkan setelah kebijakan denominator disahkan (TBD-02), dengan denominator dan pengecualian terlihat. Rasio bruto tidak disembunyikan.
- Bila denominator nol: “tidak ada order”, bukan 0%/100%.
- Untuk pcs, gunakan kuantitas versi order pada cut-off laporan dan simpan versi laporan. Perubahan terlambat memunculkan laporan direvisi; jangan mengubah angka historis diam-diam.
- Paket tercetak atau siap tidak dihitung terkirim. Handover hari berikutnya tidak memperbaiki same-day kohort kemarin.

### FR-08.2 Pending dan kualitas

- Backlog: kebutuhan aktif diterima sampai as-of tetapi belum diserahkan. Pisahkan order belum valid dari antrean kerja valid; keduanya tetap terlihat.
- Pending hari ini: bagian backlog dari kohort hari ini; bukan seluruh backlog.
- Umur pending: as-of dikurangi waktu terima; tampilkan waktu tunggu validasi terpisah jika ada.
- Rework bukan output jual baru. Rasio cacat tahap memakai unit unik gagal pada pemeriksaan awal dibagi unit unik diperiksa awal; aktivitas rework dilaporkan terpisah untuk mencegah denominator membesar karena inspeksi ulang.
- Waktu antre dan proses hanya dihitung jika timestamp tersedia; data hilang menurunkan cakupan, bukan dianggap durasi nol.
- Tampilan tim menunjukkan jenis pekerjaan, kualitas, hambatan, dan cakupan data; tidak menghasilkan ranking individu otomatis dari pcs saja.

### FR-08.3 Biaya dan margin

- Harga jual item, diskon, dan biaya standar memiliki mata uang serta versi/tanggal berlaku. Usulan mata uang operasional IDR; transaksi lain memerlukan kebijakan terpisah.
- `nilai neto item = kuantitas aktif × harga unit − diskon item`.
- Diskon order/biaya bersama hanya dialokasikan jika kebijakan ditetapkan; sebelum itu tampilkan sebagai komponen belum dialokasikan dan margin belum lengkap.
- `estimasi biaya = Σ(kuantitas aktif × biaya standar versi terkait) + biaya tambahan yang belum termasuk standar`.
- `estimasi margin = nilai penjualan neto − estimasi biaya`; `margin % = estimasi margin / nilai penjualan neto × 100%` bila nilai neto >0. Jika nol, persentase tidak tersedia, nominal tetap ditampilkan.
- Daftar komponen standar harus menunjukkan apakah bahan, vendor, tenaga kerja, kemasan, dan overhead sudah termasuk; jangan menambah vendor/rework dua kali.
- Margin seller dihitung dari total nilai dan biaya order dengan cakupan sama, bukan rata-rata sederhana persentase order.
- Riwayat versi standar tidak ditimpa ketika standar baru dibuat. Estimasi dan aktual ditampilkan terpisah.
- Kebijakan pengakuan omzet, pajak, retur, overhead, invoice dan kas masuk masih TBD-08. Sebelum tersedia, dashboard memakai label “nilai order” dan “estimasi margin”, bukan laba bersih/omzet terverifikasi.

## 13. Notifikasi dan AI — FR-10 / FR-11

### FR-11 Notifikasi internal

Pemicu: order perlu koreksi, hambatan baru, risiko melewatkan pickup, vendor overdue, stok tidak cocok, usulan keputusan, dan rekomendasi perlu evaluasi ulang.

Satu kasus aktif memiliki satu notifikasi yang diperbarui, bukan pesan baru setiap refresh. Memiliki objek, alasan, dampak, PIC, waktu, dan tindakan. Dibaca berbeda dari selesai; selesai mensyaratkan resolusi kasus. Ambang eskalasi dan pengganti PIC mengikuti TBD-07. Belum ada pengiriman otomatis WhatsApp/email ke seller atau vendor.

### FR-10 AI penjelasan

- Jawaban/ringkasan merujuk order, pekerjaan, laporan, atau rekomendasi yang berhak diakses pengguna.
- Pisahkan fakta tercatat, hasil perhitungan, dugaan penyebab, dan usulan tindakan.
- Jika data usang/tidak lengkap, sebut keterbatasannya; jangan mengisi angka kapasitas atau biaya sendiri.
- AI tidak menjalankan persetujuan, mutasi stok, perubahan harga, prioritas, atau pesan eksternal.
- Kegagalan AI tidak menghambat order/produksi/pengiriman; dashboard angka tetap tersedia.

## 14. Integrasi, impor, dan gangguan — FR-12

| Data | Sumber/otoritas tahap awal | Perilaku yang harus dipastikan |
|---|---|---|
| Stok fisik resmi | BigSeller | Arti bruto/neto, kondisi/lokasi, waktu snapshot, ID mutasi, rekonsiliasi |
| Histori/input order | Sheets/n8n/sumber yang diaudit | ID unik, waktu sumber, pembatalan, alias SKU, impor ulang |
| Progres/transfer/PIC | Aplikasi baru | Identitas kejadian, retry aman, koreksi teraudit |
| Reservasi | TBD-01 | Pilih otoritas dan pemetaan; jangan ada dua pengurangan untuk komitmen sama |
| Nilai/biaya | Sumber finance terverifikasi | Mata uang, versi, kelengkapan, siapa boleh mengubah |

Status impor: diterima → divalidasi → diterapkan sebagian/penuh atau ditahan/gagal. Ringkasan menampilkan total order/item, berhasil, duplikat, konflik, dan gagal beserta alasan. Retry hanya menerapkan bagian yang belum berhasil.

Sinkronisasi menampilkan waktu data sumber dan waktu diterima, bukan sekadar “terhubung”. Perubahan snapshot tidak menghapus reservasi atau koreksi lokal tanpa pencocokan kejadian. Selisih masuk daftar rekonsiliasi dengan PIC dan bukti penyelesaian.

Jika koneksi gagal saat simpan: UI menunjukkan belum terkonfirmasi, mempertahankan input, dan memeriksa ID kejadian sebelum retry. Jangan menampilkan sukses palsu. Jika integrasi usang, alokasi/estimasi ditandai sementara; tindakan berisiko memakai konfirmasi PPIC yang tercatat menurut kebijakan TBD-01.

Prosedur pencatatan sementara ketika aplikasi tidak tersedia dan input susulan ditetapkan sebelum pilot. Offline penuh, API tertentu, frekuensi sinkronisasi, dan write-back otomatis belum dijanjikan.

## 15. Skenario penerimaan/UAT

Semua angka berikut sintetis. UAT belum dijalankan; tabel ini adalah spesifikasi hasil yang harus dibuktikan saat implementasi.

| UAT | Kondisi dan tindakan | Hasil yang harus terlihat | Trace |
|---|---|---|---|
| U01 | Impor order sumber yang sama dua kali | Satu order, satu efek alokasi; log pengulangan | F01 / AC01 / FR-01 |
| U02 | Resi sama tetapi seller/item berbeda | Konflik ditahan, tidak overwrite otomatis | F01 / FR-01 |
| U03 | Dua order bersamaan meminta satu unit shared | Satu reservasi berhasil, satu kekurangan | F02 / AC02 / FR-02 |
| U04 | B mencoba stok eksklusif A | Tidak teralokasi; pengalihan perlu admin dan ketentuan | F02,F09 / AC03 / FR-02,09 |
| U05 | Paket 3 SKU, hanya 2 lengkap | Tidak dapat siap kirim/handover | F06 / AC04 / FR-06 |
| U06 | Tahap menerima 100, menghasilkan 60 baik, transfer 40 | Baik belum transfer 20; sisa input 40; tahap berikutnya baru menerima jumlah terkonfirmasi | F04 / AC05 / FR-04 |
| U07 | Dari 10 input, 8 baik dan 2 hold; rework 2 jadi baik | Output unik 10, bukan 12; aktivitas ulang tetap tercatat | F04 / FR-04 |
| U08 | Vendor keluar 100, kembali 60 dengan 5 gagal QC | Sisa vendor 40; 55 baik dan 5 hold; tidak ada stok baik 60 | F05 / AC06 / FR-05 |
| U09 | Order awal menunggu desain; berikutnya siap | Berikutnya dapat berjalan; awal tetap terlihat terhambat | F03 / AC07 / FR-03 |
| U10 | Paket diperkirakan siap 17.00, pickup 18.00 belum pasti | Estimasi kondisional, tidak janji pasti | F06 / AC08 / FR-06 |
| U11 | Jersey perlu cutting, kapasitas belum diketahui | Tidak ada waktu otomatis palsu; minta estimasi PPIC atau tampil belum cukup data | F06 / AC09 / FR-06 |
| U12 | Permintaan turun ketika restock sudah mulai | Usul evaluasi; WIP tidak hilang/dibatalkan otomatis | F07 / AC10 / FR-07 |
| U13 | Order batal setelah sebagian dipicking/produksi | Reservasi aman dilepas; barang picked/WIP tetap ditangani eksplisit | F01 / AC11 / FR-01,02 |
| U14 | Snapshot stok usang/selisih | Label waktu/selisih; komitmen mengikuti konfirmasi yang disepakati | F02 / AC12 / FR-02,12 |
| U15 | Biaya vendor tidak tersedia | Margin tidak berlabel lengkap/laba bersih | F08 / AC13 / FR-08 |
| U16 | Operator A menginput hasil tim B | Pencatat A, pelaksana B; tidak seluruh output diklaim A | F09 / AC14 / FR-09 |
| U17 | Resi tercetak tanpa handover | Tidak masuk numerator terkirim/same-day | F06,F08 / AC15 / FR-06,08 |
| U18 | Order K=12, forecast total 20, stok 10, WIP tepat waktu 5, target 0 | Usulan bruto 5; bukan 17; asumsi forecast terlihat | F07 / FR-07 |
| U19 | WIP U18 datang setelah kebutuhan jatuh tempo | Kekurangan awal tetap ditandai meski saldo akhir cukup | F07 / FR-07 |
| U20 | Klik setujui restock dua kali/retry | Satu otorisasi dan satu pelaksanaan yang terkait | F07,F09 / FR-00,07 |
| U21 | Snapshot baru sudah memuat mutasi lokal | Efek mutasi tidak dihitung dua kali | F02 / FR-02,12 |
| U22 | Tidak ada order pada tanggal laporan | Rasio “tidak ada order”, bukan 0%/100% | F08 / FR-08 |
| U23 | Barang pindah gudang tetapi tidak terjual | Umur sejak penjualan terakhir tidak direset | F07 / FR-07 |
| U24 | Pengguna produksi meminta biaya lewat ekspor/AI | Akses ditolak sama seperti layar biaya | F09,F10 / FR-09,10 |
| U25 | Biaya standar baru berlaku setelah order lama | Estimasi historis tetap memakai versi tercatat | F08 / FR-08 |
| U26 | Paket siap melewatkan pickup | Tetap belum terkirim, estimasi berikutnya dan alasan terlihat | F06 / FR-06 |

## 16. Pemetaan PRD → FRD

| PRD | Bagian FRD | Kriteria PRD |
|---|---|---|
| F01 Order | FR-00, FR-01 | AC01, AC11 |
| F02 Stok | FR-02, FR-12 | AC02, AC03, AC12 |
| F03 Prioritas | FR-03 | AC07 |
| F04 Produksi/QC | FR-04 | AC05 |
| F05 Vendor | FR-05 | AC06 |
| F06 Estimasi/kirim | FR-06 | AC04, AC08, AC09, AC15 |
| F07 Rekomendasi stok | FR-07 | AC10 |
| F08 KPI/margin | FR-08 | AC13, AC15 |
| F09 Akses/persetujuan | FR-09, FR-00 | AC03, AC14 |
| F10 AI | FR-10 | U24 dan batas non-eksekusi |

FR-11 notifikasi dan FR-12 integrasi mendukung fungsi PRD, bukan perluasan kanal komunikasi atau penggantian sistem sumber.

## 17. Register keputusan terbuka dan gerbang implementasi

| ID | Yang perlu dipastikan | Penanggung jawab usulan | Perilaku sementara | Gerbang yang terdampak |
|---|---|---|---|---|
| TBD-01 | BigSeller bruto/neto, reservasi, snapshot, batas data usang, ID mutasi, mekanisme integrasi | Admin + PPIC + teknis | Impor/konfirmasi dan alokasi sementara | Komit stok otomatis dan pilot integrasi |
| TBD-02 | Waktu antrean, order diperbaiki, cut-off, batal/kuantitas revisi dalam KPI | Pemilik + admin | Timestamp asli dipertahankan; tampil angka mentah dan usulan bruto | KPI resmi dan aturan antrean final |
| TBD-03 | Cutting, lokasi/serah-terima, minimum transfer, kalender, durasi vendor, QC/packing | PPIC + divisi/vendor | Estimasi manual berlabel/tidak tersedia | ETA otomatis yang mencakup tahap belum terukur |
| TBD-04 | Safety stock, batas modal, metode forecast, batch, slot restock | Pemilik + admin + PPIC | Skenario/usulan manual dengan dampak, tanpa angka default resmi | Rekomendasi kuantitatif sebagai kebijakan operasional |
| TBD-05 | Hak/kepemilikan/risiko eksklusif, urutan pool | Admin + pemilik | Pisahkan eksklusif; jangan alihkan tanpa dasar ketentuan | Pemakaian dan pengalihan lintas seller |
| TBD-06 | Dua bulan = hari atau kalender; ambang dini; jenis penjualan/pergerakan | Admin + PPIC | Tampilkan umur aktual dan indikator, label ambang belum disahkan | Peringatan dead stock otomatis berbasis ambang |
| TBD-07 | PIC desain/vendor/finance, pengganti admin, eskalasi, koreksi stok | Pemilik + admin | Antrean keputusan dan PIC kosong terlihat | Matriks akses final dan kesiapan pilot |
| TBD-08 | Komponen standar, overhead, diskon order, omzet/pajak, akses finance | Pemilik + finance/admin | Nilai order/estimasi dengan kelengkapan | Laporan keuangan resmi |
| TBD-09 | Cakupan pilot, target hasil, waktu pengamatan, performa, backup dan pemulihan | Pemilik + tim teknis | Belum ada janji angka/tanggal | Peluncuran pilot dan TRD |

TBD tidak menghalangi review rancangan atau pekerjaan pada modul yang independen. Namun fitur yang bergantung pada parameter tersebut tidak dinyatakan siap operasional sebelum keputusan/data tercatat.

## 18. Penyerahan ke TRD

TRD berikutnya menerjemahkan FRD ke arsitektur dan kontrak integrasi setelah audit sumber, termasuk mekanisme transaksi bersamaan, idempotensi, skema data, autentikasi perangkat bersama, logging, penyimpanan bukti, backup, pemulihan, serta pengujian beban. Tidak ada API, library, kapasitas teknis, atau jadwal pembangunan yang dianggap sudah dipilih oleh FRD ini.

Review FRD memprioritaskan aturan stok/rekonsiliasi (bagian 7), antrean dan parsial (8), estimasi (10), rekomendasi (11), serta metrik (12). Perubahan keputusan dicatat pada versi berikutnya; BRD/PRD tidak otomatis ditulis ulang oleh pembuatan draft ini.

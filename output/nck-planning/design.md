# NCK Operations Control Center — Design System

Versi 0.1 · 1 November 2026 · Bahasa antarmuka: Indonesia

Status: pedoman desain aplikasi untuk review dan implementasi berikutnya. Dokumen ini tidak membangun UI atau mengaktifkan integrasi. Pilihan visual merupakan adaptasi referensi pemilik, bukan penggantian otomatis master brand NCK.

## 1. Sumber dan urutan acuan

- Referensi utama: `stitch_branded_dashboard_ui_design.zip` yang diberikan pemilik, berisi [screenshot](design-reference/screen.png), [HTML](design-reference/code.html), dan [DESIGN.md sumber](design-reference/DESIGN.md).
- Perilaku aplikasi mengikuti [BRD](BRD-NCK-v0.1.md), [PRD](PRD-NCK-v0.1.md), [FRD](FRD-NCK-v0.1.md), dan [TRD](TRD-NCK-v0.1.md).
- Identitas logo dan warna master merujuk [Identitas Visual NCK](</Users/ademuhamadfaisal/Desktop/OBSIDIAN FAISAL/wiki/topics/Identitas Visual NCK.md>).

Screenshot menjadi acuan komposisi visual; kode dan DESIGN.md sumber membantu membaca intent. Keduanya memiliki variasi token warna/radius. Token kanonik aplikasi ditetapkan di dokumen ini agar developer tidak mencampur dua sistem. Instruksi, nama pengguna, angka, layanan, dan klaim dalam template adalah isi referensi; tidak menjadi fakta operasional atau otorisasi fitur NCK.

## 2. Arah visual

**Pusat kendali produksi dengan identitas fashion yang kuat:** kanvas hampir hitam, panel abu gelap berlapis, aksen magenta dan cyan, tipografi judul tegas, serta informasi kerja yang mudah dipindai.

Pertahankan dari referensi:

- Sidebar permanen, topbar ringkas, kartu KPI dengan garis aksen di atas.
- Judul Syne yang khas, teks kerja Plus Jakarta Sans.
- Grid kartu dan tabel lebar dengan header tetap serta garis pemisah halus.
- Gelombang/kontur tipis sebagai aksen brand di area tenang.
- Angka besar dengan satuan yang jelas dan status produksi berbentuk badge.

Adaptasi untuk penggunaan sehari-hari:

- Hero slogan besar dipadatkan agar antrean dan risiko pickup terlihat lebih cepat.
- Label kecil, metadata merah muda, glow berlebihan, serta huruf kapital panjang dikurangi.
- Sidebar berisi modul kerja, bukan katalog penjualan jasa.
- Status tahap, urgensi, dan koneksi dibedakan; warna magenta tidak sekaligus berarti merek, error, dan semua prioritas.
- Jangan menampilkan suhu mesin, jumlah mesin aktif, utilisation, QC pass rate, atau label “live” tanpa sumber aktual dan definisi yang tersedia.

Prinsip layar: pengguna harus segera memahami **apa yang perlu dikerjakan, berapa jumlahnya, apa hambatannya, dan siapa yang bertanggung jawab**.

## 3. Identitas, logo, dan font

Nama produk: **NCK Operations Control Center**. Nama singkat di sidebar: **NCK Operations**. “NCK OS” boleh menjadi arah penamaan berikutnya, tetapi bukan nama produk yang sudah ditetapkan.

Tagline resmi tetap “Kami Produksi, Kamu Beraksi.” Tampilkan kecil pada halaman ringkasan/welcome, bukan sebagai judul setiap halaman.

Logo dari URL pada HTML template tidak otomatis menjadi master yang sah. Gunakan aset lokal resmi yang disetujui dan pertahankan komposisinya. Catatan brand menetapkan master utuh, latar hitam, ruang luar minimum 10% lebar file per sisi, dan ukuran digital minimum 200 px. Untuk sidebar 256 px, logo selebar 200 px beserta clear space dapat ditempatkan pada area header khusus. Pada rail 72 px, gunakan label teks “NCK” sebagai identitas UI sampai varian logo kecil disetujui; jangan memotong simbol atau memaksa master menjadi ikon 24 px.

Syne dan Plus Jakarta Sans diusulkan sebagai tipografi aplikasi sesuai referensi. Ini tidak mengubah huruf pada logo atau menetapkan font untuk semua materi perusahaan. Saat implementasi, siapkan aset font dengan lisensi yang sesuai dan fallback; tidak bergantung pada URL font CDN template untuk operasi utama.

## 4. Token warna kanonik

### 4.1 Permukaan dan teks

| Token | Nilai | Pemakaian |
|---|---|---|
| `bg.canvas` | `#111317` | Kanvas utama, mengikuti konfigurasi HTML referensi |
| `bg.sidebar` | `#1A1C20` | Navigasi permanen |
| `bg.panel` | `#1A1C20` | Kartu/tabel utama |
| `bg.raised` | `#282A2E` | Drawer, menu, kontrol sekunder |
| `bg.input` | `#111317` | Field dalam panel |
| `bg.hover` | `#333539` | Hover baris/opsi |
| `border.subtle` | `#3A3D44` | Pemisah panel dan tabel |
| `border.control` | `#747A86` | Batas input/kontrol interaktif |
| `text.primary` | `#E2E2E8` | Angka dan teks utama |
| `text.secondary` | `#B8BDC8` | Metadata penting, label form |
| `text.muted` | `#9AA3B2` | Keterangan tambahan/placeholder |
| `text.inverse` | `#111317` | Teks di tombol cyan/kuning |

Metadata netral menggantikan dominasi pink-muted dari template agar warna pink tetap bermakna sebagai aksen.

### 4.2 Brand dan aksen UI

| Token | Nilai | Pemakaian |
|---|---|---|
| `action.primary` | `#E6007E` | Tombol utama dan menu aktif; turunan UI template |
| `action.primaryHover` | `#C9006D` | Hover yang tetap menjaga kontras teks putih |
| `accent.magentaText` | `#FFB0C9` | Teks kecil magenta di permukaan gelap |
| `accent.cyan` | `#00A3E0` | Garis grafik/progres dan bidang aksi sekunder |
| `accent.cyanText` | `#81CFFF` | Link, angka informasional, focus |
| `accent.yellow` | `#FFD100` | Aksen review; jangan dipakai sebagai seluruh tombol tindakan |
| `accent.violetText` | `#C4B5FD` | Kategori vendor/desain bila diperlukan |

Warna master brand tetap **magenta #E90F89, biru #0194E1, kuning #FDE900**, mengikuti catatan identitas. Jangan mewarnai ulang master logo dengan warna UI. Palette UI di atas adalah adaptasi template untuk layar gelap; perbedaannya disengaja dan harus didokumentasikan saat handoff.

### 4.3 Status semantik

| Makna | Foreground | Background | Label contoh |
|---|---|---|---|
| Selesai/terkonfirmasi | `#76EDB4` | `#12382C` | “Diterima”, “Terkirim” |
| Informasi/proses | `#81CFFF` | `#143144` | “Dikerjakan”, “Dialokasikan” |
| Perlu perhatian | `#FFE07F` | `#3C320F` | “Perlu keputusan”, “Pickup belum pasti” |
| Error/terhambat | `#FFB4AB` | `#4B2028` | “Stok tidak cocok”, “Terhambat” |
| Belum tersedia/netral | `#B8BDC8` | `#282A2E` | “Menunggu”, “Data belum cukup” |

Warna wajib didampingi label dan ikon/pola. Cyan/magenta juga dipakai sebagai identitas tahap, sehingga badge tahap tidak boleh menggantikan badge kondisi. Contoh: **Press** dengan aksen magenta + **Terhambat: bahan** dengan badge error.

## 5. Tipografi dan format data

| Token | Font | Ukuran / line-height | Weight |
|---|---|---|---|
| Page title | Syne | 28 / 36 px | 700 |
| Section title | Syne | 20 / 28 px | 700 |
| Card title | Plus Jakarta Sans | 16 / 24 px | 700 |
| KPI value | Syne | 32 / 40 px | 800 |
| Body/table | Plus Jakarta Sans | 14 / 22 px | 400/600 |
| Form/button | Plus Jakarta Sans | 14 / 20 px | 600 |
| Metadata | Plus Jakarta Sans | 12 / 18 px | 400/600 |
| Small section label | Plus Jakarta Sans | 12 / 16 px | 700 |

Hero 48 px seperti template hanya untuk welcome/brand presentation, bukan halaman kerja. Angka uang panjang menggunakan Plus Jakarta Sans 28/36 bila Syne membuatnya terpotong. Jangan mengecilkan teks tabel di bawah 14 px untuk memaksa banyak kolom.

- Gunakan tabular figures pada angka; bila font display tidak mendukung, gunakan font body untuk kolom angka.
- Angka dan uang rata kanan; nama/status rata kiri. Satuan dekat angka, tidak terpisah ke sudut kartu.
- Format Indonesia: `1.250 pcs`, `Rp395.000.000`, `28,5%`, `16.00 WIB`.
- Kartu ringkas boleh `Rp395 juta`; detail/tooltip/accessible label memuat angka lengkap. Hindari `Rp184,5M` karena ambigu juta/miliar.
- Tanggal lintas hari selalu eksplisit, misalnya `2 Nov, 13.00 WIB`; jangan hanya “besok” pada ekspor.
- Status kosong: `Belum tersedia`, bukan `0`. Nilai nol sah tetap `0` dengan konteks.
- Kapital hanya label pendek. Judul tabel, pesan error, dan kalimat memakai sentence case.

## 6. Layout, spacing, radius, dan motion

### 6.1 Shell dan grid

Desktop >=1280 px: sidebar 256 px; opsi rail 72 px; topbar minimum 64 px; area konten maksimum 1720 px; margin 28 px; gap 20 px; grid 12 kolom. Tinggi topbar boleh bertambah jika zoom/text wrap, offset konten mengikuti ukuran aktual.

Tablet 768–1279 px: rail 72 px dengan drawer navigasi; konten margin 20 px dan gap 16 px; grid 8 kolom; KPI 2×2. Pada layar 1024 px, kurangi kolom tabel yang kurang penting sebelum mengecilkan teks.

Mobile <768 px: navigasi drawer, margin 16 px, gap 12 px, grid 4 kolom; kartu satu kolom pada <480 px dan dua bila cukup ruang. Detail item menggunakan kartu berlabel. Aksi utama boleh sticky di bawah dengan ruang aman agar isi tidak tertutup.

Tabel perbandingan tetap dapat scroll horizontal dalam container berlabel dengan scrollbar terlihat. Seluruh halaman tidak boleh scroll horizontal. Jangan menyalin `::-webkit-scrollbar{display:none}` dari template.

### 6.2 Token ukuran

- Spacing scale: 4, 8, 12, 16, 20, 24, 28, 32, 40 px.
- Padding panel 20–24 px; jarak antarsection 24–32 px.
- Radius input/button 6 px; card/table 8 px; drawer/modal 12 px; badge kecil 4 px; avatar/status pill 9999 px.
- Tinggi kontrol utama 44 px; tombol ikon 44×44 px. Baris tabel minimal 52 px, meningkat sesuai wrap. Mode nyaman 64 px untuk terminal sentuh.
- Border 1 px; focus ring 2 px cyan terang dengan offset 2 px.
- Shadow panel minimal; drawer/modal `0 12px 32px rgba(0,0,0,0.45)`. Glow hanya aksen brand ringan, bukan penanda status utama.
- Layer: base 0, sticky table 10, sidebar 20, topbar 30, drawer backdrop 40/drawer 50, modal backdrop 60/modal 70, toast 80.
- Transisi 120–180 ms untuk hover/open; jangan animasikan angka stok sehingga tampak terus berubah. Tidak ada pulse/glow berkedip terus-menerus. Reduced-motion menghilangkan gerak dekoratif.

## 7. Navigasi dan header

Urutan navigasi versi pertama:

1. Ringkasan NCK.
2. Order & Pengiriman.
3. Pekerjaan Saya — landing default operator.
4. Produksi & Vendor.
5. Stok & PPIC.
6. Keputusan Admin — hanya sesuai hak.
7. Laporan.
8. Pengaturan — sesuai hak.

QC menjadi tampilan/filter kerja tersendiri di dalam alur produksi, bukan modul yang memutus keterkaitan item/paket. Marketing, CRM, dan OKR tidak ditampilkan sebagai menu aktif kosong sebelum tersedia.

Menu aktif: bidang magenta, teks putih, ikon dan indikator lokasi; hover netral. Label rail tersedia saat focus/hover, tetapi navigasi tetap bisa diakses keyboard.

Topbar: breadcrumb/judul konteks, pencarian order–resi–SKU–seller, notifikasi, identitas pengguna + peran + workstation, tombol “Ganti pengguna”. Pencarian mempertahankan scope hak akses. Pada lebar sempit pencarian membuka panel sendiri, bukan memampatkan nama pengguna.

Pisahkan indikator **koneksi aplikasi**, **waktu data stok BigSeller**, dan **waktu perhitungan laporan**. Label “Terhubung” bukan bukti stok terbaru. Contoh copy ilustratif: “Data stok: 10.05 WIB • perlu konfirmasi”. Jangan menampilkan suhu terminal atau nomor versi fiktif sebagai dekorasi.

## 8. Komposisi dashboard utama

```text
Sidebar | Header: pencarian · notifikasi · pengguna/peran
        | Ringkasan NCK     periode / seller / kategori
        | Waktu data + peringatan sumber bila perlu
        | Order masuk | Same-day | Pending | Siap pickup
        | Risiko pickup dan tindakan (8 kolom) | Keputusan admin (4)
        | Tahap produksi / backlog per divisi (12)
        | Tren terkirim & pending (8) | Stok kritis / restock (4)
        | Tabel order membutuhkan tindakan (12)
        | Nilai order & estimasi margin, sesuai akses (12)
```

Header ringkas berisi tagline sebagai caption. Tidak memakai banner slogan setinggi beberapa kartu. KPI bukan target dummy; label dan denominator mengikuti FRD:

- **Order masuk:** paket dan pcs, dengan periode.
- **Same-day:** numerator/denominator dan label definisi; data hari berjalan ditandai sementara.
- **Pending:** backlog total, umur tertua, serta bagian dari order hari ini.
- **Siap pickup:** paket lengkap yang belum diserahkan, jadwal terkait.

Kartu keuangan menampilkan nilai order dan estimasi margin sesuai kelengkapan biaya; omzet/laba aktual tidak diada-adakan. Kenaikan pending bukan delta hijau. Perbandingan periode hanya muncul bila definisi dan cakupan sebanding.

Panel risiko wajib memuat paket/kelompok pekerjaan, alasan, jumlah terdampak, PIC, deadline, dan tindakan. Panel “Layanan Unggulan” pada template diganti stok kritis/keputusan operasional. Tidak ada CTA konsultasi vendor eksternal pada dashboard internal.

## 9. Spesifikasi komponen

### 9.1 Button dan action hierarchy

- Primary: magenta, teks putih; satu aksi utama dominan per area tugas. Contoh “Simpan hasil”.
- Secondary: raised surface + teks terang/border; contoh “Lihat detail”. Cyan filled dengan teks gelap boleh untuk aksi kerja yang setara dan jelas konteksnya.
- Danger: merah semantik dengan teks kontras; contoh “Batalkan order”, bukan tombol primer magenta.
- Ghost: navigasi/aksi ringan; icon-only wajib nama aksesibel dan tooltip.
- Loading: label “Menyimpan…” dan indikator; cegah klik ganda tetapi pertahankan konteks. Disabled memiliki alasan dekat kontrol atau keterangan yang bisa diakses tanpa hover.
- Jangan memakai kuning untuk semua aksi mendesak; kuning menandai review, bukan otorisasi.

### 9.2 KPI card

Panel radius 8, top accent 3 px, label 12–14 px, value 32 px, unit dekat angka, caption 12 px, cakupan dan waktu. Seluruh kartu boleh membuka drilldown melalui link semantik; jangan menumpuk tombol/link bersarang.

Placeholder tidak memuat angka acak. Loading skeleton memiliki dimensi stabil. Data tidak lengkap menampilkan nilai yang tersedia + badge cakupan, bukan mengosongkan semua kartu.

### 9.3 Tabel operasional

Toolbar: pencarian dalam daftar, filter chip aktif, reset, ekspor sesuai hak. Header sticky, sortable dengan arah terlihat, row hover netral, selected row dengan checkbox dan jumlah pilihan. Nama seller/SKU boleh dua baris; angka dan action tidak terpotong. Header dan kolom pertama dapat sticky bila tidak menutupi kolom lain.

Default kolom order: prioritas, order/resi, seller, ringkasan item, jumlah siap/total, tahap penghambat, pickup/estimasi, PIC, aksi detail. ID dipisahkan dari nama; resi tetap teks. Detail lengkap di drawer, bukan 15 kolom kecil di layar utama.

Bulk action harus menampilkan eligible/tidak eligible per item dan hasil per paket; jangan satu toast sukses jika sebagian gagal. Pagination atau cursor mengikuti backend; filter/sort tidak hilang setelah detail ditutup.

### 9.4 Badge kondisi, tahap, dan kualitas data

Badge tahap: Printing cyan, Press magenta, Cutting/Vendor violet, QC kuning, Packing/Dispatch netral/cyan. Tahap tidak otomatis menunjukkan sukses.

Badge kondisi menggunakan token semantik: siap, proses, sebagian, terhambat, selesai. Badge data: “Sementara”, “Perlu rekonsiliasi”, “Estimasi”, “Biaya belum lengkap”. Teks status selalu terlihat; ikon tambahan bukan pengganti label.

### 9.5 Alur produksi

Jalur mengikuti produk:

- Ready stock → Picking → QC → Packing → Serah-terima ekspedisi.
- DTF → Desain bila diperlukan → Printing → Press → QC → Packing → Serah-terima.
- Jersey → Desain bila diperlukan → Printing → Press → Cutting → Jahit vendor → QC → Packing → Serah-terima.

Tahap opsional diberi “Tidak diperlukan”, bukan disimpulkan selesai. Jangan menyalin satu pipeline Printing–Press–Sablon–QC untuk semua produk.

Setiap tahap memuat input, hasil baik, hold/rework, scrap, terkirim ke tahap berikutnya, dan belum diserahkan sesuai konteks. Progress memperlihatkan kuantitas, misalnya “60/100 baik • 40 diserahkan”; tidak hanya bar persen. Selesai tahap dan selesai order dibedakan.

### 9.6 Form pencatatan kerja

Header: pekerjaan/SKU, jumlah tersedia, tahap, pelaksana. Field utama: baik, hold/rework, scrap, waktu kejadian, alasan bila perlu. Pencatat aktif terlihat terpisah dari pelaksana.

Validasi inline di bawah field dan ringkasan error fokusable. Jumlah melebihi input ditolak dengan pesan konkret, misalnya “Jumlah hasil 12 pcs melebihi input tersedia 10 pcs.” Angka contoh ini hanya ilustrasi copy.

Konfirmasi serah-terima menampilkan jumlah keluar dan jumlah diterima sebagai dua kejadian; UI tidak otomatis mengisi “diterima” hanya karena pengirim menyimpan.

### 9.7 Drawer, modal, dan approval

Drawer detail lebar 560–640 px di desktop, full screen di mobile. Tabs: ringkasan, item, progres, stok/alokasi, riwayat; biaya hanya bila berhak. Aksi tetap terlihat tanpa menutupi isi.

Modal digunakan untuk keputusan terbatas: batal, alih eksklusif, setujui restock, atau perubahan prioritas. Tampilkan sebelum/sesudah, jumlah, seller/pekerjaan terdampak, alasan, dan versi data. Tidak ada approval pemilik tambahan di atas admin untuk empat kewenangan yang sudah disepakati.

Jika data berubah saat modal terbuka, pertahankan alasan yang ditulis dan tampilkan “Data berubah. Tinjau versi terbaru sebelum menyetujui.” Persetujuan usang tidak ditampilkan sebagai berhasil.

### 9.8 Grafik

Grafik operasional memakai garis/bar yang punya sumbu, satuan, periode, legenda dan tooltip; tidak meniru garis dekoratif tanpa angka dari template. Gunakan bar untuk perbandingan output/tahap dan garis untuk seri waktu yang memang kontinu. Garis aktual solid, estimasi putus-putus; missing data menjadi gap, bukan dihubungkan seolah tersedia.

Palet seri cyan/magenta/kuning/violet disertai label/marker. Tidak mencampur pcs, paket, dan rupiah pada satu sumbu. Tersedia tabel/ringkasan data untuk pengguna yang tidak dapat membaca grafik. Tidak ada animasi terus menerus atau gradient yang menutupi titik data.

## 10. Tampilan per pekerjaan

| Layar | Informasi utama | Aksi dan batas |
|---|---|---|
| Order & Pengiriman | Seller, item, reservasi, penghambat paket, pickup | Validasi/revisi; siap kirim hanya jika semua item lengkap |
| Pekerjaan Saya | Antrean siap, aktif, hambatan, hasil parsial | Mulai, simpan hasil, tandai hambatan, serahkan; prioritas tidak diubah tanpa hak |
| Produksi & Vendor | Tahap, lot, keluar/kembali vendor, jumlah tersisa, due awal/revisi | Catat keluar/kembali; QC hasil kembali terpisah |
| Stok & PPIC | Fisik sumber, alokasi, tersedia, WIP, exclusive/shared, freshness | Usul restock/rekonsiliasi; tidak menyebut WIP sebagai ready stock |
| Keputusan Admin | Usulan, nilai/modal, kapasitas, pending terbantu, risiko sisa | Setujui/tolak/ubah dengan alasan dan pemeriksaan data terbaru |
| Laporan | Periode, definisi, sumber, cakupan, revisi | Drilldown dan ekspor sesuai akses |

### 10.1 Meja keputusan stok

Bagian kiri daftar SKU dengan kategori stabil/baru/naik/menurun/jarang; kategori belum otomatis diberi label “ditetapkan PPIC”. Bagian kanan detail rekomendasi: permintaan 7 hari dan pembanding, stok bruto/alokasi, pending, WIP tepat waktu, lead time, jumlah usulan, dampak modal, risiko, dan asumsi.

Pisahkan “kekurangan sebelum restock selesai” dari “saldo akhir horizon”. Usulan jumlah 5 pcs tidak berarti seluruh order hari ini terselamatkan. Nilai nol dan tidak cukup data dibedakan. Shared/exclusive memakai ikon/label, bukan warna saja.

### 10.2 Pickup dan ETA

Timeline harian 13.00 dan 16.00 sesuai jadwal terkonfirmasi. 18.00 memakai outline/dashed + “Menunggu konfirmasi” sampai disahkan. Setiap paket memiliki “Siap diperkirakan”, “Pickup kandidat”, dan “Status konfirmasi”.

Desain/cutting belum diketahui → “Estimasi belum tersedia” dan alasan. Tidak membuat countdown palsu. Paket siap yang melewatkan pickup tetap “Siap, belum terkirim”; warna sukses hanya untuk kejadian sukses yang benar.

### 10.3 AI

Panel sekunder “Ringkasan AI” dapat dilipat. Struktur: fakta dari data → dugaan penyebab → usulan → sumber/waktu. Tautan hanya ke objek yang berhak dibuka pengguna. Tidak ada tombol “AI perbaiki semua” atau akses write langsung. Error AI tidak memblokir pencatatan kerja; angka dashboard berasal dari mesin hitung.

## 11. State sistem dan microcopy

| State | Perlakuan visual/copy | Perilaku |
|---|---|---|
| Loading | Skeleton sederhana, “Memuat order…” | Jangan tampil nol sementara |
| Empty pertama | “Belum ada order pada periode ini” | Aksi impor hanya untuk pengguna berhak |
| Filter tanpa hasil | “Tidak ada hasil untuk filter ini” | Tombol reset filter |
| Data tidak lengkap | Badge netral/kuning + field yang belum ada | Angka sah tetap terlihat; jangan substitusi tebakan |
| Integrasi usang | Banner “Data stok terakhir …; perlu konfirmasi” | Komitmen mengikuti mode FRD/TRD |
| Simpan belum pasti | “Hasil penyimpanan belum terkonfirmasi” | Periksa status command sebelum retry; jangan minta input ulang bebas |
| Konflik versi | Banner inline dengan muat ulang | Pertahankan input yang aman dan tampilkan perubahan |
| Validasi gagal | Ringkasan + pesan field | Fokus ke error pertama; data tidak hilang |
| Akses ditolak | “Akses tindakan ini tidak tersedia untuk peran Anda” | Tidak membocorkan data yang dilindungi |
| Sukses | Feedback pendek “Hasil tersimpan” + jumlah | Update hanya setelah commit; detail riwayat tersedia |
| Partial success | Jumlah berhasil/gagal + daftar alasan | Retry hanya yang belum berhasil |

Notifikasi bisnis memiliki PIC dan tindakan. Menandai notifikasi dibaca tidak menyelesaikan hambatan. Kasus aktif diperbarui pada kartu yang sama, bukan toast berulang setiap polling.

## 12. Aksesibilitas dan penggunaan lapangan

Target desain: rasio kontras minimal 4,5:1 untuk teks normal, 3:1 untuk teks besar dan batas kontrol penting. Nilai token adalah kandidat; validasi seluruh pasangan state hover/disabled/focus, bukan mengklaim lulus hanya dari warna dasar.

- Keyboard dapat mencapai navigasi, filter, tabel, dialog, dan semua aksi; focus terlihat.
- Dialog mengelola fokus, dapat ditutup sesuai konteks, dan mengembalikan fokus ke pemicu. Kesalahan form diumumkan tanpa mengandalkan warna.
- Tombol utama 44 px; label eksplisit; tooltip bukan satu-satunya lokasi informasi wajib.
- Zoom 200% tetap memungkinkan pekerjaan tanpa tombol terpotong atau tertutup topbar/sticky footer.
- Konfirmasi destruktif menyebut objek dan dampaknya; tidak mengandalkan gesture/hover.
- Screen reader mendapat label kontrol, judul tabel, arah sort, dan status simpan. Pembaruan rutin tidak membacakan ulang seluruh dashboard.
- Reduced-motion dihormati. Tidak ada blinking untuk stockout/urgent.
- Uji di komputer divisi dengan pencahayaan nyata; tema gelap mengikuti referensi, tema terang belum termasuk deliverable versi ini.

## 13. Aset dan implementasi visual

- Gunakan satu keluarga ikon outline 20–24 px; Material Symbols Outlined mengikuti referensi, aset/lisensi diperiksa saat implementasi. Ikon berfungsi menjelaskan, bukan menggantikan label aksi kritis.
- Thumbnail SKU dari produk nyata bila tersedia; placeholder netral dengan SKU/ukuran jika tidak. Foto stok dari template tidak dijadikan produk NCK.
- Motif gelombang hanya di header/kartu brand, opacity rendah, tidak di belakang tabel/form; maksimum satu area motif dominan per layar.
- Tokens dipetakan ke CSS custom properties atau sistem styling yang dipilih. Panduan tidak mengharuskan Tailwind CDN dari HTML sumber dan tetap kompatibel dengan template Django/TRD.
- Semua state komponen menggunakan token semantik, bukan hex acak per halaman. Breakpoint, radius, dan spacing di bagian 6 menjadi acuan tunggal.
- Jangan menyalin remote URL avatar/logo template, inline angka dummy, script CDN, atau klaim sensor sebagai kebutuhan aplikasi.
- Seed/demo diberi label “Data contoh” pada seluruh layar dan ekspor terkait. Nama seller/pengguna contoh tidak menjadi master produksi.

## 14. Pemetaan perubahan dari template

| Elemen template | Keputusan adaptasi |
|---|---|
| Hero slogan besar dan tombol cek mesin | Header operasional ringkas; tidak ada cek mesin tanpa fitur/data |
| Syne dominan pada semua angka dan label | Syne untuk judul/KPI; body font untuk angka panjang dan tabel |
| Metadata pink kecil dan uppercase panjang | Metadata netral, ukuran terbaca, sentence case |
| 142 SPK, 3.450/4.000 pcs, Rp184,5M, 99,4% QC | Seluruhnya dummy; tidak ditransfer sebagai baseline NCK |
| Mesin aktif, suhu 208°C, utilisasi 91,8% | Dihilangkan sampai ada sumber dan fitur terverifikasi |
| Lima tahap generik termasuk sablon | Jalur sesuai ready stock/DTF/jersey, cutting dan vendor terlihat |
| Label realtime dan pulse dot | Waktu update nyata, kondisi koneksi dan data dipisah |
| Layanan unggulan dan tombol hubungi CS | Risiko stok/rekomendasi/keputusan internal |
| Prioritas otomatis lewat warna | Label urutan/exception admin + alasan; warna hanya pendukung |
| Logo/avatars remote | Aset resmi lokal dan identitas pengguna nyata |
| Scrollbar tersembunyi | Scrollbar container terlihat dan dapat dioperasikan |
| Tombol buat SPK bebas | Aksi sesuai role dan asal kebutuhan order/restock yang disetujui |

## 15. Checklist review desain sebelum coding UI

1. Dashboard menampilkan same-day, pending, pickup, risiko stok, PIC, dan freshness; bukan hanya volume/omzet.
2. Operator bisa menemukan pekerjaan siap dan mencatat hasil parsial tanpa membuka dashboard manajemen.
3. Satu resi multi-SKU tidak terlihat siap saat satu item belum lengkap.
4. Shared/exclusive, fisik/alokasi/WIP, dan estimasi/aktual terlihat berbeda.
5. Admin melihat dampak dan alasan sebelum persetujuan; data usang memicu review ulang.
6. Nilai yang hilang, nol, usang, dan gagal dimuat mempunyai state berbeda.
7. Kontras, keyboard, zoom, format angka, dan target klik diperiksa pada state nyata.
8. Layout diperiksa pada 1440, 1280, 1024, 768, dan 390 px; tidak ada header/tombol/angka uang terpotong.
9. UAT visual mengacu FRD U03–U08, U10–U17, U20–U26 yang relevan; layout tidak mengubah aturan transaksi.
10. Semua dummy, angka sensor, kapasitas tak tervalidasi, dan link aset eksternal contoh dihapus/diberi label sebelum review implementasi.

Belum ada mockup baru atau audit kontras/render aplikasi yang dijalankan. Referensi PNG sudah diperiksa secara visual; HTML dan DESIGN.md sumber telah dibaca sebagai bahan adaptasi. Keputusan logo turunan, aset final, dan validasi lapangan diselesaikan pada tahap desain UI berikutnya.

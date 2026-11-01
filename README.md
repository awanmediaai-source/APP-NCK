# NCK Operations Control Center

Pilot aplikasi internal PT Nusa Cipta Kreasi: order B2B, stok/reservasi FIFO, produksi/vendor, QC, pengiriman, keputusan restock dan laporan. Asisten NCK mendukung OpenAI dan Gemini, dengan mode referensi lokal saat API belum dikonfigurasi.

- [Source dan panduan aplikasi](apps/nck-operations/README.md)
- [Catatan implementasi dan pengujian](apps/nck-operations/IMPLEMENTATION.md)
- [BRD](output/nck-planning/BRD-NCK-v0.1.md), [PRD](output/nck-planning/PRD-NCK-v0.1.md), [FRD](output/nck-planning/FRD-NCK-v0.1.md), [TRD](output/nck-planning/TRD-NCK-v0.1.md)
- [Panduan desain](output/nck-planning/design.md)

## Lingkungan lokal

Python 3.12, PostgreSQL 17, Django 5.2. Dependensi terkunci dalam `apps/nck-operations/requirements.lock.txt`.

Launcher MacBook yang ada memakai runtime di `.tools/nck-runtime` pada root checkout. Runtime tidak disertakan. Untuk checkout baru, siapkan runtime itu dengan micromamba/conda dari conda-forge (`python=3.12 postgresql=17 pip`), lalu instal dependensi:

```sh
.tools/nck-runtime/bin/python -m pip install -r apps/nck-operations/requirements.lock.txt
./apps/nck-operations/start.command
```

Buka http://127.0.0.1:8000. Data contoh dibuat sekali; akun demo/password dijelaskan dalam panduan aplikasi. Database, API key dan Django secret dibuat/disimpan lokal dan tidak dilacak Git.

## Batas pilot

Hanya untuk evaluasi lokal menggunakan data contoh. Belum siap untuk data pelanggan nyata atau diekspos ke internet. Integrasi BigSeller dan pembukuan aktual belum aktif; koneksi AI memerlukan API key/model milik pengguna. Belum diuji pada skala produksi. Dokumen perencanaan menjelaskan target, bukan klaim semua fitur sudah selesai.

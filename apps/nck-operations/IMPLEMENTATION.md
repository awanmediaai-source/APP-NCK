# Catatan implementasi — 1 November 2026

Status: **pilot aplikasi lokal berjalan**, bukan seluruh FRD selesai atau siap produksi.

## Sudah terverifikasi

- 19 tes Django/PostgreSQL lulus, system check tanpa masalah.
- Tes transaksi bersamaan menggunakan koneksi/thread berbeda: satu unit stok tidak terreservasi dua kali, order FIFO memperoleh unit pertama.
- Deduplikasi resi/sumber, idempotency dengan payload fingerprint, konflik versi, batas kuantitas, exclusivity, multi-SKU packing gate, CSRF dan otorisasi server diuji.
- Hasil parsial, transfer/penerimaan terpisah, rework tanpa unit ganda, vendor return sebelum QC, pembatalan yang mempertahankan WIP, biaya snapshot, dan pickup 18.00 bersyarat diuji.
- Formula U18 diuji melalui service nyata: K12/F20/S10/W5 menghasilkan usulan 5. WIP yang tidak tercatat ditolak, WIP yang berpindah tahap tidak dihitung dua kali.
- Persetujuan berulang tidak membuat pekerjaan kedua. Perubahan data setelah usulan memblokir approval lama.
- Browser end-to-end akun admin: order `DEMO-QA-RESI-001` berisi dua SKU, picking → hasil QC masing-masing → packing → handover dengan bukti → status Terkirim. Jejak ini sengaja tetap berada dalam dataset contoh.
- Semua delapan halaman tersedia. Pencarian order dan penambahan baris SKU dicoba di browser.
- Dashboard diperiksa pada 390, 768, 1024, 1280, 1440 px; document width sama dengan viewport. Tabel panjang memakai scroll container.
- Audit axe WCAG 2A/AA dashboard: 0 violation; contrast teks SVG grafik membutuhkan review manual. Teks grafik memakai warna sekunder pada panel gelap. Ini bukan sertifikasi aksesibilitas seluruh aplikasi.
- Server di-restart dalam proses pengembangan; order contoh tetap tersimpan di PostgreSQL.

## Bukti visual

- `../../output/nck-planning/nck-dashboard-local.png`
- `../../output/nck-planning/nck-production-local.png`
- `../../output/nck-planning/nck-mobile-local.png`

## Batas yang belum diuji / belum dibuat

Belum ada load test, uji di komputer divisi nyata, integrasi BigSeller, backup/restore, worker/outbox, AI, forecast otomatis, ETA finite-capacity, pembukuan aktual, ataupun validasi seluruh U01–U26. Snapshot/sinkronisasi U14/U21 belum relevan karena integrasi belum dibuat. Tidak ada klaim dukungan kapasitas 100.000 pcs/bulan.

Keputusan yang masih manual: validasi forecast 7 hari dan WIP tepat waktu oleh PPIC. Sistem menampilkan asumsi dan mengikat approval pada versi data. Lock global dan invalidasi rekomendasi global dibuat konservatif untuk pilot; optimasi per SKU memerlukan benchmark dan tes tambahan.

Lihat README untuk alur, akun, cara menjalankan, dan daftar fitur ditunda. BRD/PRD/FRD/TRD/design.md tidak ditimpa atau dinyatakan selesai secara sepihak.

## Iterasi Asisten NCK

- Panel kanan bawah di seluruh halaman setelah login, default ChatGPT (OpenAI), pilihan Gemini.
- Basis pengetahuan NCK + retrieval kata kunci dari BRD/PRD/FRD + snapshot dengan filter akses server. Bukan indeks seluruh Obsidian.
- Mode tanpa key menyebut referensi lokal secara eksplisit, tanpa network call. Adapter dua penyedia siap dikonfigurasi melalui `configure-ai.command`.
- Total 25 tes backend lulus setelah penambahan, termasuk format API via mock dan isolasi biaya operator.
- Browser: login, panel, pertanyaan contoh, respons referensi, ganti Gemini, reload kembali default OpenAI, desktop 1440 dan mobile 390 tanpa overflow horizontal. Axe panel: 0 violation; kontras gradient masih ditandai untuk review manual, bukan sertifikasi.
- Koneksi model live, akurasi jawaban model, kuota dan kredensial belum diverifikasi karena API key belum tersedia. Chat memori tab, tidak memiliki penyimpanan percakapan permanen atau aksi transaksi.

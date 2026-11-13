# Sidang Q&A prep

## Q: "Rata-rata 5,46% dan median 2,44%, itu dihitung dari mana?"

Dihitung dari 2.002 mask di folder Segmentation_Masks, bukan dari CSV persentase bawaan dataset. Setiap mask
dibinerkan dengan threshold 127, lalu luas plastik satu citra = jumlah piksel plastik dibagi 921.600 piksel
(1280 × 720). Rata-rata dari 2.002 nilai tersebut adalah 5,46%. Karena ukuran semua citra sama, angka ini juga
berarti 5,46% dari seluruh piksel dataset adalah plastik, atau sekitar 17 piksel latar belakang untuk setiap
piksel plastik.

Median 2,44% hanya dihitung dari 1.478 citra yang mask-nya memiliki minimal satu piksel plastik (524 mask kosong
tidak diikutkan). Median dipakai karena distribusinya miring ke kanan: rata-rata citra berplastik 7,39%, tetapi
ada citra dengan luas sampai 81,91% yang menaikkan rata-rata. Median menunjukkan bahwa citra berplastik yang
umum hanya berisi sekitar 2,4% plastik.

Jebakan yang mungkin ditanya:
- 1.478 (mask tidak kosong) ≠ 1.482 (label "yes"): ada 8 + 4 citra yang label dan mask-nya tidak sesuai.
  Median berdasarkan label "yes" = 2,42%.
- CSV bawaan dataset memberi rata-rata 5,38%, karena nilainya dibulatkan 2 desimal per citra.
- pos_weight 18,37 dihitung dari 200 citra latih acak, sehingga sedikit berbeda dari rasio 17,3 pada seluruh dataset.

## Q: "Kenapa harus normalisasi?"

Normalisasi mengubah nilai piksel 0–255 menjadi nilai di sekitar 0 dengan skala yang sama pada ketiga kanal.
Masukan yang terpusat di nol dan berskala sama membuat gradien lebih stabil dan pelatihan lebih cepat konvergen
(LeCun et al., 1998, "Efficient BackProp"). Alasan utama pada penelitian ini adalah bobot pretrained: lapisan
pertama encoder dan statistik normalisasinya dipelajari dari masukan yang dinormalisasi dengan mean dan std
tertentu. Jika distribusi masukan berbeda, fitur yang dihasilkan encoder juga bergeser.

## Q: "Kenapa harus ImageNet?"

1. Encoder yang dipakai (nvidia/mit-b3, MiT-B0/B5, ResNet-34/50/101 dari Segmentation Models PyTorch) dilatih
   pada ImageNet-1K dengan mean (0,485; 0,456; 0,406) dan std (0,229; 0,224; 0,225).
2. Bobot aerial, ADE20K, dan drone adalah hasil fine-tuning dari encoder MiT-B3 yang sama, yang awalnya dilatih
   pada ImageNet. Jadi satu nilai mean dan std cocok untuk semua bobot.
3. Learning rate encoder hanya 1e-5, sehingga encoder hampir tidak sempat menyesuaikan diri jika distribusi
   masukannya diubah.
4. Normalisasi adalah variabel kontrol. Dengan nilai yang sama pada 17 model, perbedaan hasil hanya berasal dari
   arsitektur, encoder, dan bobot awal. Model tanpa pretrained juga memakai nilai yang sama supaya adil. Untuk model
   ini nilai persisnya tidak terlalu berpengaruh, selama masukan terpusat dan berskala.
5. Aplikasi (server FastAPI) memakai nilai yang sama, sehingga masukan saat inference sama dengan saat pelatihan.

Kalau ditanya "kenapa tidak pakai mean/std FloPWD sendiri?": mean FloPWD (0,456; 0,467; 0,413) dan std
(0,174; 0,173; 0,177). Rata-ratanya mirip ImageNet, std-nya lebih kecil. Mean/std dataset sendiri lebih berguna
ketika melatih dari awal atau ketika datanya bukan RGB biasa (misalnya multispektral). Pada fine-tuning, yang
penting adalah masukan sesuai dengan yang diharapkan bobot pretrained.

## Q: "Kalau normalisasi di-skip, jadinya gimana?"

Ini tidak diuji dengan eksperimen pada penelitian ini, jadi jawabannya berdasarkan teori:
- Jika A.Normalize dihapus begitu saja, ToTensorV2 menghasilkan tensor uint8 bernilai 0–255 dan model langsung
  error karena tipe data tidak sesuai.
- Jika diubah ke float tanpa dibagi 255, nilai masukan sekitar 100 kali lebih besar dari rentang normalisasi
  (sekitar −2,1 sampai 2,6). Aktivasi awal membesar, fitur pretrained tidak bermakna, dan dengan AMP fp16 bisa
  terjadi overflow (NaN). Keunggulan bobot pretrained (0,47 → 0,82 mIoU) kemungkinan besar hilang.
- Jika hanya dibagi 255 (rentang 0–1) tanpa mean/std, model masih bisa dilatih karena LayerNorm pada MiT ikut
  menyesuaikan, tetapi masukan bergeser dari distribusi pretrained. Biasanya konvergensinya lebih lambat dan
  hasilnya sedikit lebih rendah.

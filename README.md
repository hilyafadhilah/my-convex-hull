# Tugas Kecil 2 IF2211 Strategi Algoritma 2021/2022

13520024 Hilya Fadhilah Imania

## Deskripsi Singkat

Program ini adalah program pencarian convex hull untuk tes linear
separability dataset dengan algoritma divide and conquer. Program
menggunakan dataset yang disediakan oleh sklearn, yaitu dataset
Iris, Digits, Wine, dan Breast Cancer.

## Algoritma

1. Ambil dua titik dengan nilai absis terkecil dan terbesar, kemudian
   tarik garis sebagai garis dasar atau base line. Dua titik tersebut merupakan
   bagian dari himpunan solusi. Garis yang dibentuk akan membagi titik-titik
   menjadi area “atas” dan “bawah”. 

2. Untuk memeriksa apakah suatu titik `(x3, y3)` berada di sebelah “kiri” atau
   “atas” suatu garis `((x1, y1), (x2, y2))`, gunakan rumus determinan,
   dengan hasil positif menandakan titik berada di kiri, hasil negatif menandakan
   titik berada di kanan, dan hasil nol menandakan titik berada pada garis.

3. Untuk suatu area yang dibatasi `p1` dan `p2`, terdapat dua kemungkinan,
   yakni: (a) Jika tidak ada titik lain selain pembentuk garis, maka titik pembentuk
   garis adalah bagian dari himpunan solusi convex hull; (b) Jika masih ada titik
   lain, pilih titik `p_max` yang memiliki jarak terjauh dari garis. Jika terdapat
   sekumpulan titik dengan jarak yang terjauh, pilih titik yang membentuk sudut
   terbesar jika dihubungkan dengan garis.
 
4. Hubungkan `p1` dan `p_max` sehingga area di sebelah kirinya menjadi area
   kiri. Hubungkan `p2` dan `p_max` sehingga area di sebelah kanannya menjadi
   area kanan. Bagi titik dengan rumus determinan di atas dan tinjau masing-masing
   area kiri dan kanan dengan langkah 3-4. Bagian tengah tidak perlu diperiksa
   karena tidak mungkin menjadi bagian dari convex hull.

5. Ulangi langkah 3-4 untuk semua bagian yang ada, hingga tidak ada lagi titik
   selain pembentuk garis. Kembalikan pasangan titik yang membentuk convex hull.

## Requirements dan Instalasi

Program ditulis dalam bahasa Python 3.10.
Instalasi dilakukan dengan utility `pipenv` versi 2022.
Pada direktori utama repository ini, jalankan perintah berikut:

```
$ pipenv install
```

## Menjalankan Program

```
$ pipenv run py src/main.py
```

Note: Warna grafik yang dihasilkan adalah random, sehingga untuk
mendapatkan warna yang enak dipandang, jalankan program beberapa kali
hingga didapat hasil yang memuaskan.

## License

[MIT](https://opensource.org/licenses/MIT)

Copyright (C) 2022, Hilya Fadhilah Imania

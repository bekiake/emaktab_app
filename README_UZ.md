# eMaktab Avtomatik Kirish Ilovasi

## Qisqacha tavsif
Bu Android ilovasi CSV faylidagi barcha foydalanuvchilar uchun avtomatik ravishda eMaktab tizimiga kirishni amalga oshiradi.

## Nima qiladi?
- ✅ Oddiy interfeys - faqat bitta "Tizimga kirish" tugmasi
- ✅ CSV fayldagi barcha foydalanuvchilar uchun avtomatik kirish
- ✅ Jarayon va natijalarni real vaqtda ko'rsatish
- ✅ Muvaffaqiyatli va muvaffaqiyatsiz urinishlar haqida to'liq hisobot

## Fayllar tuzilishi
```
emaktab_app/
├── main.py              # Asosiy dastur fayli
├── buildozer.spec       # APK yasash uchun sozlamalar
├── credentials.csv      # Login va parollar fayli
├── test_app.bat         # Windows'da test qilish uchun
└── build_instructions.md # To'liq yo'riqnoma
```

## CSV fayl formati
`credentials.csv` faylida login va parollar tab bilan ajratilgan bo'lishi kerak:
```
foydalanuvchi1    parol1
foydalanuvchi2    parol2
foydalanuvchi3    parol3
```

## Windows'da test qilish

1. **Python o'rnating** (agar o'rnatilmagan bo'lsa):
   - https://python.org dan Python 3.8+ yuklab oling
   - O'rnatishda "Add to PATH" ni belgilang

2. **Test_app.bat ni ishga tushiring:**
   ```
   emaktab_app papkasiga kiring
   test_app.bat faylini ikki marta bosing
   ```

## APK fayl yasash

### Linux yoki Docker orqali (tavsiya etiladi):

1. **Ubuntu/Debian da:**
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user buildozer
cd emaktab_app/
buildozer android debug
```

2. **Docker orqali (Windows/Mac/Linux):**
```bash
cd emaktab_app/
docker run --rm -v ${PWD}:/home/user/app kivy/buildozer android debug
```

### APK fayl joylashuvi:
Muvaffaqiyatli yasashdan keyin APK fayl bu yerda bo'ladi:
```
emaktab_app/bin/emaktablogin-1.0-arm64-v8a-debug.apk
```

## Androidga o'rnatish

1. APK faylni Android qurilmasiga nusxalang
2. Sozlamalarda "Noma'lum manbalardan o'rnatish"ga ruxsat bering
3. APK faylni oching va ilovani o'rnating

## Foydalanish

1. "eMaktab Login" ilovasini oching
2. Internet ulanishini tekshiring
3. "Tizimga kirish" tugmasini bosing
4. Jarayon tugashini kuting
5. Natijalarni pastga siljitib ko'ring

## Xavfsizlik

⚠️ **Muhim:** credentials.csv faylida parollar ochiq holda saqlanadi:
- CSV faylni begona shaxslarga bermang
- Ishlatganingizdan keyin CSV faylni o'chiring (kerak bo'lsa)
- Faqat ishonchli qurilmalarda ishlating

## Muammolarni hal qilish

### "credentials.csv topilmadi" xatosi
- Fayl main.py bilan bir papkada ekanligini tekshiring
- Fayl formatini tekshiring (UTF-8, tab ajratgich)

### Kirish xatolari
- CSV dagi login va parollarni tekshiring
- Internet ulanishini tekshiring
- eMaktab sayti vaqtincha ishlamasligi mumkin

## Yordam

Qo'shimcha yordam uchun build_instructions.md faylini o'qing (ingliz tilida to'liq yo'riqnoma).
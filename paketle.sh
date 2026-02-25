#!/bin/bash

# --- Ayarlar ---
APP_NAME="siyer"
PKG_DIR="siyeri-nebi"
VERSION="1.0.0"
MAINTAINER="mobilturka"

echo "🚀 Mobilturka $APP_NAME .deb paketi hazırlama işlemi başladı..."

# 1. Eski kalıntıları temizle ve klasör yapısını kur
rm -rf $PKG_DIR
mkdir -p $PKG_DIR/DEBIAN
mkdir -p $PKG_DIR/opt/$APP_NAME
mkdir -p $PKG_DIR/usr/share/applications
mkdir -p $PKG_DIR/usr/share/pixmaps

# 2. Python dosyasını ve JSON verilerini kopyala
# Not: Mevcut dizindeki siyer.py ve *.json dosyalarını alır
cp siyer.py $PKG_DIR/opt/$APP_NAME/
cp *.json $PKG_DIR/opt/$APP_NAME/

# 3. İkonu kopyala
if [ -f "icon.png" ]; then
    cp icon.png $PKG_DIR/usr/share/pixmaps/siyer-icon.png
else
    echo "⚠️ Uyarı: icon.png bulunamadı!"
fi

# 4. DEBIAN/control dosyasını oluştur
cat <<EOF > $PKG_DIR/DEBIAN/control
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Maintainer: $MAINTAINER
Depends: python3, python3-pyqt6
Description: Kronolojik Siyer-i Nebi Uygulamasi
 Mobilturka tarafindan hazirlanan, Efendimiz'in hayatini
 kronolojik olarak sunan görsel rehber.
EOF

# 5. Masaüstü kısayolunu (.desktop) oluştur
cat <<EOF > $PKG_DIR/usr/share/applications/siyer.desktop
[Desktop Entry]
Name=Siyer-i Nebi
Exec=python3 /opt/siyer/siyer.py
Icon=siyer-icon
Type=Application
Categories=Education;
Terminal=false
Comment=Kronolojik Siyer-i Nebi Rehberi
EOF

# 6. İzinleri ayarla (Güvenlik ve standartlar için kritik)
chmod -R 755 $PKG_DIR/DEBIAN
chmod -R 755 $PKG_DIR/opt/$APP_NAME
chmod 644 $PKG_DIR/usr/share/applications/siyer.desktop

# 7. Paketi oluştur
dpkg-deb --build $PKG_DIR

# 8. Çıktı dosyasını isimlendir ve temizle
FINAL_NAME="${APP_NAME}_${VERSION}.deb"
mv ${PKG_DIR}.deb $FINAL_NAME
# rm -rf $PKG_DIR # İstersen çalışma klasörünü silebilirsin

echo "-------------------------------------------"
echo "✅ İşlem Başarıyla Tamamlandı!"
echo "📦 Paket: $FINAL_NAME"
echo "🛠 Kurmak için: sudo dpkg -i $FINAL_NAME"
echo "-------------------------------------------"
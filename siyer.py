import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QListWidgetItem, 
                             QLabel, QTextBrowser, QLineEdit, QFrame, QGraphicsDropShadowEffect, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor

class SiyerAppFinal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kronolojik Siyer-i Nebi")
        self.setMinimumSize(1300, 900)
        
        self.all_data = []
        self.load_data()
        
        # Tema durumu takibi
        palette = QApplication.palette()
        self.is_dark = palette.window().color().lightness() < 128
        
        self.init_ui()
        self.apply_theme()
        self.center_on_screen()

    def load_data(self):
        # Scriptin bulunduğu dizini bul (Örn: /opt/siyer/)
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        for i in range(1, 6):
            file_name = os.path.join(base_path, f"{i}.json")
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as f:
                    self.all_data.extend(json.load(f))
            else:
                print(f"Hata: {file_name} bulunamadı!")
        
        # Yıla göre sırala
        self.all_data.sort(key=lambda x: int(x['yil']))

    def center_on_screen(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()
        current_item = self.event_list.currentItem()
        if current_item:
            self.display_details(current_item)

    def apply_theme(self):
        if self.is_dark:
            self.colors = {
                "bg": "#0D1B1E", "card": "#162B2B", "item": "#1F3A3A",
                "text": "#D1E8E2", "accent": "#4DB6AC", "border": "#254141"
            }
            self.theme_btn.setText("☀️ Aydınlık")
        else:
            self.colors = {
                "bg": "#E0F2F1", "card": "#F1F5F4", "item": "#FFFFFF",
                "text": "#2D413E", "accent": "#26A69A", "border": "#B2DFDB"
            }
            self.theme_btn.setText("🌙 Koyu")
            
        self.setStyleSheet(f"background-color: {self.colors['bg']};")
        self.update_styles()

    def update_styles(self):
        card_css = f"background-color: {self.colors['card']}; border-radius: 40px; border: 1px solid {self.colors['border']};"
        self.left_card.setStyleSheet(card_css)
        self.right_card.setStyleSheet(card_css)
        
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['item']};
                border: 2px solid {self.colors['accent']};
                border-radius: 20px;
                padding: 15px 25px;
                color: {self.colors['text']};
                font-size: 14pt;
            }}
        """)
        
        self.event_list.setStyleSheet(f"""
            QListWidget {{ background: transparent; border: none; outline: none; }}
            QListWidget::item {{
                background-color: {self.colors['item']};
                border-radius: 20px;
                padding: 22px;
                margin-bottom: 15px;
                color: {self.colors['text']};
                border: 1px solid {self.colors['border']};
                font-size: 15pt;
                font-weight: 500;
            }}
            QListWidget::item:selected {{
                background-color: {self.colors['accent']};
                color: white;
                border: 1px solid {self.colors['accent']};
            }}
        """)
        
        self.title_label.setStyleSheet(f"color: {self.colors['text']}; font-weight: bold; font-size: 26pt; line-height: 1.2;")
        
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['card']};
                color: {self.colors['accent']};
                border: 1px solid {self.colors['border']};
                border-radius: 20px;
                padding: 10px 40px;
                font-weight: bold;
                font-size: 12pt;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent']};
                color: white;
            }}
        """)
        
        if hasattr(self, 'sep'):
            self.sep.setStyleSheet(f"background-color: {self.colors['accent']}; opacity: 0.3;")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Ana Dikey Düzen (Buton Üstte, Kartlar Altta)
        outer_layout = QVBoxLayout(central_widget)
        outer_layout.setContentsMargins(40, 20, 40, 40)
        outer_layout.setSpacing(20)

        # 1. BÖLÜM: Çerçevenin Dışındaki Orta Buton
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        self.theme_btn = QPushButton("Tema Değiştir")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        btn_container.addWidget(self.theme_btn)
        btn_container.addStretch()
        outer_layout.addLayout(btn_container)

        # 2. BÖLÜM: Yatay Kart Düzeni
        content_layout = QHBoxLayout()
        content_layout.setSpacing(40)

        # --- SOL PANEL ---
        self.left_card = QFrame()
        left_layout = QVBoxLayout(self.left_card)
        left_layout.setContentsMargins(25, 40, 25, 40)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Yıl veya metin ile ara...")
        self.search_bar.textChanged.connect(self.filter_list)
        left_layout.addWidget(self.search_bar)

        self.event_list = QListWidget()
        self.event_list.itemClicked.connect(self.display_details)
        left_layout.addWidget(self.event_list)

        # --- SAĞ PANEL ---
        self.right_card = QFrame()
        right_layout = QVBoxLayout(self.right_card)
        right_layout.setContentsMargins(80, 80, 80, 80)

        self.title_label = QLabel("Hz Muhammed (SAV)")
        self.title_label.setWordWrap(True)

        self.sep = QFrame()
        self.sep.setFixedHeight(3)
        
        self.detail_text = QTextBrowser()
        self.detail_text.setFont(QFont("Georgia", 18))
        self.detail_text.setStyleSheet("border: none; background: transparent;")

        right_layout.addWidget(self.title_label)
        right_layout.addSpacing(25)
        right_layout.addWidget(self.sep)
        right_layout.addSpacing(50)
        right_layout.addWidget(self.detail_text)

        content_layout.addWidget(self.left_card, 38)
        content_layout.addWidget(self.right_card, 62)
        
        outer_layout.addLayout(content_layout)

        for card in [self.left_card, self.right_card]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(50)
            shadow.setColor(QColor(0, 0, 0, 35))
            shadow.setOffset(0, 15)
            card.setGraphicsEffect(shadow)

        self.update_ui_list(self.all_data)

    def update_ui_list(self, data):
        self.event_list.clear()
        for item in data:
            li = QListWidgetItem(f" {item['yil']}   |   {item['baslik']}")
            li.setData(Qt.ItemDataRole.UserRole, item)
            li.setSizeHint(QSize(0, 95))
            self.event_list.addItem(li)

    def filter_list(self, text):
        search = text.lower()
        filtered = [i for i in self.all_data if search in i['baslik'].lower() or search in i['detay'].lower() or search in i['yil']]
        self.update_ui_list(filtered)

    def display_details(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        self.title_label.setText(data['baslik'])
        
        html = f"""
        <div style='color: {self.colors['text']}; line-height: 1.8; text-align: justify; font-family: "Georgia";'>
            {data['detay']}
        </div>
        """
        self.detail_text.setHtml(html)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Sans Serif", 12))
    window = SiyerAppFinal()
    window.show()
    sys.exit(app.exec())
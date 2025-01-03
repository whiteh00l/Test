import sys
import qrcode
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, 
                           QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class BookCurationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('책 큐레이션 프로그램')
        self.setGeometry(100, 100, 800, 600)
        
        # 메인 위젯 생성
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 메인 레이아웃
        layout = QVBoxLayout()
        
        # 책 정보 입력 섹션
        info_layout = QVBoxLayout()
        
        # 책 제목
        title_layout = QHBoxLayout()
        title_label = QLabel('책 제목:')
        self.title_input = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        
        # 저자
        author_layout = QHBoxLayout()
        author_label = QLabel('저자:')
        self.author_input = QLineEdit()
        author_layout.addWidget(author_label)
        author_layout.addWidget(self.author_input)
        
        # URL
        url_layout = QHBoxLayout()
        url_label = QLabel('URL:')
        self.url_input = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        
        # 책 소개
        review_label = QLabel('책 소개:')
        self.review_input = QTextEdit()
        
        # 버튼들
        button_layout = QHBoxLayout()
        self.create_html_btn = QPushButton('HTML 생성')
        self.create_qr_btn = QPushButton('QR코드 생성')
        self.save_feedback_btn = QPushButton('피드백 저장')
        
        button_layout.addWidget(self.create_html_btn)
        button_layout.addWidget(self.create_qr_btn)
        button_layout.addWidget(self.save_feedback_btn)
        
        # 레이아웃에 위젯 추가
        info_layout.addLayout(title_layout)
        info_layout.addLayout(author_layout)
        info_layout.addLayout(url_layout)
        info_layout.addWidget(review_label)
        info_layout.addWidget(self.review_input)
        info_layout.addLayout(button_layout)
        
        # QR 코드 이미지 표시 영역
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        
        # 메인 레이아웃에 추가
        layout.addLayout(info_layout)
        layout.addWidget(self.qr_label)
        
        # 버튼 이벤트 연결
        self.create_html_btn.clicked.connect(self.create_html)
        self.create_qr_btn.clicked.connect(self.create_qr)
        self.save_feedback_btn.clicked.connect(self.save_feedback)
        
        main_widget.setLayout(layout)
        
    def create_html(self):
        """HTML 파일 생성"""
        if not self.title_input.text() or not self.author_input.text() or not self.review_input.toPlainText():
            QMessageBox.warning(self, '경고', '모든 필드를 입력해주세요.')
            return
            
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>{self.title_input.text()} - 책 소개</title>
            <style>
                body {{ font-family: 'Nanum Gothic', sans-serif; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .book-info {{ background: #f9f9f9; padding: 20px; border-radius: 10px; }}
                .book-title {{ color: #333; font-size: 24px; margin-bottom: 10px; }}
                .book-author {{ color: #666; margin-bottom: 20px; }}
                .book-review {{ line-height: 1.6; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="book-info">
                    <h1 class="book-title">{self.title_input.text()}</h1>
                    <div class="book-author">저자: {self.author_input.text()}</div>
                    <div class="book-review">{self.review_input.toPlainText()}</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        filename = f"book_review_{self.title_input.text().replace(' ', '_')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        QMessageBox.information(self, '성공', f'HTML 파일이 생성되었습니다: {filename}')
        
    def create_qr(self):
        """QR 코드 생성"""
        if not self.url_input.text():
            QMessageBox.warning(self, '경고', 'URL을 입력해주세요.')
            return
            
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(self.url_input.text())
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        filename = f"qr_code_{self.title_input.text().replace(' ', '_')}.png"
        qr_image.save(filename)
        
        # QR 코드 이미지 표시
        pixmap = QPixmap(filename)
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        self.qr_label.setPixmap(scaled_pixmap)
        
        QMessageBox.information(self, '성공', f'QR 코드가 생성되었습니다: {filename}')
        
    def save_feedback(self):
        """피드백 저장"""
        feedback, ok = QMessageBox.getText(self, '피드백 입력', '피드백을 입력하세요:')
        if ok and feedback:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            feedback_text = f"""
도서명: {self.title_input.text()}
작성일시: {timestamp}
피드백 내용:
{feedback}
-------------------
"""
            filename = f"feedback_{self.title_input.text().replace(' ', '_')}.txt"
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(feedback_text)
                
            QMessageBox.information(self, '성공', '피드백이 저장되었습니다.')

def main():
    app = QApplication(sys.argv)
    ex = BookCurationApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

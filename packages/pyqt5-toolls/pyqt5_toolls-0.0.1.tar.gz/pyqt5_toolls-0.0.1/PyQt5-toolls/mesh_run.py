import pymysql
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QMessageBox, QComboBox, QPushButton, QVBoxLayout, QWidget)


class CarpetOrderApp(QMainWindow):
    def init(self):
        super().init()
        self.setup_ui()
        self.db = pymysql.connect(host="localhost", user="root", password="",
                                  db="carpet_shop", charset="utf8mb4")
        self.cursor = self.db.cursor()
        self.user_id = self.user_role = None
        self.load_data()

    def setup_ui(self):
        self.setWindowTitle("Шелковпарк - Заказ ковров")
        self.setGeometry(100, 100, 600, 400)

        widgets = {
            'email': QLineEdit(placeholderText="Email"),
            'password': QLineEdit(placeholderText="Пароль", echoMode=QLineEdit.Password),
            'login_btn': QPushButton("Войти", clicked=self.login),
            'load_btn': QPushButton("Загрузить ковры", clicked=self.load_carpets),
            'carpets': QComboBox(),
            'material': QComboBox(),
            'edge': QComboBox(),
            'width': QLineEdit(placeholderText="Ширина (м)"),
            'height': QLineEdit(placeholderText="Длина (м)"),
            'quantity': QLineEdit(placeholderText="Количество"),
            'order_btn': QPushButton("Оформить заказ", clicked=self.place_order)
        }

        layout = QVBoxLayout()
        for label, widget in [
            ("Вход", widgets['email']), ("", widgets['password']), ("", widgets['login_btn']),
            ("Выбор ковра", widgets['load_btn']), ("", widgets['carpets']),
            ("Материал", widgets['material']), ("Окантовка", widgets['edge']),
            ("", widgets['width']), ("", widgets['height']),
            ("", widgets['quantity']), ("", widgets['order_btn'])
        ]:
            if label: layout.addWidget(QLabel(label))
            layout.addWidget(widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.widgets = widgets

    def load_data(self):
        for combo, query in [
            (self.widgets['material'], "SELECT id, model FROM materials"),
            (self.widgets['edge'], "SELECT id, name FROM edge_types")
        ]:
            combo.clear()
            self.cursor.execute(query)
            combo.addItems(f"{row[1]} (id: {row[0]})" for row in self.cursor.fetchall())

    def login(self):
        email, password = self.widgets['email'].text(), self.widgets['password'].text()
        self.cursor.execute("SELECT id, role FROM users WHERE email=%s AND password_hash=%s",
                            (email, password))
        if user := self.cursor.fetchone():
            self.user_id, self.user_role = user
            QMessageBox.information(self, "Успех", f"Вход выполнен как {self.user_role}")
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные данные для входа")

    def load_carpets(self):
        self.widgets['carpets'].clear()
        self.cursor.execute("SELECT id, name FROM carpets")
        self.widgets['carpets'].addItems(f"{row[1]} (id: {row[0]})" for row in self.cursor.fetchall())

    def place_order(self):
        try:
            width, height, quantity = map(float, (self.widgets['width'].text(),
                                                  self.widgets['height'].text(),
                                                  self.widgets['quantity'].text()))
            carpet_id = self.widgets['carpets'].currentText().split("id: ")[1][:-1]

            self.cursor.execute("SELECT price_per_m2 FROM carpets WHERE id=%s", (carpet_id,))
            price = self.cursor.fetchone()[0] * width * height * quantity

            if price > 10000:
                discount = 0.05 if price <= 50000 else 0.10 if price <= 100000 else 0.15
                price *= (1 - discount)
self.cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (self.user_id,))
            self.cursor.execute("""
                INSERT INTO order_items (order_id, carpet_id, edge_type_id, width, height, quantity, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                (self.cursor.lastrowid, carpet_id,
                                 self.widgets['edge'].currentText().split("id: ")[1][:-1],
                                 width, height, quantity, price))

            self.db.commit()
            QMessageBox.information(self, "Успех", f"Заказ оформлен! Цена: {price:.2f} руб.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка заказа: {str(e)}")


if name == "main":
    app = QApplication(sys.argv)
    window = CarpetOrderApp()
    window.show()
    sys.exit(app.exec_())

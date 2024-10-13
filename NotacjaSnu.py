import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QGroupBox
from PySide6.QtGui import QCloseEvent

def save_titile():
    file_exists = os.path.isfile("sleep_data.txt")
    with open("sleep_data.txt", "a") as file:
        if not file_exists:
            file.write("Data;Czas snu;Czas snu lekkiego;Czas snu glebokiego;Czas fazy REM\n")

def save_data_to_txt(date, sleep_duration, light_sleep_duration, deep_sleep_duration, rem_duration):
    with open("sleep_data.txt", "a") as file:
        file.write(f"{date};{sleep_duration};{light_sleep_duration};{deep_sleep_duration};{rem_duration}\n")

def clear_data_file():
    with open("sleep_data.txt", "w") as file:
        file.truncate()

class SleepApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sleep App")

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        self.group_box = QGroupBox("Wprowadź dane snu")
        self.form_layout = QFormLayout()

        self.date_input = QLineEdit()
        self.duration_input = QLineEdit()
        self.light_sleep_duration_input = QLineEdit()
        self.deep_sleep_duration_input = QLineEdit()
        self.rem_duration_input = QLineEdit()

        self.form_layout.addRow("Data (YYYY-MM-DD):", self.date_input)
        self.form_layout.addRow("Czas snu (w godzinach):", self.duration_input)
        self.form_layout.addRow("Czas snu lekkiego (w godzinach):", self.light_sleep_duration_input)
        self.form_layout.addRow("Czas snu głębokiego (w godzinach):", self.deep_sleep_duration_input)
        self.form_layout.addRow("Czas fazy REM (w godzinach):", self.rem_duration_input)

        self.group_box.setLayout(self.form_layout)
        self.layout.addWidget(self.group_box)

        self.submit_btn = QPushButton("Dodaj dane")
        self.submit_btn.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_btn)

        self.clear_btn = QPushButton("Wyczyść dane")
        self.clear_btn.clicked.connect(self.clear_data)
        self.layout.addWidget(self.clear_btn)

        self.quit_btn = QPushButton("Wyjście")
        self.quit_btn.clicked.connect(QApplication.instance().quit)
        self.layout.addWidget(self.quit_btn)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def submit(self):
        try:
            date = self.date_input.text()
            sleep_duration = float(self.duration_input.text())
            light_sleep_duration = float(self.light_sleep_duration_input.text())
            deep_sleep_duration = float(self.deep_sleep_duration_input.text())
            rem_duration = float(self.rem_duration_input.text())

            save_titile()
            save_data_to_txt(date, sleep_duration, light_sleep_duration, deep_sleep_duration, rem_duration)

            QMessageBox.information(self, "Sukces", "Dane zostały dodane!")
            self.clear_inputs()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Proszę wprowadzić poprawne dane.")

    def clear_data(self):
        clear_data_file()
        QMessageBox.information(self, "Sukces", "Dane zostały wyczyszczone!")

    def closeEvent(self, event: QCloseEvent):
        should_close = QMessageBox.question(self, 'Close App', 'Do you want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if should_close == QMessageBox.StandardButton.Yes:
            self.open_text_file()
            event.accept()
        else:
            event.ignore()

    def open_text_file(self):
        try:
            if os.name == 'nt':  # For Windows
                os.startfile("sleep_data.txt")
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Nie można otworzyć pliku: {e}")

    def clear_inputs(self):
        self.date_input.clear()
        self.duration_input.clear()
        self.light_sleep_duration_input.clear()
        self.deep_sleep_duration_input.clear()
        self.rem_duration_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SleepApp()
    window.show()
    sys.exit(app.exec())

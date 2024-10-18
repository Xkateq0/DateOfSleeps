import sys
import os
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QGroupBox , QInputDialog, QDialog , QLabel
from PySide6.QtGui import QCloseEvent
from datetime import datetime
import numpy as np


def save_title():
    file_exists = os.path.isfile("sleep_data.txt")
    with open("sleep_data.txt", "a", encoding="utf-8") as file:
        if not file_exists:
            file.write("Data;Czas snu;Czas snu lekkiego;Czas snu głębokiego;Czas fazy REM\n")


def save_data_to_txt(date, sleep_duration, light_sleep_duration, deep_sleep_duration, rem_duration):
    with open("sleep_data.txt", "a", encoding="utf-8") as file:
        file.write(f"{date};{sleep_duration};{light_sleep_duration};{deep_sleep_duration};{rem_duration}\n")


def clear_data_file():
    with open("sleep_data.txt", "w", encoding="utf-8") as file:
        file.write("Data;Czas snu;Czas snu lekkiego;Czas snu głębokiego;Czas fazy REM\n")  # Zachowaj nagłówek


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

        self.visualize_btn = QPushButton("Wizualizuj dane")
        self.visualize_btn.clicked.connect(self.visualize_data)
        self.layout.addWidget(self.visualize_btn)

        self.group_btn = QPushButton("Grupuj dane dla miesiąca")
        self.group_btn.clicked.connect(self.group_data_by_month)
        self.layout.addWidget(self.group_btn)

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

            new_date = datetime.strptime(date, "%Y-%m-%d").date()
            total_sleep = light_sleep_duration + deep_sleep_duration + rem_duration
            if total_sleep != sleep_duration:
                QMessageBox.warning(self, "Błąd",
                                    "Suma czasu snu lekkiego, głębokiego i REM musi być równa całkowitemu czasowi snu.")
                return

            save_title()
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
            if os.name == 'nt':
                os.startfile("sleep_data.txt")
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Nie można otworzyć pliku: {e}")

    def visualize_data(self):
        try:
            dates = []
            sleep_durations = []
            light_sleep_durations = []
            deep_sleep_durations = []
            rem_durations = []

            with open("sleep_data.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()[1:]

                for line in lines:
                    parts = line.strip().split(';')
                    if len(parts) == 5:
                        dates.append(parts[0])
                        sleep_durations.append(float(parts[1]))
                        light_sleep_durations.append(float(parts[2]))
                        deep_sleep_durations.append(float(parts[3]))
                        rem_durations.append(float(parts[4]))

            sorted_data = sorted(
                zip(dates, sleep_durations, light_sleep_durations, deep_sleep_durations, rem_durations),
                key=lambda x: x[0])
            sorted_dates, sorted_sleep_durations, sorted_light_sleep_durations, sorted_deep_sleep_durations, sorted_rem_durations = zip(
                *sorted_data)

            plt.figure(figsize=(10, 6))

            plt.plot(sorted_dates, sorted_sleep_durations, label='Czas snu', marker='o')
            plt.plot(sorted_dates, sorted_light_sleep_durations, label='Czas snu lekkiego', marker='o')
            plt.plot(sorted_dates, sorted_deep_sleep_durations, label='Czas snu głębokiego', marker='o')
            plt.plot(sorted_dates, sorted_rem_durations, label='Czas fazy REM', marker='o')

            plt.title('Wizualizacja danych snu')
            plt.xlabel('Data')
            plt.ylabel('Czas (godziny)')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()

        except FileNotFoundError:
            QMessageBox.warning(self, "Błąd", "Plik z danymi snu nie został znaleziony.")
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Wystąpił błąd: {e}")

    def show_average_durations(self, avg_sleep_duration, avg_light_sleep_duration, avg_deep_sleep_duration,
                               avg_rem_duration):
        dialog = QDialog(self)
        dialog.setWindowTitle("Średnie czasy snu")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Średni czas snu: {avg_sleep_duration:.2f} godzin"))
        layout.addWidget(QLabel(f"Średni czas snu lekkiego: {avg_light_sleep_duration:.2f} godzin"))
        layout.addWidget(QLabel(f"Średni czas snu głębokiego: {avg_deep_sleep_duration:.2f} godzin"))
        layout.addWidget(QLabel(f"Średni czas fazy REM: {avg_rem_duration:.2f} godzin"))

        close_button = QPushButton("Zamknij")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec()

    def group_data_by_month(self):
        try:
            month, ok = QInputDialog.getText(self, "Wybierz miesiąc", "Podaj miesiąc (YYYY-MM):")
            if not ok or not month:
                return
            try:
                datetime.strptime(month, "%Y-%m")
            except ValueError:
                QMessageBox.warning(self, "Błąd", "Proszę podać poprawny miesiąc w formacie YYYY-MM.")
                return

            dates = []
            sleep_durations = []
            light_sleep_durations = []
            deep_sleep_durations = []
            rem_durations = []

            with open("sleep_data.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()[1:]

                for line in lines:
                    parts = line.strip().split(';')
                    if len(parts) == 5 and parts[0].startswith(month):
                        dates.append(parts[0])
                        sleep_durations.append(float(parts[1]))
                        light_sleep_durations.append(float(parts[2]))
                        deep_sleep_durations.append(float(parts[3]))
                        rem_durations.append(float(parts[4]))

            if dates:
                plt.suptitle(f'Wizualizacja danych snu za miesiąc {month}', fontsize=14)
                plt.figure(figsize=(10, 6))
                plt.plot(dates, sleep_durations, label='Czas snu', marker='o')
                plt.plot(dates, light_sleep_durations, label='Czas snu lekkiego', marker='o')
                plt.plot(dates, deep_sleep_durations, label='Czas snu głębokiego', marker='o')
                plt.plot(dates, rem_durations, label='Czas fazy REM', marker='o')

                avg_sleep_duration = np.mean(sleep_durations)
                avg_light_sleep_duration = np.mean(light_sleep_durations)
                avg_deep_sleep_duration = np.mean(deep_sleep_durations)
                avg_rem_duration = np.mean(rem_durations)

                plt.title(f'Wizualizacja danych snu dla {month}')
                plt.xlabel('Data')
                plt.ylabel('Czas (godziny)')
                plt.xticks(rotation=45)
                plt.legend()
                plt.tight_layout()
                plt.show()

                self.show_average_durations(avg_sleep_duration, avg_light_sleep_duration, avg_deep_sleep_duration,
                                            avg_rem_duration)

            else:
                QMessageBox.information(self, "Brak danych", "Brak danych dla wybranego miesiąca.")

        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Wystąpił błąd: {e}")

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

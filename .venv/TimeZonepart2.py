import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import QDateTime, QTimeZone, QTime, QDate


class TimeZoneConverterApp(QMainWindow):
    @staticmethod
    def main():
        app = QApplication(sys.argv)
        window = TimeZoneConverterApp()
        window.show()
        sys.exit(app.exec_())

    def __init__(self):
        super().__init__()

        self.result_label = QLabel("", self)
        self.convert_button = QPushButton("Convert", self)
        self.time_entry = QLineEdit(self)
        self.time_label = QLabel("Enter Time (HH:MM:SS):", self)
        self.to_timezone_combobox = QComboBox(self)
        self.to_timezone_label = QLabel("To Time Zone:", self)
        self.from_timezone_combobox = QComboBox(self)
        self.from_timezone_label = QLabel("From Time Zone:", self)
        self.setWindowTitle("Time Zone Converter")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        self.from_timezone_label.setGeometry(20, 20, 120, 30)
        self.from_timezone_combobox.setGeometry(150, 20, 200, 30)
        self.from_timezone_combobox.addItems([str(zone_id) for zone_id in QTimeZone.availableTimeZoneIds()])

        self.to_timezone_label.setGeometry(20, 70, 120, 30)
        self.to_timezone_combobox.setGeometry(150, 70, 200, 30)
        self.to_timezone_combobox.addItems([str(zone_id) for zone_id in QTimeZone.availableTimeZoneIds()])
        self.to_timezone_combobox.setCurrentText("b'Asia/Calcutta'")

        self.time_label.setGeometry(20, 120, 150, 30)
        self.time_entry.setGeometry(180, 120, 170, 30)

        self.convert_button.setGeometry(150, 170, 100, 40)
        self.convert_button.clicked.connect(self.convert_time)

        self.result_label.setGeometry(20, 220, 360, 30)
        self.result_label.setVisible(True)
        self.result_label.setStyleSheet("color: black")

    def convert_time(self):
        from_tz = self.from_timezone_combobox.currentText()
        to_tz = self.to_timezone_combobox.currentText()
        time_str = self.time_entry.text()

        print("From Time Zone:", from_tz)
        print("To Time Zone:", to_tz)
        print("Input Time:", time_str)

        time_parts = time_str.split(':')
        input_time = QTime(int(time_parts[0]), int(time_parts[1]), int(time_parts[2]))
        input_date_time = QDateTime.currentDateTime()
        input_date_time.setTime(input_time)
        print("Input QDateTime:", input_date_time.toString(Qt.ISODate))

        from_zone = QTimeZone(from_tz)
        from_offset = from_zone.offsetFromUtc(input_date_time)
        from_local_time = input_date_time.addSecs(from_offset)
        print("Local Time in 'From' Zone:", from_local_time.toString(Qt.ISODate))

        to_zone = QTimeZone(to_tz)
        to_offset = to_zone.offsetFromUtc(from_local_time)
        to_converted_time = from_local_time.addSecs(to_offset - from_offset)
        print("Converted Time in 'To' Zone:", to_converted_time.toString(Qt.ISODate))

        self.result_label.setText(f"Converted time: {to_converted_time.toString(Qt.ISODate)} {to_tz}")
        self.result_label.repaint()


if __name__ == "__main__":
    TimeZoneConverterApp.main()

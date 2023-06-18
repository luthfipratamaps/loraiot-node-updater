import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'luthfipratamaps',
    'password': 'Alsin12354!',
    'database': 'loraiot'
}

# Function to update data in the database
def update_data(node_id, longitude, latitude, is_need_shade):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to update the data
        sql = "UPDATE nodes SET Longitude = %s, Latitude = %s, Is_Need_Shade = %s WHERE Node_Id = %s"
        data = (longitude, latitude, is_need_shade, node_id)

        cursor.execute(sql, data)
        conn.commit()

        print("Data updated successfully!")
    except mysql.connector.Error as error:
        print("Error updating data:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Create a custom QMainWindow subclass for the GUI window
class NodeDataUpdaterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Data Updater")
        self.setGeometry(100, 100, 400, 250)

        # Create and position labels
        label_node_id = QLabel("Node ID:", self)
        label_node_id.setFont(QFont("Arial", 12))
        label_node_id.move(30, 30)

        label_longitude = QLabel("Longitude (Range: -90 to 90):", self)
        label_longitude.setFont(QFont("Arial", 12))
        label_longitude.move(30, 70)

        label_latitude = QLabel("Latitude (Range: -180 to 180):", self)
        label_latitude.setFont(QFont("Arial", 12))
        label_latitude.move(30, 110)

        label_is_need_shade = QLabel("Is Need Shade (0 or 1):", self)
        label_is_need_shade.setFont(QFont("Arial", 12))
        label_is_need_shade.move(30, 150)

        # Create and position line edits
        self.entry_node_id = QLineEdit(self)
        self.entry_node_id.setGeometry(250, 30, 100, 25)

        self.entry_longitude = QLineEdit(self)
        self.entry_longitude.setGeometry(250, 70, 100, 25)

        self.entry_latitude = QLineEdit(self)
        self.entry_latitude.setGeometry(250, 110, 100, 25)

        self.entry_is_need_shade = QLineEdit(self)
        self.entry_is_need_shade.setGeometry(250, 150, 100, 25)

        # Create and position the update button
        self.button_update = QPushButton("Update", self)
        self.button_update.setGeometry(150, 190, 100, 30)
        self.button_update.clicked.connect(self.handle_update)

    # Function to handle the button click event
    def handle_update(self):
        node_id = self.entry_node_id.text()
        longitude = self.entry_longitude.text()
        latitude = self.entry_latitude.text()
        is_need_shade = self.entry_is_need_shade.text()

        # Check if any input field is empty
        if node_id == '' or longitude == '' or latitude == '' or is_need_shade == '':
            QMessageBox.warning(self, "Error", "Please fill in all the fields.")
        else:
            # Validate input ranges
            try:
                node_id = int(node_id)
                longitude = float(longitude)
                latitude = float(latitude)
                is_need_shade = int(is_need_shade)

                if not (1 <= node_id <= 4):
                    QMessageBox.warning(self, "Error", "Node ID must be between 1 and 4.")
                elif not (-90 <= longitude <= 90):
                    QMessageBox.warning(self, "Error", "Longitude must be between -90 and 90.")
                elif not (-180 <= latitude <= 180):
                    QMessageBox.warning(self, "Error", "Latitude must be between -180 and 180.")
                elif is_need_shade not in [0, 1]:
                    QMessageBox.warning(self, "Error", "Is Need Shade must be either 0 or 1.")
                else:
                    update_data(node_id, longitude, latitude, is_need_shade)
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid input type. Please enter numeric values.")

# Create the application instance
app = QApplication(sys.argv)

# Create the main window instance
window = NodeDataUpdaterWindow()
window.show()

# Start the event loop
sys.exit(app.exec_())

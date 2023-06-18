import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QWidget, QFormLayout
from PyQt5.QtGui import QFont
import mysql.connector

# Function to read the database configuration from db.conf file
def read_db_config():
    db_config = {}
    with open('db.conf', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            db_config[key] = value
    return db_config

# Database configuration
db_config = read_db_config()

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

        return True
    except mysql.connector.Error as error:
        print("Error updating data:", error)
        return False
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

        # Create a central widget and a vertical layout for it
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a form layout for labels and input fields
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        # Create labels and input fields
        self.entry_node_id = QLineEdit()
        self.entry_longitude = QLineEdit()
        self.entry_latitude = QLineEdit()
        self.entry_is_need_shade = QLineEdit()

        # Add labels and input fields to the form layout
        form_layout.addRow(QLabel("Node ID (1-4):", self), self.entry_node_id)
        form_layout.addRow(QLabel("Longitude (-90 to 90):", self), self.entry_longitude)
        form_layout.addRow(QLabel("Latitude (-180 to 180):", self), self.entry_latitude)
        form_layout.addRow(QLabel("Is Need Shade (0 or 1):", self), self.entry_is_need_shade)

        # Create the update button
        self.button_update = QPushButton("Update")
        layout.addWidget(self.button_update)
        self.button_update.clicked.connect(self.handle_update)

    # Function to handle the button click event
    def handle_update(self):
        node_id = self.entry_node_id.text()
        longitude = self.entry_longitude.text()
        latitude = self.entry_latitude.text()
        is_need_shade = self.entry_is_need_shade.text()

        # Check if any input field is empty
        if node_id == '' or longitude == '' or latitude == '' or is_need_shade == '':
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        try:
            # Convert input values to the appropriate types
            node_id = int(node_id)
            longitude = float(longitude)
            latitude = float(latitude)
            is_need_shade = int(is_need_shade)

            # Validate input ranges
            if not (1 <= node_id <= 4):
                QMessageBox.warning(self, "Error", "Node ID must be between 1 and 4.")
            elif not (-90 <= longitude <= 90):
                QMessageBox.warning(self, "Error", "Longitude must be between -90 and 90.")
            elif not (-180 <= latitude <= 180):
                QMessageBox.warning(self, "Error", "Latitude must be between -180 and 180.")
            elif is_need_shade not in [0, 1]:
                QMessageBox.warning(self, "Error", "Is Need Shade must be either 0 or 1.")
            else:
                if update_data(node_id, longitude, latitude, is_need_shade):
                    QMessageBox.information(self, "Success", "Data updated successfully.")
                else:
                    QMessageBox.warning(self, "Error", "Failed to update data.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input type. Please enter numeric values.")

# Create the application instance
app = QApplication(sys.argv)

# Create the main window instance
window = NodeDataUpdaterWindow()
window.show()

# Start the event loop
sys.exit(app.exec_())

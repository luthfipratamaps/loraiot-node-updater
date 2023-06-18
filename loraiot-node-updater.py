import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
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

        label_longitude = QLabel("Longitude:", self)
        label_longitude.setFont(QFont("Arial", 12))
        label_longitude.move(30, 70)

        label_latitude = QLabel("Latitude:", self)
        label_latitude.setFont(QFont("Arial", 12))
        label_latitude.move(30, 110)

        label_is_need_shade = QLabel("Is Need Shade:", self)
        label_is_need_shade.setFont(QFont("Arial", 12))
        label_is_need_shade.move(30, 150)

        # Create and position line edits
        self.entry_node_id = QLineEdit(self)
        self.entry_node_id.setGeometry(150, 30, 200, 25)

        self.entry_longitude = QLineEdit(self)
        self.entry_longitude.setGeometry(150, 70, 200, 25)

        self.entry_latitude = QLineEdit(self)
        self.entry_latitude.setGeometry(150, 110, 200, 25)

        self.entry_is_need_shade = QLineEdit(self)
        self.entry_is_need_shade.setGeometry(150, 150, 200, 25)

        # Create and position the update button
        button_update = QPushButton("Update", self)
        button_update.setGeometry(150, 190, 100, 30)
        button_update.clicked.connect(self.handle_update)

    # Function to handle the button click event
    def handle_update(self):
        node_id = self.entry_node_id.text()
        longitude = self.entry_longitude.text()
        latitude = self.entry_latitude.text()
        is_need_shade = self.entry_is_need_shade.text()

        update_data(node_id, longitude, latitude, is_need_shade)

# Create the application instance
app = QApplication(sys.argv)

# Create the main window instance
window = NodeDataUpdaterWindow()
window.show()

# Start the event loop
sys.exit(app.exec_())

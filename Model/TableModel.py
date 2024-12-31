from PyQt6.QtCore import Qt, QAbstractTableModel
from decimal import Decimal
from datetime import date, datetime, time, timedelta


class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]

            # Handle Decimal data types
            if isinstance(value, Decimal):
                return str(value)

            # Handle datetime.date and datetime.datetime types
            if isinstance(value, date):
                return value.strftime("%Y-%m-%d")  # Format date as desired

            # Handle timedelta types
            if isinstance(value, timedelta):
                # Convert timedelta to "HH:MM:SS"
                total_seconds = int(value.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours:02}:{minutes:02}:{seconds:02}"

            # Optionally handle other data types like integers or floats
            if isinstance(value, (int, float)):
                return str(value)

            return value  # Default case for strings or other types

        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            else:
                return section + 1  # Display row numbers vertically
        return None


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import pandas as pd
import sys

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        current_column = index.column()
        current_row = index.row()
        if index.isValid():
            if role == QtCore.Qt.ForegroundRole:
                if current_column == 3 or current_column==4:
                    it = self._df.iloc[current_row, current_column]
                    if float(it) <0:
                        return QtGui.QBrush(QtCore.Qt.green)

            # if role == QtCore.Qt.BackgroundColorRole:
            #     if current_column == 3:
            #         it = self._df.iloc[index.row(), current_column]
            #         if float(it) < 0:
            #             return QtGui.QBrush(QtCore.Qt.blue)

            # if role == QtCore.Qt.FontRole:
            #     table_font = QtGui.QFont('open sans', 9)
            #     return table_font
            #
            if role == QtCore.Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class Main(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.setWindowTitle('根据条件改变颜色')
        self.tableView = QTableView()
        pddata = pd.DataFrame(
            {'代码': ['000625', '000628'], '名称': ['长安汽车', '高薪发展'], '价格': ['16.37', '8.77'], '涨幅': ['-1.32', '-2.34'],
             '3日涨幅': ['-1', '-4.12']})
        self.model = PandasModel(pddata)
        self.tableView.setModel(self.model)
        self.tableView.setFixedSize(900,600)
        self.tableView.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    # main.show()
    sys.exit(app.exec_())
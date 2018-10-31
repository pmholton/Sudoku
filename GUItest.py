import sys
import ruleBasedSudoku
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore


data = ([0,0,3,0,2,0,6,0,0], [9,0,0,3,0,5,0,0,1], [0,0,1,8,0,6,4,0,0],
   [0,0,8,1,0,2,9,0,0], [7,0,0,0,0,0,0,0,8],
   [0,0,6,7,0,8,2,0,0], [0,0,2,6,0,9,5,0,0],
   [8,0,0,2,0,3,0,0,9], [0,0,5,0,1,0,3,0,0])

class SudokuGrid(QtCore.QAbstractTableModel):
    def __init__(self, grid = [[]], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._grid = grid

    def isValid(self, value):
        if type(value) is int:
            if value <= 9 and value >= 0:
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return ''

    def rowCount(self, parent):
        return 9

    def columnCount(self, parent):
        return 9

    def data(self, index, role):

        if role == QtCore.Qt.BackgroundRole:
            row = index.row()
            col = index.column()
            if (row//3 + col//3) % 2 == 0:
                return QtGui.QBrush(QtGui.QColor('#CCCCCC'))

        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            value = self._grid[row][col]

            return value
        
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self._grid[row][col]

            return value

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        
        if role == QtCore.Qt.EditRole:

            row = index.row()
            col = index.column()

            if self.isValid(value):
                self._grid[row][col] = value
                self.dataChanged.emit(index, index)
                return True
        return False


class Example(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.topLeft = QtCore.QModelIndex()
        self.topLeft.row = 0
        self.topLeft.column = 0
        self.botRight = QtCore.QModelIndex()
        self.botRight.row = 8
        self.botRight.column = 8

    def solve(self):
        alg = self.algChecked()
        if alg == 1:
            formatted_grid = []
            for i in range(9):
                for j in range(9):
                    formatted_grid.append(self.model._grid[i][j])
            solved, solved_grid = ruleBasedSudoku.solve(self.model._grid)
            self.model._grid = solved_grid
        self.model.dataChanged.emit(self.topLeft, self.botRight)

    def initUI(self):

        qbtn = QtWidgets.QPushButton('&Quit', self)
        qbtn.clicked.connect(QtWidgets.QApplication.instance().quit)

        sbtn = QtWidgets.QPushButton('&Solve', self)
        sbtn.setAutoDefault(True)
        sbtn.clicked.connect(self.solve)

        btnbox = QtWidgets.QHBoxLayout()
        btnbox.addStretch(1)
        btnbox.addWidget(sbtn)
        btnbox.addWidget(qbtn)

        # Outbox contains the output statistics
        # outbox

        # rvbox contains the Output Box and the Button Box
        rvbox = QtWidgets.QVBoxLayout()
        #rvbox.addWidget(outbox)
        rvbox.addStretch(1)
        rvbox.addLayout(btnbox)


        gridbox = QtWidgets.QTableView()

        font = QtGui.QFont("Helvetica", 14)
        gridbox.setFont(font)

        gridbox.verticalHeader().setVisible(False)
        gridbox.horizontalHeader().setVisible(False)

        self.model = SudokuGrid(data)
        gridbox.setModel(self.model)


        for i in range(9):
            gridbox.setColumnWidth(i, 25)
            gridbox.setRowHeight(i, 25)


        self.algRadio1 = QtWidgets.QRadioButton('Deductive Solutions Only')
        self.algRadio2 = QtWidgets.QRadioButton('Deductive and Backtracking')
        self.algRadio3 = QtWidgets.QRadioButton('Backtracking Only')
        self.algRadio1.setChecked(True)
        
        algbox = QtWidgets.QVBoxLayout()
        algbox.addWidget(self.algRadio1)
        algbox.addWidget(self.algRadio2)
        algbox.addWidget(self.algRadio3)

        algGroup = QtWidgets.QGroupBox('Select an Algorithm:')
        algGroup.setLayout(algbox)

        lvbox = QtWidgets.QVBoxLayout()
        lvbox.addWidget(gridbox)
        lvbox.addWidget(algGroup)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(lvbox)
        hbox.addLayout(rvbox)
        self.setLayout(hbox)

        self.setGeometry(300, 300, 455, 375)
        self.setWindowTitle("Phil's Sudoku Solver")

        self.show()

    def algChecked(self):
        if self.algRadio1.isChecked():
            return 1
        elif self.algRadio2.isChecked():
            return 2
        elif self.algRadio3.isChecked():
            return 3
        return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
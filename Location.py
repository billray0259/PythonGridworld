
class Location:
    def __init__(self, row, col):
        self._row = row
        self._col = col

    def __str__(self):
        return "(" + str(self.row) + ", " + str(self.col) + ")"

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        self._row = row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col


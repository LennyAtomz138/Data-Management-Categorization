class Matrix:
    def __init__(self, rows, cols, values=3):
        self.rows = rows
        self.cols = cols
        try:
            self.matrix = []
            for i in range(rows):
                self.matrix.append([])
                for j in range(cols):
                    self.matrix[i].append(values[j + cols * i])
        except:
            values = [1.0 * i + 1 for i in range(rows * cols)]
            self.matrix = []
            for i in range(rows):
                self.matrix.append([])
                for j in range(cols):
                    self.matrix[i].append(values[j + cols * i])

    def update(self, row, col, value):
        self.matrix[row][col] = value

    def swapRows(self, x, y):
        self.matrix[x], self.matrix[y] = self.matrix[y], self.matrix[x]

    def __add__(self, other):
        if ((self.rows == other.rows) & (self.cols == other.cols)):
            temp = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    temp.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
            return temp
        else:
            raise ValueError('These Matrices do not have the same number of rows and columns')

    def __sub__(self, other):
        return self.__add__(other.__mul__(-1))

    def __mul__(self, other):
        if (type(1) == type(other) or type(0.1) == type(other)):
            temp = []
            for i in range(len(self.matrix)):
                for j in self.matrix[i]:
                    temp.append(j * other)
            return Matrix(self.rows, self.cols, temp)

        if (self.cols == other.rows):
            temp = Matrix(self.rows, other.cols, [0 for i in range(self.rows * other.cols)])
            for i in range(self.numberOfRows):
                for j in range(other.numberOfColumns):
                    for k in range(other.numberOfRows):
                        temp[i][j] += self.content[i][k] * other.content[k][j]
            return temp
        else:
            raise ValueError('Your matrix does not have the same number of cols as the number of rows of the second matrix')

    def __str__(self):
        temp = ""
        for i in self.matrix:
            temp += str(i) + "\n"
        return temp
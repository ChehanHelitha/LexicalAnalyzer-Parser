class FSATable:
    def _init_(self):
          self.fsaTable = [
            [ 1,  1,  2, -1,  3, 11, -1,  5,  6,  7,  8,  4,  4,  4,  3],
            [ 1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1,  2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  4,  4,  4, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,  4, 10],
            [11, 11, 11, 11, 11,  9, 12, 11, 11, 11, 11, 11, -1, -1, 11],
            [-1, 11, -1, -1, -1, 11, 11, -1, -1, -1, -1, -1, -1, -1, -1],
        ]
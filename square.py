class Square:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        
    def __str__(self) -> str:
        ranks = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', }
        files = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', }
        return f'{files[self.column]}{ranks[self.row]}'
    
    def __eq__(self, __value: object) -> bool:
        return self.row == __value.row and self.column == __value.column
    
    def __hash__(self) -> int:
        return hash((self.row, self.column))
    
    def is_valid(self) -> bool:
        return 0 <= self.row < 8 and 0 <= self.column < 8
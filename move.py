from square import Square

class Move:
    def __init__(self, start: Square, end: Square) -> None:
        self.start = start
        self.end = end
        
    def __str__(self) -> str:
        return f'{self.start} to {self.end}'
    
    def __eq__(self, __value: object) -> bool:
        return self.start == __value.start and self.end == __value.end
    
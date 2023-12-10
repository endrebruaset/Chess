from square import Square

class Move:
    def __init__(self, start: Square, end: Square) -> None:
        self.start = start
        self.end = end
        
    def __str__(self) -> str:
        return f'From: {self.start}, To: {self.end}'
    
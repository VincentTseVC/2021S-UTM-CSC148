from typing import List, Tuple
from Style import Style

class OnitamaStack:

    def __init__(self) -> None:
        self.content = []
    

    def push(self, board: List[List[str]], styles: List[Style]) -> None:
        self.content.append((board, styles))
    
    def pop(self) -> Tuple[List[List[str]], List[Style]]:
        return self.content.pop()

    def empty(self) -> bool:
        return self.content == []





    


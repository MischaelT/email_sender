from typing import List
import asyncio


class Universe():
    def exists() -> bool:
        pass
    def create():
        pass

class Soul():
    def __init__(self) -> None:
        soul_level: int = 0
    
    async def run_living(self):
        pass

class Buddism():
    def __init__(self) -> None:
        self.souls: List[Soul] = []
        self.universe: Universe = Universe(souls=souls)
    
    def run_life(self):
        while True:
            if not self.universe.exists():
                self.universe.create()
            lives: List = []
            for soul in self.souls:
                lives.append(soul.run_living)

            asyncio.gather(lives)


# Уровни
class LevelManager:
    def __init__(self):
        self.level = 1

    def next_level(self):
        self.level += 1

    def asteroid_count(self):
        return 3 + self.level

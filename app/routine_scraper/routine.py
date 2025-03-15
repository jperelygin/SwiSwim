class Routine:
    def __init__(self):
        self.level = None
        self.style = None
        self.capacity = None
        self.pre_workout = None
        self.workout = None
        self.post_workout = None
        self.inventory = None

    def __repr__(self):
        return (f"Routine. Level: {self.level}. Style: {self.style}. Capacity: {self.capacity}.\n"
                f"Inventory: {self.inventory}\n"
                f"Pre-workout:\n{self.pre_workout}\nMain workout:\n{self.workout}\nPost-workout:\n{self.post_workout}")

class Constraints:

    def __init__(self):
        super().__init__()

class DifferentThanPreviousDirectionConstraint:

    def __init__(self, direction, previous_direction):
        super().__init__()
        self.direction = direction
        self.previous_direction = previous_direction
    
    def apply(self):
        if self.direction != self.previous_direction:
            return True
        return False

class LessThanConstraint:

    def __init__(self, price, previous_price):
        super().__init__()
        self.price = price
        self.previous_price = previous_price

    def apply(self):
        if self.price < self.previous_price:
            return True
        return False
    

class MoreThanConstraint:
    
    def __init__(self, price, previous_price):
        super().__init__()
        self.price = price
        self.previous_price = previous_price

    def apply(self):
        if self.price > self.previous_price:
            return True
        return False
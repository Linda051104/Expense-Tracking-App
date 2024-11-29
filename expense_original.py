class Expense:
    def init(self, name, category, amount) -> None:
        self.name = name
        self.category = category 
        self.amount = amount
    
    def repr(self):
        return f"<Expense: {self.name}, {self.category}, ${self.amount:.2f}>"
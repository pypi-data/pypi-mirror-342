class Variable:
    def __init__(self, var_id, degree) -> None:
        """
        Variable initialization.
        
        Args:
            var_id (int): Variable ID
            degree (int): Degree
        
        Returns:
            None
        """
        self.var_id = var_id
        self.degree = degree
        self.price = 10
        self.demand = 0
        self.threshold = 1
        
    def reset(self) -> None:
        self.demand = 0
        self.price = 10
        self.threshold = 1
    
    
    # --- 価格の更新 ------------------------------------------------------------
    def update_price(self):
        """
        価格を更新する
        """
        if self.demand >= self.threshold: # 需要が閾値を超えたら価格を増加
            self.increase_price(1)
        elif self.demand < self.threshold: # 需要が閾値を下回ったら価格を減少
            self.decrease_price(1)
    
    
    def increase_price(self, amount) -> None:
        """
        価格を増加する
        """
        self.price += amount

    
    def decrease_price(self, amount) -> None:
        """
        価格を減少する
        """
        self.price = max(0, self.price - amount)
    
    
    # --- 閾値の更新 ------------------------------------------------------------
    def update_threshold(self):
        """
        閾値を更新する
        """
        if self.demand >= self.threshold: # 需要が閾値を超えたら閾値を増加
            self.increase_threshold(1)
        elif self.demand < self.threshold: # 需要が閾値を下回ったら閾値を減少
            self.decrease_threshold(1)
    
    
    def increase_threshold(self, amount):
        """
        閾値を増加する
        """
        self.threshold += amount
    
    
    def decrease_threshold(self, amount):
        """
        閾値を減少する
        """
        self.threshold = max(0, self.threshold - amount)

    
    def __repr__(self) -> str:
        return f"""
        Variable(var_id={self.var_id}, 
                 price={self.price}, 
                 demand={self.demand}, 
                 threshold={self.threshold})
        """
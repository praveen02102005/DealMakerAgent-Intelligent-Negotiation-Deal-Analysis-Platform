class SellerAgent:
    def __init__(self, initial_price, minimum_price, concession):
        self.initial_price = initial_price
        self.minimum_price = minimum_price
        self.concession = concession

    def make_offer(self, round_number):
        price = self.initial_price - (
            (round_number - 1) * self.concession
        )

        if price < self.minimum_price:
            price = self.minimum_price

        return round(price, 2)

    def can_accept(self, buyer_price):
        return buyer_price >= self.minimum_price

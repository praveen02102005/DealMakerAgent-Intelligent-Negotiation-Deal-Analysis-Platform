class BuyerAgent:
    def __init__(self, initial_offer, maximum_price, concession):
        self.initial_offer = initial_offer
        self.maximum_price = maximum_price
        self.concession = concession

    def make_offer(self, round_number):
        offer = self.initial_offer + (
            (round_number - 1) * self.concession
        )

        if offer > self.maximum_price:
            offer = self.maximum_price

        return round(offer, 2)

    def can_accept(self, seller_price):
        return seller_price <= self.maximum_price

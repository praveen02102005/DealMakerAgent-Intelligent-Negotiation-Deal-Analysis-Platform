from buyer_agent import BuyerAgent
from seller_agent import SellerAgent


class NegotiationEngine:

    def __init__(
        self,
        quantity,
        buyer_initial,
        buyer_maximum,
        seller_initial,
        seller_minimum,
        buyer_concession,
        seller_concession,
        maximum_rounds
    ):

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if maximum_rounds <= 0:
            raise ValueError("Maximum rounds must be greater than zero.")

        self.quantity = quantity
        self.maximum_rounds = maximum_rounds

        self.buyer = BuyerAgent(
            buyer_initial,
            buyer_maximum,
            buyer_concession
        )

        self.seller = SellerAgent(
            seller_initial,
            seller_minimum,
            seller_concession
        )

    def negotiate(self):

        history = []

        for round_number in range(
            1,
            self.maximum_rounds + 1
        ):

            buyer_offer = self.buyer.make_offer(
                round_number
            )

            seller_offer = self.seller.make_offer(
                round_number
            )

            difference = seller_offer - buyer_offer

            # Agreement condition
            if buyer_offer >= seller_offer:

                final_price = (
                    buyer_offer + seller_offer
                ) / 2

                total_amount = (
                    final_price * self.quantity
                )

                history.append({
                    "Round": round_number,
                    "Buyer Offer": buyer_offer,
                    "Seller Offer": seller_offer,
                    "Difference": difference,
                    "Status": "AGREEMENT"
                })

                return {
                    "status": "Agreement Reached",
                    "rounds": round_number,
                    "final_price": round(
                        final_price, 2
                    ),
                    "quantity": self.quantity,
                    "total_amount": round(
                        total_amount, 2
                    ),
                    "history": history
                }

            history.append({
                "Round": round_number,
                "Buyer Offer": buyer_offer,
                "Seller Offer": seller_offer,
                "Difference": difference,
                "Status": "COUNTER OFFER"
            })

        return {
            "status": "No Agreement",
            "rounds": self.maximum_rounds,
            "final_price": None,
            "quantity": self.quantity,
            "total_amount": None,
            "history": history
        }

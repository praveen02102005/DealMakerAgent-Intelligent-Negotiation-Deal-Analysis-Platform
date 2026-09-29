import unittest

from negotiation import NegotiationEngine


class NegotiationEngineTests(unittest.TestCase):
    def test_reaches_agreement_and_calculates_total(self):
        result = NegotiationEngine(
            quantity=10,
            buyer_initial=700,
            buyer_maximum=900,
            seller_initial=1000,
            seller_minimum=850,
            buyer_concession=50,
            seller_concession=50,
            maximum_rounds=10,
        ).negotiate()

        self.assertEqual(result["status"], "Agreement Reached")
        self.assertEqual(result["rounds"], 4)
        self.assertEqual(result["final_price"], 850.0)
        self.assertEqual(result["total_amount"], 8500.0)

    def test_stops_without_agreement_when_budget_is_too_low(self):
        result = NegotiationEngine(
            quantity=5,
            buyer_initial=500,
            buyer_maximum=600,
            seller_initial=900,
            seller_minimum=800,
            buyer_concession=25,
            seller_concession=25,
            maximum_rounds=4,
        ).negotiate()

        self.assertEqual(result["status"], "No Agreement")
        self.assertEqual(result["rounds"], 4)
        self.assertIsNone(result["final_price"])
        self.assertEqual(len(result["history"]), 4)

    def test_offers_are_capped_at_reservation_prices(self):
        result = NegotiationEngine(
            quantity=1,
            buyer_initial=700,
            buyer_maximum=750,
            seller_initial=1000,
            seller_minimum=950,
            buyer_concession=100,
            seller_concession=100,
            maximum_rounds=3,
        ).negotiate()

        self.assertEqual(result["history"][-1]["Buyer Offer"], 750)
        self.assertEqual(result["history"][-1]["Seller Offer"], 950)

    def test_rejects_non_positive_quantity(self):
        with self.assertRaises(ValueError):
            NegotiationEngine(0, 700, 900, 1000, 850, 50, 50, 10)

    def test_rejects_non_positive_round_limit(self):
        with self.assertRaises(ValueError):
            NegotiationEngine(10, 700, 900, 1000, 850, 50, 50, 0)


if __name__ == "__main__":
    unittest.main()
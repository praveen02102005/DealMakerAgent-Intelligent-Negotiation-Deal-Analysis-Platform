# 🤝 DealMakerAgent

A **rule-based multi-agent negotiation system** built with Python and Streamlit. No AI, no APIs, just pure logic-based negotiation.

## 📋 Features

- ✅ **Rule-Based Logic** - No ML, no AI APIs, just Python
- 👤 **Buyer Agent** - Increases offers gradually up to maximum budget
- 🏪 **Seller Agent** - Reduces prices gradually down to minimum
- ⚙️ **Negotiation Engine** - Automated round-based negotiation
- 📊 **Live Visualization** - Real-time negotiation tracking
- 📈 **Charts & Graphs** - Visual representation of price convergence
- 💾 **CSV Export** - Download negotiation history
- 🎯 **Agreement Detection** - Automatic deal closure

## 🏗️ Project Structure

```
DealMakerAgent/
│
├── app.py                 # Main Streamlit application
├── buyer_agent.py         # Buyer Agent class
├── seller_agent.py        # Seller Agent class
├── negotiation.py         # Negotiation Engine
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### 2. Installation

```bash
# Clone or download the project
cd DealMakerAgent

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

Your browser will automatically open the DealMakerAgent dashboard at `http://localhost:8501`

### 4. Run the Tests

The negotiation engine includes scenario tests for agreement, no-agreement, offer caps, and invalid inputs.

```bash
python -m unittest discover -v
```

## 📖 How It Works

### Negotiation Flow

1. **Initial Setup**
   - Buyer starts with initial offer (lower than seller's price)
   - Seller starts with initial price (higher than buyer's offer)

2. **Negotiation Rounds**
   - Each round, buyer increases offer by concession amount
   - Each round, seller decreases price by concession amount
   - System checks if offers meet (agreement condition: buyer_offer ≥ seller_offer)

3. **Agreement**
   - When buyer_offer ≥ seller_offer, agreement is reached
   - Final price = average of both offers
   - Total transaction value calculated

4. **No Agreement**
   - If maximum rounds reached without agreement, negotiation ends

### Example Scenario

```
Configuration:
- Buyer Maximum: ₹900
- Buyer Initial: ₹700
- Buyer Concession: ₹50

- Seller Initial: ₹1000
- Seller Minimum: ₹850
- Seller Concession: ₹50

Negotiation Progress:
Round 1: Buyer ₹700  vs  Seller ₹1000  (Difference: ₹300)
Round 2: Buyer ₹750  vs  Seller ₹950   (Difference: ₹200)
Round 3: Buyer ₹800  vs  Seller ₹900   (Difference: ₹100)
Round 4: Buyer ₹850  vs  Seller ₹850   (Difference: ₹0)

✅ AGREEMENT REACHED at ₹850
Total Value: ₹8,500 (for 10 units)
```

## ⚙️ Configuration Parameters

### Buyer Configuration
- **Initial Offer**: Starting price buyer offers
- **Maximum Price**: Maximum buyer willing to pay (budget limit)
- **Concession**: Amount buyer increases offer each round

### Seller Configuration
- **Initial Price**: Starting asking price
- **Minimum Price**: Lowest price seller willing to accept
- **Concession**: Amount seller decreases price each round

### General Settings
- **Quantity**: Number of units being negotiated
- **Maximum Rounds**: Maximum negotiation iterations before failure

## 📊 Output Features

### Agreement Reached
- ✅ Success message with visual confirmation
- 📌 Final agreed price
- 📦 Quantity and total transaction value
- 📍 Number of rounds taken

### Negotiation History Table
- Round number
- Buyer offer in that round
- Seller offer in that round
- Price difference
- Status (Counter Offer / Agreement)

### Negotiation Graph
- Line chart showing price convergence
- Buyer price line (ascending)
- Seller price line (descending)
- Visual intersection point at agreement

### CSV Export
- Download complete negotiation history
- Includes all rounds and pricing data

## 🔧 Code Overview

### `buyer_agent.py`
```python
class BuyerAgent:
    - make_offer(round_number)    # Calculates buyer's offer for given round
    - can_accept(seller_price)    # Checks if price is within budget
```

### `seller_agent.py`
```python
class SellerAgent:
    - make_offer(round_number)    # Calculates seller's offer for given round
    - can_accept(buyer_price)     # Checks if price meets minimum
```

### `negotiation.py`
```python
class NegotiationEngine:
    - negotiate()                 # Runs the complete negotiation process
    # Returns: Agreement status, final price, history, etc.
```

### `app.py`
- Streamlit UI with sidebar controls
- Real-time negotiation execution
- Dynamic visualization and charts
- CSV download functionality

## 🎯 Key Formulas

### Buyer's Offer (Round N)
```
Offer = Initial_Offer + (N - 1) × Concession
Maximum: Capped at Buyer_Maximum_Price
```

### Seller's Price (Round N)
```
Price = Initial_Price - (N - 1) × Concession
Minimum: Floored at Seller_Minimum_Price
```

### Agreement Condition
```
Agreement when: Buyer_Offer ≥ Seller_Offer
```

### Final Price
```
Final_Price = (Buyer_Offer + Seller_Offer) / 2
Total_Value = Final_Price × Quantity
```

## 🎨 Technologies Used

- **Python 3.7+** - Core language
- **Streamlit** - Web UI framework
- **Pandas** - Data manipulation and CSV export
- **Matplotlib** - Visualization and charts

## 📝 Example Use Cases

1. **Business Negotiations**
   - Supplier price negotiations
   - Contract rate discussions
   - Bulk purchase pricing

2. **Real Estate**
   - Property price negotiations
   - Rental rate discussions

3. **E-commerce**
   - Vendor pricing agreements
   - Wholesale negotiations

4. **Educational Projects**
   - Learning game theory
   - Understanding negotiation dynamics
   - Multi-agent systems

## 🔍 Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: Browser doesn't open automatically
**Solution**: Manually navigate to `http://localhost:8501`

### Issue: "Buyer initial offer cannot be greater than buyer maximum price"
**Solution**: Adjust slider values - Initial Offer must be ≤ Maximum Price

### Issue: "Seller initial price cannot be lower than seller minimum price"
**Solution**: Adjust slider values - Initial Price must be ≥ Minimum Price

## 📚 Learning Resources

This project demonstrates:
- Object-oriented programming in Python
- Rule-based decision making
- Multi-agent system design
- Web application development with Streamlit
- Data visualization with Matplotlib

## 🤝 Contributing

Feel free to modify and extend the project:
- Add different negotiation strategies
- Implement timeout/walkaway conditions
- Add multiple buyers/sellers
- Create different concession patterns
- Add logging and analytics

## 📄 License

This project is open source and available for educational and commercial use.

## 💡 Tips

- **Quick Agreement**: Set buyer and seller parameters close together
- **Long Negotiation**: Set wider gaps between buyer max and seller min
- **No Agreement**: Set incompatible ranges (e.g., buyer max < seller min)
- **Experiment**: Try different concession rates to see how speed of negotiation changes

---

**Built with ❤️ using Python and Streamlit**

No AI APIs. No Machine Learning. Just Pure Logic. 🚀

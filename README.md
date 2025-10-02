## Put-Call Parity CLI Feature

### Overview
The Put-Call Parity Checker allows users to verify the relationship between put and call options, ensuring that arbitrage opportunities do not exist in the market.

### Usage
To use the Put-Call Parity Checker, run the following command:

```bash
python put_call_parity.py --call_price <CALL_PRICE> --put_price <PUT_PRICE> --strike_price <STRIKE_PRICE> --interest_rate <INTEREST_RATE> --time_to_maturity <TIME_TO_MATURITY>
```

### Example
Assuming you have a call option priced at $10, a put option priced at $5, a strike price of $100, an interest rate of 5%, and a time to maturity of 1 year, you would use:

```bash
python put_call_parity.py --call_price 10 --put_price 5 --strike_price 100 --interest_rate 0.05 --time_to_maturity 1
```

### Sample Output
```plaintext
Put-Call Parity holds: True
```
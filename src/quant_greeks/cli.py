import argparse
import logging

def main():
    parser = argparse.ArgumentParser(description="Compute Black-Scholes Delta for a European Call")
    parser.add_argument("--spot", type=float, required=True, help="Spot price")
    parser.add_argument("--strike", type=float, required=True, help="Strike price")
    parser.add_argument("--rate", type=float, required=True, help="Risk-free rate (e.g., 0.01)")
    parser.add_argument("--vol", type=float, required=True, help="Volatility (e.g., 0.2)")
    parser.add_argument("--time", type=float, required=True, help="Time to maturity (in years)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Inputs: {args}")

    # Minimal Black-Scholes Delta formula (call)
    from math import log, sqrt, exp
    from scipy.stats import norm
    d1 = (log(args.spot/args.strike) + (args.rate + 0.5*args.vol**2)*args.time) / (args.vol*sqrt(args.time))
    delta = norm.cdf(d1)
    print(f"Call Delta: {delta:.4f}")

if __name__ == "__main__":
    main()


import argparse
from greeks import delta, gamma, vega, theta, rho
from binomial import binomial_option_pricing
from implied_vol import implied_volatility
from black_scholes import black_scholes_price

def main():
    parser = argparse.ArgumentParser(
        description="Options Greeks and Pricing CLI"
    )
    parser.add_argument("--option_type", choices=["call", "put"], required=True, help="Type of option: call or put")
    parser.add_argument("--S", type=float, required=True, help="Current stock price")
    parser.add_argument("--K", type=float, required=True, help="Strike price")
    parser.add_argument("--T", type=float, required=True, help="Time to expiry in years (e.g., 0.5 for 6 months)")
    parser.add_argument("--r", type=float, required=True, help="Annual risk-free interest rate (decimal, e.g., 0.01)")
    parser.add_argument("--sigma", type=float, help="Annual volatility (decimal, e.g., 0.2)")
    parser.add_argument(
        "--q",
        type=float,
        default=0.0,
        help="Continuous dividend yield (annualized, decimal, e.g., 0.03). Default is 0.0"
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["black-scholes", "binomial"],
        default="black-scholes",
        help="Option pricing model to use (default: black-scholes)"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=100,
        help="Number of steps for the binomial model (default: 100; ignored for Black-Scholes)"
    )
    parser.add_argument(
        '--american',
        action='store_true',
        help='Price an American style option (default is European)'
    )
    parser.add_argument(
        "--implied_vol",
        action="store_true",
        help="Compute implied volatility given the market price"
    )
    parser.add_argument(
        "--price",
        type=float,
        help="Market option price for implied volatility calculation"
    )

    args = parser.parse_args()

    # Implied volatility calculation
    if args.implied_vol:
        if args.price is None:
            print("Error: --price is required when using --implied_vol")
            return
        imp_vol = implied_volatility(
            option_type=args.option_type,
            S=args.S,
            K=args.K,
            T=args.T,
            r=args.r,
            price=args.price,
            q=args.q  # Pass dividend yield to implied volatility calculation
        )
        print(f"Implied volatility: {imp_vol:.5f}")
        return

    # Option Pricing
    if args.model == "black-scholes":
        if args.sigma is None:
            print("Error: --sigma is required for Black-Scholes pricing")
            return
        price = black_scholes_price(
            args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q
        )
        print(f"Black-Scholes {args.option_type} price: {price:.5f}")
        print(f"Delta: {delta(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q):.5f}")
        print(f"Gamma: {gamma(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q):.5f}")
        print(f"Vega: {vega(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q):.5f}")
        print(f"Theta: {theta(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q):.5f}")
        print(f"Rho: {rho(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q):.5f}")

    elif args.model == "binomial":
        if args.sigma is None:
            print("Error: --sigma is required for binomial pricing")
            return
        price = binomial_option_pricing(
            S=args.S,
            K=args.K,
            T=args.T,
            r=args.r,
            sigma=args.sigma,
            steps=args.steps,
            option_type=args.option_type,
            american=args.american,
            q=args.q  # Pass dividend yield to binomial pricing
        )
        style = "American" if args.american else "European"
        print(f"Binomial {args.option_type} option price ({style}): {price:.5f}")

if __name__ == "__main__":
    main()
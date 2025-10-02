import argparse
from greeks import delta, gamma, vega, theta, rho
from binomial import binomial_option_pricing
from implied_vol import implied_volatility
from black_scholes import black_scholes_price

def check_put_call_parity(S, K, T, r, sigma, q=0.0):
    call = black_scholes_price("call", S, K, T, r, sigma, q=q)
    put = black_scholes_price("put", S, K, T, r, sigma, q=q)
    lhs = call + K * pow(2.718281828459045, -r*T)
    rhs = put + S * pow(2.718281828459045, -q*T)
    diff = abs(lhs - rhs)
    return call, put, lhs, rhs, diff

def main():
    parser = argparse.ArgumentParser(description="Options Greeks and Pricing CLI")
    subparsers = parser.add_subparsers(dest='command', required=False)

    # Main pricer arguments (default)
    main_parser = subparsers.add_parser('price', help='Calculate option prices and Greeks (default)')
    main_parser.add_argument("--option_type", choices=["call", "put"], required=True, help="Type of option: call or put")
    main_parser.add_argument("--S", type=float, required=True, help="Current stock price")
    main_parser.add_argument("--K", type=float, required=True, help="Strike price")
    main_parser.add_argument("--T", type=float, required=True, help="Time to expiry in years (e.g., 0.5 for 6 months)")
    main_parser.add_argument("--r", type=float, required=True, help="Annual risk-free interest rate (decimal, e.g., 0.01)")
    main_parser.add_argument("--sigma", type=float, help="Annual volatility (decimal, e.g., 0.2)")
    main_parser.add_argument("--q", type=float, default=0.0, help="Continuous dividend yield (decimal, e.g., 0.03)")
    main_parser.add_argument("--model", type=str, choices=["black-scholes", "binomial"], default="black-scholes")
    main_parser.add_argument("--steps", type=int, default=100)
    main_parser.add_argument('--american', action='store_true', help='American style option (default is European)')
    main_parser.add_argument("--implied_vol", action="store_true", help="Compute implied volatility given the market price")
    main_parser.add_argument("--price", type=float, help="Market option price for implied volatility calculation")

    # Parity checker subcommand
    parity_parser = subparsers.add_parser('parity', help='Check put-call parity for given parameters')
    parity_parser.add_argument("--S", type=float, required=True, help="Current stock price")
    parity_parser.add_argument("--K", type=float, required=True, help="Strike price")
    parity_parser.add_argument("--T", type=float, required=True, help="Time to expiry in years (e.g., 0.5 for 6 months)")
    parity_parser.add_argument("--r", type=float, required=True, help="Annual risk-free interest rate (decimal, e.g., 0.01)")
    parity_parser.add_argument("--sigma", type=float, required=True, help="Annual volatility (decimal, e.g., 0.2)")
    parity_parser.add_argument("--q", type=float, default=0.0, help="Continuous dividend yield (decimal, e.g., 0.03)")

    args = parser.parse_args()

    if args.command == "parity":
        call, put, lhs, rhs, diff = check_put_call_parity(args.S, args.K, args.T, args.r, args.sigma, q=args.q)
        print(f"Put-Call Parity Check (European options):")
        print(f"  Call Price: {call:.5f}")
        print(f"  Put Price:  {put:.5f}")
        print(f"  Call + Ke^(-rT): {lhs:.5f}")
        print(f"  Put + Se^(-qT):  {rhs:.5f}")
        print(f"  Difference:      {diff:.8f}")
        if diff < 1e-6:
            print("  ✅ Put-call parity holds (within numerical tolerance).")
        else:
            print("  ⚠️ Put-call parity does NOT hold (check your inputs or model).")
        return

    # Default behavior if no subcommand is provided: pricing (your existing code)
    # ... (your previous main logic here, e.g., implied vol, pricing, greeks, etc.) ...
    # Copy your previous CLI logic here for option pricing and greeks as seen above.

if __name__ == "__main__":
    main()
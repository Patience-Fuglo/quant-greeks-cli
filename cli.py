import argparse
from greeks import delta, gamma, vega, theta, rho
from binomial import binomial_option_pricing
from implied_vol import implied_volatility
from black_scholes import black_scholes_price
from tabulate import tabulate
import csv

def check_put_call_parity(S, K, T, r, sigma, q=0.0):
    call = black_scholes_price("call", S, K, T, r, sigma, q=q)
    put = black_scholes_price("put", S, K, T, r, sigma, q=q)
    lhs = call + K * pow(2.718281828459045, -r*T)
    rhs = put + S * pow(2.718281828459045, -q*T)
    diff = abs(lhs - rhs)
    return call, put, lhs, rhs, diff

def print_results(results, args):
    if args.output == "plain":
        for row in results[1:]:  # Skip header
            print(f"{row[0]}: {row[1]:.5f}")
    elif args.output == "table":
        print(tabulate(results, headers="firstrow", tablefmt="github"))
    elif args.output == "csv":
        filename = args.csvfile if hasattr(args, "csvfile") and args.csvfile else "output.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(results)
        print(f"Results written to {filename}")

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
    main_parser.add_argument(
        "--output",
        choices=["plain", "table", "csv"],
        default="plain",
        help="Output format: plain (default), table (pretty print), or csv (export to CSV file)"
    )
    main_parser.add_argument(
        "--csvfile",
        type=str,
        help="CSV file path to write results if output is 'csv'"
    )

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
    if hasattr(args, "option_type") and args.option_type in ["call", "put"]:
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
                q=args.q
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
            delta_val = delta(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q)
            gamma_val = gamma(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q)
            vega_val = vega(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q)
            theta_val = theta(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q)
            rho_val = rho(args.option_type, args.S, args.K, args.T, args.r, args.sigma, q=args.q)
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
                q=args.q
            )
            # Greeks not implemented for binomial in this example
            delta_val = gamma_val = vega_val = theta_val = rho_val = float('nan')
        else:
            print("Invalid model specified.")
            return

        results = [
            ["Metric", "Value"],
            ["Price", price],
            ["Delta", delta_val],
            ["Gamma", gamma_val],
            ["Vega", vega_val],
            ["Theta", theta_val],
            ["Rho", rho_val]
        ]

        print_results(results, args)

if __name__ == "__main__":
    main()
    
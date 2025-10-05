import argparse
from greeks import delta, gamma, vega, theta, rho
from binomial import binomial_option_pricing
from implied_vol import implied_volatility
from black_scholes import black_scholes_price
from tabulate import tabulate
import csv
import json
import numpy as np
import sys
import os
from quant_greeks_cli.binomial import binomial_option_pricing
from quant_greeks_cli.greeks import delta, gamma, vega, theta, rho
# etc.


# Only import matplotlib if needed (for CLI robustness)
def safe_import_matplotlib():
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        print("matplotlib is required for plotting. Install with: pip install matplotlib")
        sys.exit(1)

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

def validate_args(args):
    errors = []
    if hasattr(args, "S") and args.S is not None and args.S <= 0:
        errors.append("Stock price S must be positive.")
    if hasattr(args, "K") and args.K is not None and args.K <= 0:
        errors.append("Strike price K must be positive.")
    if hasattr(args, "T") and args.T is not None and args.T < 0:
        errors.append("Time to expiry T cannot be negative.")
    if hasattr(args, "sigma") and args.sigma is not None and args.sigma <= 0:
        errors.append("Volatility sigma must be positive.")
    if hasattr(args, "r") and args.r is not None and args.r < 0:
        errors.append("Risk-free rate r cannot be negative.")
    if hasattr(args, "q") and args.q is not None and args.q < 0:
        errors.append("Dividend yield q cannot be negative.")

    # Model-specific
    if hasattr(args, "model") and args.model == "black-scholes" and getattr(args, "american", False):
        errors.append("Black-Scholes model does not support American options. Use binomial model with --american.")

    # Implied vol
    if hasattr(args, "implied_vol") and args.implied_vol and (not hasattr(args, "price") or args.price is None):
        errors.append("Implied volatility calculation requires --price (market price).")

    # Sweep: check swept param is not None
    if getattr(args, "command", None) == "sweep":
        sweep_required = ["S", "K", "T", "r", "sigma", "q"]
        for param in sweep_required:
            if param != args.param and getattr(args, param, None) is None:
                errors.append(f"Please provide a value for {param} (all fixed parameters except for the one being swept: {args.param}).")

    # Output format
    if hasattr(args, "output") and args.output == "csv" and not (hasattr(args, "csvfile") and args.csvfile):
        print("Hint: CSV output will be saved as 'output.csv' by default. Use --csvfile to specify a filename.")

    # Plotting metric
    if getattr(args, "output", None) == "plot":
        allowed_metrics = ["price", "delta", "gamma", "vega", "theta", "rho"]
        if not hasattr(args, "plot_metric") or args.plot_metric not in allowed_metrics:
            errors.append(f"--plot_metric must be one of {allowed_metrics} for plotting.")

    if errors:
        print("Error(s):")
        for err in errors:
            print(f" - {err}")
        print("See --help for usage examples and required arguments.")
        sys.exit(1)

def plot_sweep(sweep_values, results, args):
    plt = safe_import_matplotlib()
    metric_map = {
        "price": 1,
        "delta": 2,
        "gamma": 3,
        "vega": 4,
        "theta": 5,
        "rho": 6
    }
    idx = metric_map.get(args.plot_metric, 1)
    y_label = args.plot_metric.capitalize()
    y_vals = [row[idx] for row in results[1:]]  # skip header

    plt.plot(sweep_values, y_vals, marker='o')
    plt.xlabel(args.param)
    plt.ylabel(y_label)
    plt.title(f"{y_label} vs {args.param}")
    plt.grid(True)
    plt.savefig("plot.png")
    print("Plot saved as plot.png")

def sweep_parameter(args):
    sweep_values = np.linspace(args.start, args.end, args.steps)
    results = [["Param", "Price", "Delta", "Gamma", "Vega", "Theta", "Rho"]]
    json_results = []

    params = {
        "S": args.S, "K": args.K, "T": args.T, "r": args.r,
        "sigma": args.sigma, "q": args.q
    }

    for val in sweep_values:
        params_sweep = params.copy()
        params_sweep[args.param] = val

        if args.model == "black-scholes":
            price = black_scholes_price(args.option_type, params_sweep["S"], params_sweep["K"], params_sweep["T"], params_sweep["r"], params_sweep["sigma"], q=params_sweep["q"])
            delta_val = delta(args.option_type, params_sweep["S"], params_sweep["K"], params_sweep["T"], params_sweep["r"], params_sweep["sigma"], q=params_sweep["q"])
            gamma_val = gamma(args.option_type, params_sweep["S"], params_sweep["K"], params_sweep["T"], params_sweep["r"], params_sweep["sigma"], q=params_sweep["q"])
            vega_val = vega(args.option_type, params_sweep["S"], params_sweep["K"], params_sweep["T"], params_sweep["r"], params_sweep["sigma"], q=params_sweep["q"])
            theta_val = theta(args.option_type, params_sweep["S"], params_sweep["K"], params_sweep["T"], params_sweep["r"], params_sweep["sigma"], q=params_sweep["q"])
            rho_val = rho(args.option_type, params_sweep["S"], params_sweep["K"], params_sweep["T"], params_sweep["r"], params_sweep["sigma"], q=params_sweep["q"])
        else:
            price, delta_val, gamma_val, vega_val, theta_val, rho_val = binomial_option_pricing(
                S=params_sweep["S"], K=params_sweep["K"], T=params_sweep["T"], r=params_sweep["r"],
                sigma=params_sweep["sigma"], steps=100,
                option_type=args.option_type, american=False, q=params_sweep["q"], return_greeks=True
            )

        results.append([
            round(val, 5), round(price, 5), round(delta_val, 5), round(gamma_val, 5),
            round(vega_val, 5), round(theta_val, 5), round(rho_val, 5)
        ])
        json_results.append({
            args.param: val, "price": price, "delta": delta_val, "gamma": gamma_val,
            "vega": vega_val, "theta": theta_val, "rho": rho_val
        })

    if args.output == "json":
        print(json.dumps(json_results, indent=2))
    elif args.output == "plot":
        plot_sweep(sweep_values, results, args)
    else:
        print_results(results, args)

def process_option_row(opt):
    S = float(opt.get("S", 100))
    K = float(opt.get("K", 100))
    T = float(opt.get("T", 1))
    r = float(opt.get("r", 0.05))
    sigma = float(opt.get("sigma", 0.2))
    q = float(opt.get("q", 0.0))
    model = opt.get("model", "black-scholes")
    steps = int(opt.get("steps", 100))
    american = bool(opt.get("american", False))
    option_type = opt.get("option_type", "call")

    if model == "black-scholes":
        price = black_scholes_price(option_type, S, K, T, r, sigma, q=q)
        delta_val = delta(option_type, S, K, T, r, sigma, q=q)
        gamma_val = gamma(option_type, S, K, T, r, sigma, q=q)
        vega_val = vega(option_type, S, K, T, r, sigma, q=q)
        theta_val = theta(option_type, S, K, T, r, sigma, q=q)
        rho_val = rho(option_type, S, K, T, r, sigma, q=q)
    else:
        price, delta_val, gamma_val, vega_val, theta_val, rho_val = binomial_option_pricing(
            S=S, K=K, T=T, r=r, sigma=sigma, steps=steps,
            option_type=option_type, american=american, q=q, return_greeks=True
        )

    return {
        "option_type": option_type,
        "S": S, "K": K, "T": T, "r": r, "sigma": sigma, "q": q,
        "model": model, "steps": steps, "american": american,
        "price": price, "delta": delta_val, "gamma": gamma_val,
        "vega": vega_val, "theta": theta_val, "rho": rho_val
    }

def batch_process(file_path, args):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    options = []
    with open(file_path, "r") as f:
        if ext == ".csv":
            reader = csv.DictReader(f)
            for row in reader:
                options.append(row)
        elif ext == ".json":
            options = json.load(f)
        else:
            print("Batch file must be .csv or .json")
            sys.exit(1)
    
    results = []
    for opt in options:
        res = process_option_row(opt)
        results.append(res)

    if args.output == "json":
        print(json.dumps(results, indent=2))
    elif args.output == "csv":
        fieldnames = ["option_type", "S", "K", "T", "r", "sigma", "q", "model", "steps", "american", "price", "delta", "gamma", "vega", "theta", "rho"]
        filename = args.csvfile if hasattr(args, "csvfile") and args.csvfile else "batch_output.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        print(f"Batch results written to {filename}")
    else:
        table_data = [
            ["Type", "S", "K", "T", "r", "sigma", "q", "model", "steps", "american", "price", "delta", "gamma", "vega", "theta", "rho"]
        ]
        for row in results:
            table_data.append([
                row["option_type"], row["S"], row["K"], row["T"], row["r"], row["sigma"], row["q"],
                row["model"], row["steps"], row["american"], row["price"], row["delta"], row["gamma"],
                row["vega"], row["theta"], row["rho"]
            ])
        print(tabulate(table_data, headers="firstrow", tablefmt="github"))

def main():
    parser = argparse.ArgumentParser(description="Options Greeks and Pricing CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    main_parser = subparsers.add_parser('price', help='Calculate option prices and Greeks (default)')
    main_parser.add_argument("--option_type", choices=["call", "put"], required=True, help="Type of option: call or put")
    main_parser.add_argument("--S", type=float, required=True, help="Current stock price (must be > 0)")
    main_parser.add_argument("--K", type=float, required=True, help="Strike price (must be > 0)")
    main_parser.add_argument("--T", type=float, required=True, help="Time to expiry in years (e.g., 0.5 for 6 months; must be >= 0)")
    main_parser.add_argument("--r", type=float, required=True, help="Annual risk-free interest rate (decimal, e.g., 0.01; must be >= 0)")
    main_parser.add_argument("--sigma", type=float, help="Annual volatility (decimal, e.g., 0.2; must be > 0)")
    main_parser.add_argument("--q", type=float, default=0.0, help="Continuous dividend yield (decimal, e.g., 0.03; must be >= 0)")
    main_parser.add_argument("--model", type=str, choices=["black-scholes", "binomial"], default="black-scholes")
    main_parser.add_argument("--steps", type=int, default=100)
    main_parser.add_argument('--american', action='store_true', help='American style option (default is European)')
    main_parser.add_argument("--implied_vol", action="store_true", help="Compute implied volatility given the market price")
    main_parser.add_argument("--price", type=float, help="Market option price for implied volatility calculation")
    main_parser.add_argument(
        "--output",
        choices=["plain", "table", "csv", "json"],
        default="plain",
        help="Output format: plain (default), table (pretty print), csv, or json"
    )
    main_parser.add_argument(
        "--csvfile",
        type=str,
        help="CSV file path to write results if output is 'csv'"
    )

    parity_parser = subparsers.add_parser('parity', help='Check put-call parity for given parameters')
    parity_parser.add_argument("--S", type=float, required=True, help="Current stock price")
    parity_parser.add_argument("--K", type=float, required=True, help="Strike price")
    parity_parser.add_argument("--T", type=float, required=True, help="Time to expiry in years (e.g., 0.5 for 6 months)")
    parity_parser.add_argument("--r", type=float, required=True, help="Annual risk-free interest rate (decimal, e.g., 0.01)")
    parity_parser.add_argument("--sigma", type=float, required=True, help="Annual volatility (decimal, e.g., 0.2)")
    parity_parser.add_argument("--q", type=float, default=0.0, help="Continuous dividend yield (decimal, e.g., 0.03)")

    sweep_parser = subparsers.add_parser('sweep', help='Show Greeks/price as you vary a parameter')
    sweep_parser.add_argument("--param", choices=["S", "K", "T", "r", "sigma", "q"], required=True, help="Parameter to sweep")
    sweep_parser.add_argument("--start", type=float, required=True, help="Sweep start value")
    sweep_parser.add_argument("--end", type=float, required=True, help="Sweep end value")
    sweep_parser.add_argument("--steps", type=int, default=10, help="Number of points (default: 10)")
    sweep_parser.add_argument("--option_type", choices=["call", "put"], required=True)
    sweep_parser.add_argument("--S", type=float)
    sweep_parser.add_argument("--K", type=float)
    sweep_parser.add_argument("--T", type=float)
    sweep_parser.add_argument("--r", type=float)
    sweep_parser.add_argument("--sigma", type=float)
    sweep_parser.add_argument("--q", type=float, default=0.0)
    sweep_parser.add_argument("--model", choices=["black-scholes", "binomial"], default="black-scholes")
    sweep_parser.add_argument("--output", choices=["plain", "table", "csv", "json", "plot"], default="plain")
    sweep_parser.add_argument("--csvfile", type=str, help="CSV file path for csv output")
    sweep_parser.add_argument("--plot_metric", choices=["price", "delta", "gamma", "vega", "theta", "rho"], default="price", help="Metric to plot on y-axis if --output plot")

    batch_parser = subparsers.add_parser('batch', help='Batch process a CSV or JSON file of options')
    batch_parser.add_argument('--file', required=True, help='CSV or JSON file with batch options')
    batch_parser.add_argument('--output', choices=['plain', 'table', 'csv', 'json'], default='table', help='Output format')
    batch_parser.add_argument('--csvfile', type=str, help="CSV file path for csv output")

    args = parser.parse_args()

    try:
        validate_args(args)

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

        if args.command == "sweep":
            sweep_parameter(args)
            return

        if args.command == "batch":
            batch_process(args.file, args)
            return

        if hasattr(args, "option_type") and args.option_type in ["call", "put"]:
            if args.implied_vol:
                if args.price is None:
                    print("Error: --price is required when using --implied_vol")
                    print("Hint: Provide the market option price with the --price flag.")
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

            if args.model == "black-scholes":
                if args.sigma is None:
                    print("Error: --sigma is required for Black-Scholes pricing")
                    print("Hint: Provide the volatility with the --sigma flag.")
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
                    print("Hint: Provide the volatility with the --sigma flag.")
                    return
                price, delta_val, gamma_val, vega_val, theta_val, rho_val = binomial_option_pricing(
                    S=args.S,
                    K=args.K,
                    T=args.T,
                    r=args.r,
                    sigma=args.sigma,
                    steps=args.steps,
                    option_type=args.option_type,
                    american=args.american,
                    q=args.q,
                    return_greeks=True
                )
            else:
                print("Invalid model specified.")
                print("Hint: Use --model with 'black-scholes' or 'binomial'.")
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
    except Exception as e:
        print("An unexpected error occurred:", e)
        print("Please check your inputs or use --help for guidance.")
        sys.exit(1)

if __name__ == "__main__":
    main()
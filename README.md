# Quant Greeks CLI Tool

![CI](https://github.com/Patience-Fuglo/quant-greeks-cli/actions/workflows/ci.yml/badge.svg)

A lightweight command-line tool for calculating the five main Black-Scholes Greeks (Delta, Gamma, Vega, Theta, Rho). Designed for traders, quants, and finance students, this tool helps you analyze options risk and sensitivity directly from your terminal.

---

## Features

- **Black-Scholes Greeks Calculator:** Computes Delta, Gamma, Vega, Theta, and Rho
- **Binomial and Black-Scholes Option Pricing:** Supports both models; Binomial supports American and European options
- **Implied Volatility Calculator:** Computes the implied volatility given a market price for a European option
- **Simple CLI:** Run calculations from your terminal with intuitive arguments
- **100% Test Coverage:** Every calculation is unit tested for accuracy
- **CI/CD:** Integrated with GitHub Actions for continuous testing and reliability

---

## Installation

Install directly from PyPI:

```bash
pip install quant-greeks-cli
```

Or clone the repository:

```bash
git clone https://github.com/Patience-Fuglo/quant-greeks-cli.git
cd quant-greeks-cli
python3 -m venv .venv       # optional but recommended
source .venv/bin/activate
pip install -r requirements.txt
pip install .
```

---

## Usage

Calculate option Greeks from the CLI:

```bash
quant-greeks --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2
```

Where:

- `--option_type` is `"call"` or `"put"`
- `--S` is the current stock price
- `--K` is the strike price
- `--T` is time to maturity (in years)
- `--r` is the annual risk-free rate (decimal)
- `--sigma` is volatility (decimal)

For help:
```bash
quant-greeks --help
```

### Example

```bash
quant-greeks --option_type put --S 95 --K 100 --T 0.5 --r 0.01 --sigma 0.15
```

---

## Implied Volatility Calculator (New Feature!)

You can now solve for the implied volatility that matches a given market price for a European option:

```bash
python cli.py --implied_vol --option_type call --S 100 --K 100 --T 1 --r 0.05 --price 10
```

Where:
- `--implied_vol`: Activates implied volatility calculation mode
- `--price`: The market price of the option

This will output:
```
Implied volatility: 0.18797
```

---

## Binomial Option Pricing Model

This CLI now supports option pricing using both the Black-Scholes and Binomial models.

### Usage Examples

**Black-Scholes (default):**
```bash
python cli.py --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2
```

**Binomial model (with steps):**
```bash
python cli.py --model binomial --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2 --steps 100
```
## New: Dividend Yield Support

You can now specify a **continuous dividend yield** using the `--q` flag for Black-Scholes and Binomial models:

```bash
python cli.py --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2 --q 0.03
```

- `--q`: The continuous dividend yield (as a decimal, e.g., 0.03 for 3%).  
- If omitted, defaults to 0 (no dividends).

This works for pricing and all Black-Scholes Greeks!


- `--model`: Choose `binomial` or `black-scholes` (default is `black-scholes`)
- `--steps`: Number of steps for the binomial tree (only used for binomial model; default = 100)


## Put-Call Parity Checker (New!)

You can now check put-call parity from the CLI:

```bash
python cli.py parity --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2 --q 0.03
```

## Output Formats: Table and CSV (New!)

You can now choose how your results are displayed or saved using the `--output` flag:

- **Plain (default):** One result per line (classic style)
- **Table:** Nicely formatted table in the terminal
- **CSV:** Save results for further analysis

### Examples

**Pretty table:**
```bash
python cli.py price --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2 --output table
```

**CSV export:**
```bash
python cli.py price --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2 --output csv --csvfile myresults.csv
```

**Classic (plain):**
```bash
python cli.py price --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2
```

If you use `--output csv` and do not specify `--csvfile`, the results will be saved to `output.csv` by default.

### What’s New

- Add binomial model for European option pricing
- New CLI arguments: `--model` and `--steps`
- All previous Black-Scholes functionality remains unchanged

---
## Greek Sensitivity Table (Parameter Sweep)

You can now analyze how option prices and Greeks (Delta, Gamma, Vega, Theta, Rho) change as you vary a single parameter, such as the spot price (S), volatility (sigma), time to expiry (T), strike (K), risk-free rate (r), or dividend yield (q).

### Usage

```bash
python cli.py sweep --param <PARAM> --start <START> --end <END> --steps <N> --option_type <call|put> --S <S> --K <K> --T <T> --r <r> --sigma <sigma> [--q <q>] [--output plain|table|csv|json] [--csvfile filename.csv]
```

- `--param`: Which parameter to sweep (S, K, T, r, sigma, q)
- `--start`, `--end`: Range for the swept parameter
- `--steps`: Number of points in the sweep (default: 10)
- All other option arguments: held constant unless swept
- `--output`: Output format (`plain`, `table`, `csv`, or `json`)
- `--csvfile`: CSV file (only needed if `--output csv`)

### Examples

**Sweep spot price S:**
```bash
python cli.py sweep --param S --start 80 --end 120 --steps 5 --option_type call --K 100 --T 1 --r 0.05 --sigma 0.2 --output table
```

**Sweep volatility sigma and get JSON output:**
```bash
python cli.py sweep --param sigma --start 0.1 --end 0.5 --steps 5 --option_type call --S 100 --K 100 --T 1 --r 0.05 --output json
```

**Sweep risk-free rate r and save to CSV:**
```bash
python cli.py sweep --param r --start 0.01 --end 0.1 --steps 10 --option_type put --S 100 --K 100 --T 1 --sigma 0.2 --output csv --csvfile sweep_rates.csv
```

The table output shows the parameter value, price, and all Greeks for each step. JSON and CSV let you use the results for further analysis.

## Robust Error Handling and User Hints

The CLI now features robust input validation and helpful error messages for common mistakes, such as:
- Missing required arguments (e.g., missing `--sigma` for Black-Scholes)
- Invalid values (e.g., negative prices or time)
- Contradictory arguments (e.g., American + Black-Scholes)
- Sweep mode missing a required fixed parameter
- Implied volatility calculation without a `--price`
- And more!

**Examples:**
```bash
python cli.py price --option_type call --S -100 --K 100 --T 1 --r 0.05 --sigma 0.2
# Error(s): Stock price S must be positive.

python cli.py price --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2 --model black-scholes --american
# Error(s): Black-Scholes model does not support American options. Use binomial model with --american.

python cli.py price --option_type call --S 100 --K 100 --T 1 --r 0.05 --implied_vol
# Error(s): Implied volatility calculation requires --price (market price).
```

Whenever a problem is detected, the CLI tells you what’s wrong and suggests a fix or refers you to `--help`.

## Plotting Sweep Results

You can now generate and save plots of option price or any Greek as you sweep a parameter! This feature uses matplotlib and is available via the CLI.

### Usage

To plot, use the `--output plot` option with the `sweep` subcommand, and optionally specify which metric to plot with `--plot_metric`.

```bash
python cli.py sweep --param <PARAM> --start <START> --end <END> --steps <N> --option_type <call|put> --S <S> --K <K> --T <T> --r <r> --sigma <sigma> [--q <q>] --output plot [--plot_metric <price|delta|gamma|vega|theta|rho>]
```

- `--output plot`: Save the plot as a PNG (`plot.png`) in your current directory.
- `--plot_metric`: Which metric to plot on the y-axis (default: price).

### Examples

**Plot how Delta changes with the spot price:**
```bash
python cli.py sweep --param S --start 80 --end 120 --steps 10 --option_type call --K 100 --T 1 --r 0.05 --sigma 0.2 --output plot --plot_metric delta
```

**Plot Vega as you vary volatility:**
```bash
python cli.py sweep --param sigma --start 0.1 --end 0.5 --steps 10 --option_type put --S 100 --K 100 --T 1 --r 0.05 --output plot --plot_metric vega
```

### Output

When you run a sweep with `--output plot`, a file named `plot.png` will be saved to your working directory. Open this file to view your chart. (If you're running in a remote or headless setup, download the file to your local machine to view.)

**Note:** You must have matplotlib installed (`pip install matplotlib`).


## Batch/Portfolio Processing

You can process multiple options at once from a CSV or JSON file using the `batch` subcommand.

### Usage

```bash
python cli.py batch --file my_options.csv --output table
python cli.py batch --file my_options.json --output csv
```

- Replace `my_options.csv` or `my_options.json` with your file path.
- Use `--output table`, `--output csv`, or `--output json` to choose the output format.
- Use `--csvfile <filename>` to specify the output CSV name (optional).

### Example CSV File

```csv
option_type,S,K,T,r,sigma,q,model,steps,american
call,100,100,1,0.05,0.2,0.0,black-scholes,100,False
put,50,45,0.5,0.03,0.25,0.01,black-scholes,100,False
call,120,110,2,0.04,0.22,0.01,binomial,200,True
put,80,85,0.8,0.02,0.18,0.0,binomial,150,False
```

### Example JSON File

```json
[
  {"option_type":"call","S":100,"K":100,"T":1,"r":0.05,"sigma":0.2,"q":0.0,"model":"black-scholes","steps":100,"american":false},
  {"option_type":"put","S":50,"K":45,"T":0.5,"r":0.03,"sigma":0.25,"q":0.01,"model":"black-scholes","steps":100,"american":false}
]
```

### Output

The CLI will print a table, write a CSV, or print JSON, depending on your choice. For binomial options, only the price is shown by default.


## Binomial Model Greeks

**New:** The CLI now supports Greeks (Delta, Gamma, Vega, Theta, Rho) for the binomial model as well!
- For European options, binomial Greeks will be close to Black-Scholes for a high number of steps.
- For American options, only the price is reliable; Greeks are approximate or may be set to `nan`.
- As a beginner, expect some differences—binomial Greeks are numerically estimated and can be less stable.

---

## Example: Compare Black-Scholes and Binomial Greeks

```bash
python cli.py price --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2 --q 0 --model black-scholes --output table
python cli.py price --option_type call --S 100 --K 100 --T 1 --r 0.05 --sigma 0.2 --q 0 --model binomial --steps 200 --output table
```

Check the results—Greeks for binomial (European) should be reasonably close to Black-Scholes with enough steps.

---

## Testing

Run all tests with:

```bash
pytest
```
(Requires pytest, included in `requirements.txt`.)

---

## Contributing

1. Fork the repo and create your feature branch:
    ```bash
    git checkout -b feature/YourFeature
    ```
2. Commit your changes and push:
    ```bash
    git commit -m "Describe your feature"
    git push origin feature/YourFeature
    ```
3. Open a Pull Request.

---

## License

MIT License

---

## Author

Patience Fuglo
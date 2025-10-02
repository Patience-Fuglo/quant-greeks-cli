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

The CLI will print a table, write a CSV, or print JSON, depending on your choice.
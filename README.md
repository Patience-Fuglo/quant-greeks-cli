# Quant Greeks CLI

A command-line tool for calculating the key option Greeks (Delta, Gamma, Vega, Theta, Rho) for European options using the Black-Scholes model. Built as part of my Quant Infra Engineer portfolio to demonstrate practical understanding of derivatives pricing, Python CLI development, and financial engineering best practices.

---

## Features

- **Supports European Calls and Puts**
- **Calculates all primary Greeks:** Delta, Gamma, Vega, Theta, Rho
- **Command-line interface** with clear argument structure
- **Modular, extensible Python codebase**
- **Well-documented and beginner-friendly**

---

## Usage

Assuming you have Python 3.8+ installed:

```bash
python quant_greeks_cli.py --type call --S 100 --K 100 --T 0.5 --r 0.01 --sigma 0.2 --q 0.0
```

- `--type`: call or put
- `--S`: Spot price
- `--K`: Strike price
- `--T`: Time to maturity (in years)
- `--r`: Risk-free rate (as decimal)
- `--sigma`: Volatility (as decimal)
- `--q`: Dividend yield (optional, default 0)

Run `python quant_greeks_cli.py --help` for full options.

---

## Example Output

```
Delta: 0.53
Gamma: 0.04
Vega: 0.19
Theta: -0.02
Rho: 0.10
```

---

## Installation

Clone this repository and navigate to the `quant-greeks-cli` folder:

```bash
git clone https://github.com/YOUR-USERNAME/quant-infra-portfolio.git
cd quant-infra-portfolio/quant-greeks-cli
pip install -r requirements.txt
```
*(Add `requirements.txt` if you use external packages; otherwise, skip this step.)*

---

## Project Structure

```
quant-greeks-cli/
├── quant_greeks_cli.py
├── README.md
└── (other files)
```

---

## What I Learned

- Building and structuring a maintainable Python CLI tool
- Translating financial models (Black-Scholes) into production-ready code
- Best practices in argument parsing, code documentation, and modularity
- Laying groundwork for larger quant engineering infrastructure

---

## License

MIT License

---

## Author

Patience Fuglo  
[LinkedIn](https://linkedin.com/in/YOUR-LINKEDIN) | [GitHub](https://github.com/Patience-Fuglo)

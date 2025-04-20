# CSV Summary CLI Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Status](https://img.shields.io/badge/status-actively--developed-brightgreen)

A command-line tool to summarize CSV files with basic statistics. Lightweight, fast, and extensible.

---

## Features

- Count total **rows** and **columns**
- Extract **column names**
- Infer **data types** (`int` or `str`)
- For numeric columns:
  - Mean
  - Std deviation
  - Min/Max
  - Median

---

## Installation

```bash
git clone https://github.com/MadhurDixit13/csv_summary_cli.git
```

```bash
pip install csv-summary-cli
```

Recommended

```bash
pip install pipx
pipx install csv-summary-cli
```

Once installed, run it using:

```bash
csv-summary data.csv
```

---

## Sample Output

![Output](output.png)

---

## Future Scope

- [ ] Float support
- [ ] Missing value counts
- [ ] `--numeric-only` option
- [ ] Handle malformed rows
- [ ] Tabular formatting (`tabulate`)
- [ ] Colored terminal output (`rich`, `colorama`)
- [ ] Column filters (`--columns age,salary`)
- [ ] Export summary to JSON

---

## Sample Input

```csv
Name,Age,Department,Salary,StartDate
Alice,29,Engineering,85000,2019-08-01
Bob,34,Marketing,62000,2018-03-15
Charlie,25,Engineering,73000,2021-06-30
Diana,45,HR,54000,2010-10-01
Evan,38,Engineering,,2017-01-12
Fay,30,Marketing,66000,2020-09-20
Grace,,HR,58000,2015-07-25
```

---

## License

MIT © [Madhur Dixit]

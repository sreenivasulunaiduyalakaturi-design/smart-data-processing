# Smart Data Processing

A simple Python base project that automatically loads, cleans, analyzes and
reports on any tabular dataset (CSV / Excel / JSON).

## Features
- Load CSV, Excel or JSON files
- Standardize column names
- Remove duplicate rows
- Auto-detect numeric and date columns
- Fill missing values (median for numbers, mode for text)
- Summary statistics, IQR outlier detection, correlation matrix
- Auto-generated insights and a text report

## Project Structure
```
smart_data_processing/
├── main.py            # entry point
├── requirements.txt
├── src/
│   ├── loader.py      # read files
│   ├── cleaner.py     # cleaning pipeline
│   ├── analyzer.py    # stats, outliers, correlations, insights
│   └── reporter.py    # saves cleaned CSV + report
├── data/sample_data.csv
├── tests/test_cleaner.py
└── output/            # results appear here
```

## Setup & Run
```bash
pip install -r requirements.txt
python main.py                      # run on the sample data
python main.py your_file.csv        # run on your own file
pip install pytest && python -m pytest tests   # run tests
```
(For Excel files also run: `pip install openpyxl`)

## Output
- `output/cleaned_data.csv` - cleaned dataset
- `output/report.txt` - insights, statistics, outliers, correlations

import sys
import re
import csv

def summary(csv_files):
    for csv_file in csv_files:
        print(f'\nSummarizing {csv_file}')
        try:
            with open(csv_file, 'r') as f:
                num_rows = 0
                col_names = []
                col_types = []

                first_line = f.readline()
                second_line = f.readline()

                col_names = first_line.strip().split(',')
                num_cols = len(col_names)

                for value in second_line.strip().split(','):
                    col_types.append('int' if value.isdigit() else 'str')

                for line in f:
                    num_rows += 1

                print(f'Number of rows: {num_rows}')
                print(f'Number of columns: {num_cols}')
                print(f'Column names: {col_names}')
                print(f'Column types: {col_types}')

                for i in range(num_cols):
                    f.seek(0)
                    reader = csv.reader(f)
                    next(reader)  # Skip the header

                    column_data = [row[i] for row in reader if len(row) > i]
                    if col_types[i] == 'int':
                        numeric_data = [int(x) for x in column_data if x.isdigit()]
                        if numeric_data:
                            mean = sum(numeric_data) / len(numeric_data)
                            std = (sum([(x - mean) ** 2 for x in numeric_data]) / len(numeric_data)) ** 0.5
                            mini = min(numeric_data)
                            maxi = max(numeric_data)
                            sorted_data = sorted(numeric_data)
                            mid = len(sorted_data) // 2
                            median = (sorted_data[mid - 1] + sorted_data[mid]) / 2 if len(sorted_data) % 2 == 0 else sorted_data[mid]
                            print(f"Column '{col_names[i]}': Mean = {mean:.2f}, Std = {std:.2f}, Min = {mini}, Max = {maxi}, Median = {median:.2f}")
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found.")
        except Exception as e:
            print(f"An error occurred while processing '{csv_file}': {e}")


def main():
    csv_files = []
    # Checking csv files
    for file in sys.argv[1:]:
        if re.search(r'\.csv$', file):
            csv_files.append(file)
    summary(csv_files)

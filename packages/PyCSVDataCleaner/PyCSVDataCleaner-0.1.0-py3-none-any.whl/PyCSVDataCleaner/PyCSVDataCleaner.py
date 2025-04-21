import csv
import os

def PyCSVDataCleaner(input_path, output_path=None):
    print(f"\nCleaning file: {os.path.basename(input_path)}")
    
    try:
        with open(input_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    if not rows:
        print("Empty file!")
        return

    header = rows[0]
    data = rows[1:]

    print("\n--- Initial Data Info ---")
    print(f"Rows (excluding header): {len(data)}")
    print(f"Columns: {len(header)}")

    unique_data = list({tuple(row) for row in data})
    print(f"Removed {len(data) - len(unique_data)} duplicate rows.")
    data = unique_data

    clean_data = [row for row in data if all(cell.strip() != '' for cell in row)]
    print(f"Removed {len(data) - len(clean_data)} rows with missing values.")
    data = clean_data

    constant_cols = []
    for idx, col in enumerate(header):
        col_vals = [row[idx] for row in data]
        if len(set(col_vals)) == 1:
            constant_cols.append(idx)

    if constant_cols:
        print(f"Removed {len(constant_cols)} constant columns.")
        header = [col for idx, col in enumerate(header) if idx not in constant_cols]
        data = [[cell for idx, cell in enumerate(row) if idx not in constant_cols] for row in data]
    else:
        print("No constant columns found.")

    print("\n--- Cleaning Done ---")
    print(f"Final Rows: {len(data)}")
    print(f"Final Columns: {len(header)}")

    if output_path:
        try:
            with open(output_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)
            print(f"\nCleaned file saved as: {output_path}")
        except Exception as e:
            print(f"Error saving cleaned file: {e}")
    else:
        print("\nNo output path provided. Data not saved.")
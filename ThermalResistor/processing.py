import csv
import math

def extract_missing_data(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the header row
        missing_rows = [headers]  # Include headers in the output

        for row in reader:
            if any(cell.strip() == "" for cell in row):
                missing_rows.append(row)

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(missing_rows)

def complete_missing_data(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = []
        headers = next(reader)  # Read the header row
        rows.append(headers)

        seen_rows = set()  # Track unique row labels

        for row in reader:
            row_label = row[0].strip()
            if row_label in seen_rows:
                continue  # Skip duplicate rows
            seen_rows.add(row_label)

            if row_label == "T/K":
                t_row = next((r for r in rows if r[0].strip() == "t/℃"), None)
                if t_row:
                    row = [str(float(t) + 273) if t.strip() != "" else "N/A" for t in t_row[1:]]
                    row.insert(0, "T/K")  # Reinsert the row label
            elif row_label == "1/T (10^-2 K^-1)":
                t_row = next((r for r in rows if r[0].strip() == "T/K"), None)
                if t_row:
                    row = [str(round(1 / float(t) * 100, 5)) if t.strip() != "" and t != "N/A" else "N/A" for t in t_row[1:]]
                    row.insert(0, "1/T (10^-2 K^-1)")  # Reinsert the row label
            elif row_label == "ln R_T":
                r_t_row = next((r for r in rows if r[0].strip() == "R_T/Ω"), None)
                if r_t_row:
                    row = [str(round(math.log(float(r)), 5)) if r.strip() != "" and r != "N/A" else "N/A" for r in r_t_row[1:]]
                    row.insert(0, "ln R_T")  # Reinsert the row label
            # TODO: Not isable algorithm to figure omega out yet
            # elif row_label == "-w/(%·K^-1)":
            #     r_t_row = next((r for r in rows if r[0].strip() == "R_T/Ω"), None)
            #     if r_t_row:
            #         row = [str(round(-1 * (float(r) / 100), 5)) if r.strip() != "" and r != "N/A" else "N/A" for r in r_t_row[1:]]
            #         row.insert(0, "-w/(%·K^-1)")  # Reinsert the row label
            else:
                row = [cell if cell.strip() != "" else "N/A" for cell in row]

            rows.append(row)

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# Main execution
if __name__ == "__main__":
    input_file = "f:/@courseworks/PhysicsExperiments/ThermalResistor/source_data.csv"
    output_file = "f:/@courseworks/PhysicsExperiments/ThermalResistor/processed_data.csv"
    complete_missing_data(input_file, output_file)
import csv
import os


def complete_meter_data(input_file, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with (
        open(input_file, encoding="utf-8") as fin,
        open(output_file, "w", encoding="utf-8", newline="") as fout,
    ):
        reader = list(csv.reader(fin))
        writer = csv.writer(fout)
        writer.writerow(reader[0])
        for row in reader[1:]:
            if len(row) < 6:
                row += [""] * (6 - len(row))
            try:
                v1 = float(row[2])
                v2 = float(row[3])
                avg = (v1 + v2) / 2
                row[4] = f"{avg:.4f}"
                diff = avg - float(row[1])
                row[5] = f"{diff:.4f}"
            except Exception:
                pass
            writer.writerow(row)


if __name__ == "__main__":
    current_meter_input_file = "source_data/source_i_meter.csv"
    current_meter_output_file = "processed_data/processed_i_meter.csv"

    voltage_meter_input_file = "source_data/source_v_meter.csv"
    voltage_meter_output_file = "processed_data/processed_v_meter.csv"

    complete_meter_data(current_meter_input_file, current_meter_output_file)
    complete_meter_data(voltage_meter_input_file, voltage_meter_output_file)

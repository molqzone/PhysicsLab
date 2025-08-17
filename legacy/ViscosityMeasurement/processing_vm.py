import csv
import os

def read_source_data(file_path):
    """
    Reads source data from a CSV file and returns it as a list of dictionaries.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# Function to process tube diameter data in source_data/test_tube_diameter.csv
# 直径/mm,1,2,3,4,5,平均值
# D₁,45.36,45.60,45.58,45.42,45.62,
# ΔD₁,,,,,,
# D₂,36.46,36.40,36.62,36.58,36.46,
# ΔD₂,,,,,,
# D₃,25.40,25.54,25.48,25.52,25.38,
# ΔD₃,,,,,,
# D₄,20.92,20.80,21.04,20.94,20.93,
# ΔD₄,,,,,,
def process_tube_diameter_data(data):
    """
    Processes tube diameter data and returns a list of dictionaries with average values and deviations.
    """
    processed = []
    for row in data:
        if row['直径/mm'].startswith('D') and not row['直径/mm'].startswith('Δ'):
            # 计算平均值
            values = [float(row[str(i)]) for i in range(1, 6) if row[str(i)]]
            avg = round(sum(values) / len(values), 2) if values else ''
            # 原始数据行
            processed.append({'直径/mm': row['直径/mm'], '1': row['1'], '2': row['2'], '3': row['3'], '4': row['4'], '5': row['5'], '平均值': avg})
            # 计算ΔD
            delta = [round(float(row[str(i)]) - avg, 2) for i in range(1, 6) if row[str(i)]]
            delta_row = {'直径/mm': f'Δ{row["直径/mm"]}'}
            for j, d in enumerate(delta, 1):
                delta_row[str(j)] = d
            for j in range(len(delta)+1, 6):
                delta_row[str(j)] = ''
            delta_sum = sum(delta)
            delta_count = len(delta)
            delta_avg = delta_sum / delta_count if delta_count else ''

            delta_row['平均值'] = f'{delta_avg:.50f}'
            processed.append(delta_row)
    return processed

def process_steel_ball_diameter_data(data):
    """
    Processes steel ball diameter data and returns a list of dictionaries with average values and deviations.
    """
    processed = []
    for row in data:
        if row['测量次序'].startswith('d'):
            # 计算平均值
            values = [float(row[str(i)]) for i in range(1, 6) if row[str(i)]]
            avg = round(sum(values) / len(values), 5) if values else ''
            result_row = {'测量次序': row['测量次序']}
            for i in range(1, 6):
                result_row[str(i)] = row[str(i)]
            result_row['平均值'] = avg
            processed.append(result_row)
            # 计算Δd
            delta = [round(abs(float(row[str(i)]) - avg), 5) for i in range(1, 6) if row[str(i)]]
            delta_row = {'测量次序': 'Δd = |(dᵢ - d₀) - d̅| / mm'}
            for j, d in enumerate(delta, 1):
                delta_row[str(j)] = d
            for j in range(len(delta)+1, 6):
                delta_row[str(j)] = ''
            delta_avg = round(sum(delta) / len(delta), 5) if delta else ''
            delta_row['平均值'] = delta_avg
            processed.append(delta_row)
    return processed

def process_fall_time_data(data):
    """
    Processes fall time data and returns a list of dictionaries with average values and deviations.
    """
    processed = []
    for row in data:
        if row['时间/s'].startswith('t') and not row['时间/s'].startswith('Δ'):
            # 计算平均值
            values = [float(row[str(j)]) for j in range(1, 6) if row[str(j)]]
            avg = round(sum(values) / len(values), 2) if values else ''
            # 原始数据行
            processed.append({'时间/s': row['时间/s'], '1': row['1'], '2': row['2'], '3': row['3'], '4': row['4'], '5': row['5'], '平均值': avg})
            # 计算Δt
            delta = [round(float(row[str(j)]) - avg, 2) for j in range(1, 6) if row[str(j)]]
            delta_avg = sum(delta) / len(delta) if len(delta) else ''
            delta_row = {'时间/s': f'Δ{row["时间/s"]}'}
            for j, d in enumerate(delta, 1):
                delta_row[str(j)] = d
            for j in range(len(delta)+1, 6):
                delta_row[str(j)] = ''
            delta_row['平均值'] = f'{delta_avg:.50f}'
            processed.append(delta_row)
    return processed

def process_timer_distance_data(data):
    """
    Processes timer distance data and returns a list of dictionaries with average values and deviations.
    """
    processed = []
    for row in data:
        if row['测量次序'].startswith('距离'):
            # 计算平均值
            values = [float(row[str(i)]) for i in range(1, 5) if row[str(i)]]
            avg = round(sum(values) / len(values), 2) if values else ''
            result_row = {'测量次序': row['测量次序']}
            for i in range(1, 5):
                result_row[str(i)] = row[str(i)]
            result_row['平均值'] = avg
            processed.append(result_row)
            # 计算Δs
            delta = [round(float(row[str(i)]) - avg, 2) for i in range(1, 5) if row[str(i)]]
            delta_row = {'测量次序': 'Δs/mm'}
            for j, d in enumerate(delta, 1):
                delta_row[str(j)] = d
            for j in range(len(delta)+1, 5):
                delta_row[str(j)] = ''
            delta_avg = round(sum(delta) / len(delta), 5) if delta else ''
            delta_row['平均值'] = delta_avg
            processed.append(delta_row)
    return processed

def output_processed_data(processed_data, output_file):
    """
    Outputs processed data to a CSV file.
    """
    if not processed_data:
        return
    fieldnames = list(processed_data[0].keys())
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in processed_data:
            writer.writerow(row)

def main():
    """
    Main function.
    """
    tube_diameters_source_file = './source_data/test_tube_diameters.csv'
    tube_diameters_output_file = 'processed_data/test_tube_diameters.csv'
    data = read_source_data(tube_diameters_source_file)
    processed_data = process_tube_diameter_data(data)
    output_processed_data(processed_data, tube_diameters_output_file)

    steel_ball_diameters_source_file = './source_data/steel_ball_diameters.csv'
    steel_ball_diameters_output_file = 'processed_data/steel_ball_diameters.csv'
    data = read_source_data(steel_ball_diameters_source_file)
    processed_data = process_steel_ball_diameter_data(data)
    output_processed_data(processed_data, steel_ball_diameters_output_file)

    fall_time_source_file = './source_data/steel_ball_fall_time.csv'
    fall_time_output_file = 'processed_data/steel_ball_fall_time.csv'
    data = read_source_data(fall_time_source_file)
    processed_data = process_fall_time_data(data)
    output_processed_data(processed_data, fall_time_output_file)

    timer_distance_source_file = './source_data/timer_distance.csv'
    timer_distance_output_file = 'processed_data/timer_distance.csv'
    data = read_source_data(timer_distance_source_file)
    processed_data = process_timer_distance_data(data)
    output_processed_data(processed_data, timer_distance_output_file)

if __name__ == '__main__':
    if not os.path.exists('processed_data'):
        os.makedirs('processed_data')
    main()

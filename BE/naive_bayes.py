from csv import reader
from math import sqrt
from math import exp
from math import pi
# Đọc file CSV
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset
# Chuyển cột sang kiểu số thực (float)
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())
# Chuyển cột sang kiểu số nguyên (integer)
lookupData = {}
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    lookup = dict()
    unique = set(class_values)
    for i, value in enumerate(unique):
        lookup[value] = i
        print('[%s] => %d' %(value, i))
        lookupData.update(lookup)
        print("lookup:", lookupData)
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup
# Phân chia dữ liệu theo nhãn
def separate_by_class(dataset):
    separated = dict()
    for i in range(len(dataset)):
        vector = dataset[i]
        class_value = vector[-1]
        if class_value not in separated:
            separated[class_value] = list()
        separated[class_value].append(vector)
    return separated
# Tính giá trị trung bình
def mean(numbers):
    return sum(numbers) / float(len(numbers))
# Tính độ lệch chuẩn
def stdev(numbers):
    avg = mean(numbers)
    variance = sum((x - avg) ** 2 for x in numbers) / float(len(numbers) - 1)
    return sqrt(variance)
# Tổng hợp dữ liệu
def summarize_dataset(dataset):
    summaries = [(mean(column), stdev(column), len(column)) for column in zip(*dataset)]
    del summaries[-1]  # Loại bỏ cột nhãn
    return summaries
# Tổng hợp dữ liệu theo nhãn
def summarize_by_class(dataset):
    separated = separate_by_class(dataset)
    summaries = dict()
    for class_value, rows in separated.items():
        summaries[class_value] = summarize_dataset(rows)
    return summaries
# Tính mật độ xác suất Gaussian
def calculate_probability(x, mean, stdev):
    exponent = exp(-((x - mean) ** 2 / (2 * stdev ** 2)))
    return (1 / (sqrt(2 * pi) * stdev)) * exponent
# Tính xác suất cho từng nhãn
def calculate_class_probabilities(summaries, row):
    total_rows = sum([summaries[label][0][2] for label in summaries])
    probabilities = dict()
    for class_value, class_summaries in summaries.items():
        probabilities[class_value] = summaries[class_value][0][2] / float(total_rows)
        for i in range(len(class_summaries)):
            mean, stdev, _ = class_summaries[i]
            probabilities[class_value] *= calculate_probability(row[i], mean, stdev)
    return probabilities
# Dự đoán nhãn
def predict(summaries, row):
    probabilities = calculate_class_probabilities(summaries, row)
    best_label, best_prob = None, -1
    for class_value, probability in probabilities.items():
        if best_label is None or probability > best_prob:
            best_prob = probability
            best_label = class_value
    print("best_label:", best_label)
    print("lookupData:", lookupData)
    if best_label == lookupData.get('0'):
        best_label = 'No'
    else:
        best_label = 'Yes'
    return best_label
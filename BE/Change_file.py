import csv
import os

# Định nghĩa file
fileToRead = "diabetes.csv"  # File CSV đầu vào
fileToWrite = "diabetes.arff"  # File ARFF đầu ra
relation = "diabetes"  # Tên tập dữ liệu

# Khởi tạo các danh sách lưu trữ tạm thời
dataType = []        # Kiểu dữ liệu từng cột: 'nominal' hoặc 'numeric'
columnsTemp = []     # Lưu dữ liệu từng cột
uniqueTemp = []      # Lưu giá trị riêng biệt tạm thời
uniqueOfColumn = []  # Lưu các giá trị riêng biệt cho từng cột
finalDataType = []   # Kiểu dữ liệu cuối cùng cho từng cột
attTypes = []        # Mô tả thuộc tính cho WEKA (numeric hoặc {value1, value2, ...})

# Mở file ARFF để ghi
writeFile = open(fileToWrite, 'w')

# Mở file CSV để đọc
with open(fileToRead, 'r') as f:
    reader = csv.reader(f)
    allData = list(reader)
    attributes = allData[0]  # Lấy tên các thuộc tính từ dòng đầu tiên
    totalCols = len(attributes)  # Tổng số cột
    totalRows = len(allData)  # Tổng số dòng

# Xử lý các ô trống trong dữ liệu
for j in range(0, totalCols):
    for i in range(0, totalRows):
        if len(allData[i][j]) == 0:  # Nếu ô trống, thay bằng '0'
            allData[i][j] = "0"

# Kiểm tra loại dữ liệu (nominal hoặc numeric) của từng cột
for j in range(0, totalCols):
    for i in range(1, totalRows):  # Bỏ qua dòng tiêu đề
        try:
            float(allData[i][j])  # Nếu chuyển được sang float, là numeric
            dataType.append("numeric")
        except ValueError:
            dataType.append("nominal")

    # Xác định kiểu dữ liệu cuối cùng
    if "nominal" in dataType:
        finalDataType.append("nominal")
    else:
        finalDataType.append("numeric")
    dataType = []

# Ghi dữ liệu meta-data vào file ARFF
writeFile.write("% Comments go after a '%' sign.\n")
writeFile.write("% Relation: " + relation + "\n\n")
writeFile.write("@relation " + relation + "\n\n")

# Ghi thuộc tính
for i in range(0, totalCols):
    if finalDataType[i] == "nominal":
        # Lấy giá trị riêng biệt cho thuộc tính nominal
        uniqueTemp = []
        for j in range(1, totalRows):
            if allData[j][i] not in uniqueTemp:
                uniqueTemp.append(allData[j][i])
        uniqueOfColumn.append("{" + ", ".join(uniqueTemp) + "}")
        attTypes.append(uniqueOfColumn[i])
    else:
        attTypes.append("numeric")
    writeFile.write("@attribute " + attributes[i] + " " + attTypes[i] + "\n")

# Ghi dữ liệu
writeFile.write("\n@data\n")
for i in range(1, totalRows):
    writeFile.write(",".join(allData[i]) + "\n")

writeFile.close()
print(f"File {fileToWrite} đã được chuyển đổi từ {fileToRead}.")

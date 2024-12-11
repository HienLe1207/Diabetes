document.getElementById("checkButton").addEventListener("click", function() {
    let data = {
        pregnancy: document.getElementById("pregnancy").value,
        glucose: document.getElementById("glucose").value,
        blood_pressure: document.getElementById("bloodPressure").value,
        skin_thickness: document.getElementById("skinThickness").value,
        insulin: document.getElementById("insulin").value,
        bmi: document.getElementById("bmi").value,
        diabetes_pedigree_function: document.getElementById("diabetesPedigreeFunction").value,
        age: document.getElementById("age").value
    };

    fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        let resultText = result.prediction === "Yes" ? "Bệnh tiểu đường" : "Không có khả năng mắc bệnh tiểu đường";
        document.getElementById("result").innerHTML = `Kết quả: ${resultText}`;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = "Đã có lỗi xảy ra!";
    });
});

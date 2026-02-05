const fileInput = document.getElementById("audioFile");
const fileName = document.getElementById("fileName");

fileInput.addEventListener("change", () => {
    if (fileInput.files.length)
        fileName.textContent = fileInput.files[0].name;
});

async function analyze() {
    const apiKey = document.getElementById("apiKey").value;
    const file = fileInput.files[0];

    if (!apiKey || !file) {
        alert("Enter API key and upload audio");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/detect", {
        method: "POST",
        headers: { "x-api-key": apiKey },
        body: formData
    });

    const data = await res.json();

    if (!res.ok) {
        alert(data.detail);
        return;
    }

    // Show prediction
    document.getElementById("prediction").innerText = data.prediction;

    // Confidence meter
    const confidence = Math.round((data.confidence || 0) * 100);
    document.getElementById("confidence").innerText = confidence + "%";
    document.getElementById("bar").style.width = confidence + "%";
}

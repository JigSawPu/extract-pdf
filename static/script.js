document.getElementById("uploadBtn").addEventListener("click", async () => {

    const files = document.getElementById("pdfs").files;

    if(files.length === 0){
        alert("Select PDFs");
        return;
    }

    const formData = new FormData();

    for(let file of files){
        formData.append("pdfs", file);
    }

    document.getElementById("loading").innerHTML =
        "Processing PDFs...";

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("loading").innerHTML = "";

    const tbody =
        document.querySelector("#resultsTable tbody");

    tbody.innerHTML = "";

    data.forEach(item => {

        tbody.innerHTML += `
            <tr>
                <td>${item.pdf}</td>

                <td>
                    <a class="download-btn"
                       href="/download/${item.text_file}">
                       Download
                    </a>
                </td>

                <td>
                    <a class="download-btn"
                       href="/download/${item.unique_file}">
                       Download
                    </a>
                </td>

                <td>
                    <a class="download-btn"
                       href="/download/${item.sorted_unique_file}">
                       Download
                    </a>
                </td>
            </tr>
        `;
    });
});

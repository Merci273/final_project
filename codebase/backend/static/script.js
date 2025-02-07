document.getElementById("upload-form").onsubmit = async function(event) {
    event.preventDefault();
    
    let fileInput = document.getElementById("file-input");
    if (fileInput.files.length === 0) {
        alert("Please select a file!");
        return;
    }
    
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    let response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    let result = await response.json();
    alert(result.message);
};

async function mineBlock() {
    let response = await fetch("/mine");
    let result = await response.json();
    alert(result.message);
}

async function viewChain() {
    let response = await fetch("/chain");
    let result = await response.json();
    
    document.getElementById("chain-output").innerText = JSON.stringify(result.chain, null, 2);
}

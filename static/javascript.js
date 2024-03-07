const generateForm = document.getElementById("generateForm");
const contentDiv = document.getElementById("imageContainer");
const downloadButton = document.getElementById("downloadButton");
const loader = document.querySelector(".loader");

generateForm.onsubmit = async (e) => {
    e.preventDefault();
    loader.classList.remove("loader-disabled");

    try {
        const res = await fetch("/prompt", {
            method: "POST",
            body: new FormData(generateForm),
        });

        if (res.ok) {
            const { base64_image, original_prompt } = await res.json();
            const image = new Image();
            image.src = `data:image/png;base64,${base64_image}`;            
            contentDiv.innerHTML = '';
            contentDiv.appendChild(image);

            downloadButton.style.display = "inline-block";
            downloadButton.href = `data:image/png;base64,${base64_image}`;
            downloadButton.download = `${original_prompt}.png`;
        } else {
            console.error("Failed to fetch image data");
        }
    } catch (error) {
        console.error("An error occurred:", error);
    } finally {
        loader.classList.add("loader-disabled");
    }
};

downloadButton.addEventListener('click', function(event) {
    if (downloadButton.href && downloadButton.download) {
        const downloadLink = document.createElement('a');
        downloadLink.href = downloadButton.href;
        downloadLink.download = downloadButton.download;
      
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    } else {
        console.error("Image data not available for download");
    }
});

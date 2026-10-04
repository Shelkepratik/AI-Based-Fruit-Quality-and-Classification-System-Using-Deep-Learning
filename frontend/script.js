// ==============================
// GET HTML ELEMENTS
// ==============================

const imageInput = document.getElementById("imageInput");

const preview = document.getElementById("preview");

const analyzeButton = document.getElementById("analyzeButton");


// ==============================
// IMAGE PREVIEW
// ==============================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (file) {

        preview.src = URL.createObjectURL(file);

        preview.style.display = "block";

    }

});


// ==============================
// ANALYZE BUTTON
// ==============================

analyzeButton.addEventListener("click", async function () {

    const file = imageInput.files[0];


    // Check image selection

    if (!file) {

        alert("Please select a fruit image.");

        return;

    }


    // ==============================
    // CREATE FORM DATA
    // ==============================

    const formData = new FormData();

    formData.append("file", file);


    // ==============================
    // SHOW LOADING MESSAGE
    // ==============================

    analyzeButton.innerText = "Analyzing...";

    analyzeButton.disabled = true;


    try {

        // ==============================
        // SEND IMAGE TO FASTAPI
        // ==============================

        const response = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",
                body: formData
            }
        );


        // ==============================
        // GET JSON RESPONSE
        // ==============================

        const data = await response.json();


        // ==============================
        // CHECK RESPONSE
        // ==============================

        if (!response.ok) {

            throw new Error(
                data.detail || "Prediction failed"
            );

        }


        // ==============================
        // DISPLAY RESULT
        // ==============================

        document.getElementById("fruit").innerText =
            data.fruit;


        document.getElementById("fruitConfidence").innerText =
            data.fruit_confidence + "%";


        document.getElementById("quality").innerText =
            data.quality;


        document.getElementById("qualityConfidence").innerText =
            data.quality_confidence + "%";


        document.getElementById("calories").innerText =
            data.calories;


        document.getElementById("fiber").innerText =
            data.fiber;


        document.getElementById("vitamins").innerText =
            data.vitamins;


        document.getElementById("price").innerText =
            data.reference_price;


    }


    catch (error) {

        console.error(error);

        alert(
            "Error: " + error.message
        );

    }


    finally {

        analyzeButton.innerText =
            "Analyze Fruit";

        analyzeButton.disabled =
            false;

    }

});
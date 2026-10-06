/* =====================================================
   ELEMENTS
===================================================== */

const imageInput =
    document.getElementById("imageInput");

const preview =
    document.getElementById("preview");

const analyzeButton =
    document.getElementById("analyzeButton");

const resetButton =
    document.getElementById("resetButton");

const removeImage =
    document.getElementById("removeImage");

const uploadPlaceholder =
    document.getElementById("uploadPlaceholder");

const imagePreviewContainer =
    document.getElementById(
        "imagePreviewContainer"
    );

const loadingStatus =
    document.getElementById(
        "loadingStatus"
    );

const themeButton =
    document.getElementById(
        "themeButton"
    );

const fileName =
    document.getElementById(
        "fileName"
    );

const fileSize =
    document.getElementById(
        "fileSize"
    );


/* =====================================================
   FRUIT HEALTH DATA
===================================================== */

const fruitData = {

    Apple: {

        benefits: [

            [
                "❤️",
                "Heart Health",
                "Apples provide dietary fiber and plant compounds that can support a balanced diet and cardiovascular health."
            ],

            [
                "🌿",
                "Digestive Health",
                "The dietary fiber in apples can contribute to normal digestive function."
            ],

            [
                "🛡️",
                "Antioxidants",
                "Apples contain antioxidant compounds that help support protection against oxidative stress."
            ],

            [
                "💧",
                "Hydration",
                "Apples contain a high amount of water and can contribute to daily fluid intake."
            ],

            [
                "⚡",
                "Natural Energy",
                "Natural carbohydrates provide energy as part of a balanced diet."
            ],

            [
                "🥗",
                "Healthy Snack",
                "A whole apple can be a convenient nutrient-rich snack."
            ]

        ],

        summary:
            "Apple provides dietary fiber, vitamin C and antioxidant compounds. It can be a useful part of a balanced diet.",

        tips: [

            "Wash the apple properly before eating.",

            "Eating the whole fruit provides more fiber than juice.",

            "Avoid visibly spoiled or moldy fruit."

        ]

    },


    Banana: {

        benefits: [

            [
                "⚡",
                "Natural Energy",
                "Bananas provide carbohydrates that can contribute to energy needs."
            ],

            [
                "💪",
                "Muscle Support",
                "Bananas provide potassium, an important mineral involved in normal muscle function."
            ],

            [
                "❤️",
                "Heart Friendly",
                "Potassium-rich foods can be part of a heart-healthy eating pattern."
            ],

            [
                "🌿",
                "Digestive Support",
                "Bananas provide dietary fiber that can support normal digestive function."
            ],

            [
                "🧠",
                "Vitamin B6",
                "Bananas provide vitamin B6, which is involved in normal metabolism and nervous-system function."
            ],

            [
                "🥤",
                "Easy Snack",
                "Bananas are convenient and easy to include in meals or snacks."
            ]

        ],

        summary:
            "Banana is a convenient fruit providing carbohydrates, potassium, dietary fiber and vitamin B6.",

        tips: [

            "Choose bananas according to your preferred ripeness.",

            "Wash the peel before handling food.",

            "Include bananas as part of a balanced diet."

        ]

    },


    Mango: {

        benefits: [

            [
                "🛡️",
                "Antioxidants",
                "Mango provides vitamin C and other plant compounds that contribute to antioxidant intake."
            ],

            [
                "👁️",
                "Eye Support",
                "Mango contains vitamin A-related nutrients that support normal vision."
            ],

            [
                "❤️",
                "Heart Health",
                "Mango can contribute vitamins and plant compounds to a balanced diet."
            ],

            [
                "💪",
                "Immune Support",
                "Vitamin C contributes to normal immune system function."
            ],

            [
                "🌿",
                "Digestive Health",
                "Mango provides dietary fiber that supports normal digestive function."
            ],

            [
                "💧",
                "Hydration",
                "Mango contains water and can contribute to overall fluid intake."
            ]

        ],

        summary:
            "Mango provides vitamin C, vitamin A-related nutrients and dietary fiber. It can be enjoyed as part of a varied and balanced diet.",

        tips: [

            "Wash the mango before cutting.",

            "Consume appropriate portions because mango contains natural sugars.",

            "Avoid visibly spoiled or moldy fruit."

        ]

    },


    Orange: {

        benefits: [

            [
                "🛡️",
                "Vitamin C",
                "Orange is a well-known source of vitamin C, which supports normal immune function."
            ],

            [
                "💧",
                "Hydration",
                "Orange contains a high amount of water and can contribute to fluid intake."
            ],

            [
                "❤️",
                "Heart Health",
                "Orange provides fiber and plant compounds that can be part of a heart-healthy diet."
            ],

            [
                "🌿",
                "Digestive Health",
                "The fruit provides dietary fiber that supports normal digestive function."
            ],

            [
                "🛡️",
                "Antioxidant Support",
                "Vitamin C and other plant compounds contribute to antioxidant intake."
            ],

            [
                "🥗",
                "Healthy Snack",
                "A whole orange is a convenient nutrient-rich snack."
            ]

        ],

        summary:
            "Orange provides vitamin C, dietary fiber, water and plant compounds that can support a balanced diet.",

        tips: [

            "Wash the orange before peeling.",

            "Whole fruit generally provides more fiber than juice.",

            "Avoid visibly spoiled or moldy fruit."

        ]

    }

};


/* =====================================================
   FILE SIZE FORMAT
===================================================== */

function formatFileSize(bytes) {

    if (bytes < 1024) {

        return bytes + " B";

    }

    if (bytes < 1024 * 1024) {

        return (
            (bytes / 1024).toFixed(1)
            + " KB"
        );

    }

    return (
        (bytes / (1024 * 1024)).toFixed(1)
        + " MB"
    );

}


/* =====================================================
   IMAGE SELECTION
===================================================== */

imageInput.addEventListener(
    "change",
    function () {

        const file =
            imageInput.files[0];

        if (!file) {

            return;

        }


        /* Validate */

        const allowedTypes = [

            "image/jpeg",
            "image/jpg",
            "image/png"

        ];


        if (
            !allowedTypes.includes(
                file.type
            )
        ) {

            alert(
                "Please select JPG, JPEG or PNG image."
            );

            imageInput.value = "";

            return;

        }


        /* File size */

        if (
            file.size >
            10 * 1024 * 1024
        ) {

            alert(
                "Image size should be less than 10 MB."
            );

            imageInput.value = "";

            return;

        }


        /*
         IMPORTANT:
         FileReader is used instead of
         URL.createObjectURL().
        */

        const reader =
            new FileReader();


        reader.onload =
            function (event) {

                preview.src =
                    event.target.result;

                preview.style.display =
                    "block";


                imagePreviewContainer.style.display =
                    "block";


                uploadPlaceholder.style.display =
                    "none";


                fileName.innerText =
                    file.name;


                fileSize.innerText =
                    formatFileSize(
                        file.size
                    )
                    + " • Ready for AI";


                resetButton.style.display =
                    "block";


                /* Restart animation */

                preview.style.animation =
                    "none";

                void preview.offsetWidth;

                preview.style.animation =
                    "imageAppear 0.8s ease";

            };


        reader.onerror =
            function () {

                alert(
                    "Unable to load image."
                );

            };


        reader.readAsDataURL(file);

    }
);


/* =====================================================
   REMOVE IMAGE
===================================================== */

removeImage.addEventListener(
    "click",
    function () {

        clearImage();

    }
);


/* =====================================================
   CLEAR IMAGE
===================================================== */

function clearImage() {

    imageInput.value = "";

    preview.src = "";

    preview.style.display =
        "none";

    imagePreviewContainer.style.display =
        "none";

    uploadPlaceholder.style.display =
        "block";

    fileName.innerText =
        "Image selected";

    fileSize.innerText =
        "Ready for analysis";

}


/* =====================================================
   ANALYZE BUTTON
===================================================== */

analyzeButton.addEventListener(
    "click",
    async function () {


        const file =
            imageInput.files[0];


        if (!file) {

            alert(
                "Please select a fruit image first."
            );

            return;

        }


        /* Form Data */

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );


        /* Loading */

        analyzeButton.disabled =
            true;

        document.getElementById(
            "analyzeText"
        ).innerText =
            "Analyzing...";

        document.getElementById(
            "analyzeIcon"
        ).innerText =
            "⏳";


        loadingStatus.style.display =
            "flex";


        try {


            /*
             FastAPI backend
            */

            const response =
                await fetch(
                    "http://127.0.0.1:8000/predict",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Prediction failed"
                );

            }


            /* =================================================
               RESULT
            ================================================= */


            document.getElementById(
                "fruit"
            ).innerText =
                data.fruit;


            document.getElementById(
                "fruitConfidence"
            ).innerText =
                data.fruit_confidence
                + "%";


            document.getElementById(
                "quality"
            ).innerText =
                data.quality;


            document.getElementById(
                "qualityConfidence"
            ).innerText =
                data.quality_confidence
                + "%";


            document.getElementById(
                "calories"
            ).innerText =
                data.calories;


            document.getElementById(
                "fiber"
            ).innerText =
                data.fiber;


            document.getElementById(
                "vitamins"
            ).innerText =
                data.vitamins;


            document.getElementById(
                "price"
            ).innerText =
                data.reference_price;


            /* =================================================
               PROGRESS BARS
            ================================================= */


            document.getElementById(
                "fruitProgress"
            ).style.width =
                data.fruit_confidence
                + "%";


            document.getElementById(
                "qualityProgress"
            ).style.width =
                data.quality_confidence
                + "%";


            /* =================================================
               NUTRITION
            ================================================= */


            document.getElementById(
                "nutritionCalories"
            ).innerText =
                data.calories;


            document.getElementById(
                "nutritionFiber"
            ).innerText =
                data.fiber;


            document.getElementById(
                "nutritionVitamins"
            ).innerText =
                data.vitamins;


            document.getElementById(
                "nutritionPrice"
            ).innerText =
                data.reference_price;


            /* =================================================
               HEALTH
            ================================================= */

            showFruitBenefits(
                data.fruit
            );


            /* =================================================
               AI SUMMARY
            ================================================= */

            createAISummary(
                data
            );


            /* =================================================
               SCROLL
            ================================================= */

            document
                .getElementById(
                    "analysis"
                )
                .scrollIntoView({
                    behavior: "smooth"
                });


        }

        catch (error) {

            console.error(
                error
            );

            alert(
                "Error: "
                + error.message
            );

        }

        finally {

            analyzeButton.disabled =
                false;

            document.getElementById(
                "analyzeText"
            ).innerText =
                "Analyze Fruit";

            document.getElementById(
                "analyzeIcon"
            ).innerText =
                "🤖";

            loadingStatus.style.display =
                "none";

        }

    }
);


/* =====================================================
   SHOW BENEFITS
===================================================== */

function showFruitBenefits(
    fruitName
) {


    const container =
        document.getElementById(
            "benefitsContainer"
        );


    const data =
        fruitData[
            fruitName
        ];


    if (!data) {

        container.innerHTML =

            "<p>Information not available.</p>";

        return;

    }


    container.innerHTML = "";


    data.benefits.forEach(
        function (benefit) {


            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "benefit-card";


            card.innerHTML = `

                <div class="benefit-icon">
                    ${benefit[0]}
                </div>

                <h3>
                    ${benefit[1]}
                </h3>

                <p>
                    ${benefit[2]}
                </p>

            `;


            container.appendChild(
                card
            );

        }
    );


    document.getElementById(
        "healthSummary"
    ).innerText =
        data.summary;


    const tipsList =
        document.getElementById(
            "tipsList"
        );


    tipsList.innerHTML = "";


    data.tips.forEach(
        function (tip) {

            const li =
                document.createElement(
                    "li"
                );

            li.innerText =
                tip;

            tipsList.appendChild(
                li
            );

        }
    );

}


/* =====================================================
   AI SUMMARY
===================================================== */

function createAISummary(
    data
) {


    const message =
        document.getElementById(
            "aiMessage"
        );


    let qualityMessage =
        "";


    const quality =
        data.quality.toLowerCase();


    if (
        quality === "good"
    ) {

        qualityMessage =
            "The image has been classified with a good visual quality level.";

    }

    else if (
        quality === "average"
    ) {

        qualityMessage =
            "The image has been classified with an average visual quality level. Minor visible imperfections may be present.";

    }

    else {

        qualityMessage =
            "The image has been classified with a poor visual quality level. Further physical inspection is recommended.";

    }


    message.innerHTML = `

        <strong>
            ${data.fruit}
        </strong>

        was detected with

        <strong>
            ${data.fruit_confidence}%
        </strong>

        fruit-classification confidence.

        The visual quality prediction is

        <strong>
            ${data.quality}
        </strong>

        with

        <strong>
            ${data.quality_confidence}%
        </strong>

        confidence.

        ${qualityMessage}

    `;

}


/* =====================================================
   RESET
===================================================== */

resetButton.addEventListener(
    "click",
    function () {

        clearImage();


        document.getElementById(
            "fruit"
        ).innerText =
            "—";


        document.getElementById(
            "fruitConfidence"
        ).innerText =
            "—";


        document.getElementById(
            "quality"
        ).innerText =
            "—";


        document.getElementById(
            "qualityConfidence"
        ).innerText =
            "—";


        document.getElementById(
            "calories"
        ).innerText =
            "—";


        document.getElementById(
            "fiber"
        ).innerText =
            "—";


        document.getElementById(
            "vitamins"
        ).innerText =
            "—";


        document.getElementById(
            "price"
        ).innerText =
            "—";


        document.getElementById(
            "fruitProgress"
        ).style.width =
            "0%";


        document.getElementById(
            "qualityProgress"
        ).style.width =
            "0%";


        document.getElementById(
            "nutritionCalories"
        ).innerText =
            "—";


        document.getElementById(
            "nutritionFiber"
        ).innerText =
            "—";


        document.getElementById(
            "nutritionVitamins"
        ).innerText =
            "—";


        document.getElementById(
            "nutritionPrice"
        ).innerText =
            "—";


        document.getElementById(
            "healthSummary"
        ).innerText =

            "Analyze a fruit to see nutritional and health information.";


        document.getElementById(
            "benefitsContainer"
        ).innerHTML = `

            <div class="benefit-card">

                <div class="benefit-icon">
                    🍎
                </div>

                <h3>
                    Waiting for Analysis
                </h3>

                <p>
                    Upload and analyze a fruit
                    image to view health benefits.
                </p>

            </div>

        `;


        document.getElementById(
            "tipsList"
        ).innerHTML = `

            <li>
                Wash fruits properly before consumption.
            </li>

            <li>
                Prefer fresh and properly stored fruits.
            </li>

            <li>
                Avoid visibly spoiled or moldy fruit.
            </li>

        `;


        document.getElementById(
            "aiMessage"
        ).innerHTML = `

            Upload a fruit image and click
            <strong>Analyze Fruit</strong>
            to generate an AI analysis.

        `;


        resetButton.style.display =
            "none";

    }
);


/* =====================================================
   DARK / LIGHT MODE
===================================================== */

themeButton.addEventListener(
    "click",
    function () {

        document.body.classList.toggle(
            "light-mode"
        );


        if (
            document.body.classList.contains(
                "light-mode"
            )
        ) {

            themeButton.innerText =
                "☀️";

        }

        else {

            themeButton.innerText =
                "🌙";

        }

    }
);


/* =====================================================
   INITIAL STATE
===================================================== */

resetButton.style.display =
    "none";

loadingStatus.style.display =
    "none";
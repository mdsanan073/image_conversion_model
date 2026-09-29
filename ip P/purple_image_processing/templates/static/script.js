```javascript
document.addEventListener(
    "DOMContentLoaded",
    function () {

        // =============================================
        // GET HTML ELEMENTS
        // =============================================

        const imageInput =
            document.getElementById("image");

        const filename =
            document.getElementById("filename");

        const form =
            document.getElementById("imageForm");

        const processButton =
            document.getElementById("processButton");


        // =============================================
        // SHOW SELECTED FILE NAME
        // =============================================

        imageInput.addEventListener(
            "change",
            function () {

                if (this.files.length > 0) {

                    const selectedFile =
                        this.files[0];

                    filename.style.display =
                        "block";

                    filename.textContent =
                        "Selected: " +
                        selectedFile.name;
                }

                else {

                    filename.style.display =
                        "none";

                    filename.textContent =
                        "";
                }
            }
        );


        // =============================================
        // IMAGE VALIDATION
        // =============================================

        imageInput.addEventListener(
            "change",
            function () {

                if (this.files.length === 0) {
                    return;
                }

                const file =
                    this.files[0];

                const allowedTypes = [
                    "image/jpeg",
                    "image/png",
                    "image/bmp",
                    "image/webp"
                ];

                if (
                    !allowedTypes.includes(
                        file.type
                    )
                ) {

                    alert(
                        "Please select a valid image file."
                    );

                    this.value = "";

                    filename.style.display =
                        "none";

                    filename.textContent =
                        "";
                }
            }
        );


        // =============================================
        // FORM SUBMIT
        // =============================================

        form.addEventListener(
            "submit",
            function () {

                if (
                    imageInput.files.length > 0
                ) {

                    processButton.disabled =
                        true;

                    processButton.textContent =
                        "⏳ Processing...";
                }
            }
        );


        // =============================================
        // OPERATION SELECTION
        // =============================================

        const operations =
            document.querySelectorAll(
                'input[name="operation"]'
            );


        operations.forEach(
            function (operation) {

                operation.addEventListener(
                    "change",
                    function () {

                        console.log(
                            "Selected operation:",
                            this.value
                        );
                    }
                );
            }
        );

    }
);
```

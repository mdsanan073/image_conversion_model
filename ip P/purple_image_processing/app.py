from flask import Flask, render_template, request, url_for
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# =========================================================
# FOLDERS
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "static", "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================================================
# ALLOWED FILE EXTENSIONS
# =========================================================
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "webp"}


def allowed_file(filename):
    return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================================================
# HOME PAGE
# =========================================================
@app.route("/", methods=["GET", "POST"])
def index():
    original_image = None
    output_image = None
    error = None
    current_image = None  # Tracks the active image

    if request.method == "POST":
        file = request.files.get("image")
        existing_image = request.form.get("current_image")

        # -------------------------------------------------
        # DETERMINE WHICH IMAGE TO USE
        # -------------------------------------------------
        if file and file.filename != "":
            # A NEW file was uploaded
            if not allowed_file(file.filename):
                error = "Invalid image format. Use JPG, JPEG, PNG, BMP or WEBP."
                return render_template("index.html", error=error)

            original_name = secure_filename(file.filename)
            name, extension = os.path.splitext(original_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = name + "_" + timestamp + extension

            input_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(input_path)
            current_image = filename
            print("New image saved:", input_path)

        elif existing_image:
            # NO new file, but an existing image is active
            filename = existing_image
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            current_image = filename

            if not os.path.exists(input_path):
                error = "Previous image lost from server. Please upload again."
                return render_template("index.html", error=error)
            print("Using existing image:", input_path)

        else:
            # No new file and no existing file
            error = "Please select an image."
            return render_template("index.html", error=error)

        # -------------------------------------------------
        # READ IMAGE USING OPENCV
        # -------------------------------------------------
        image = cv2.imread(input_path)

        if image is None:
            error = "OpenCV could not read the image data."
            return render_template("index.html", error=error)

        # -------------------------------------------------
        # GET SELECTED OPERATION
        # -------------------------------------------------
        operation = request.form.get("operation", "original")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # New timestamp for output

        # -------------------------------------------------
        # IMAGE PROCESSING
        # -------------------------------------------------
        try:
            if operation == "original":
                processed = image.copy()
            elif operation == "gray":
                processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            elif operation == "binary":
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, processed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            elif operation == "blur":
                processed = cv2.GaussianBlur(image, (15, 15), 0)
            elif operation == "edge":
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                processed = cv2.Canny(gray, 100, 200)
            elif operation == "threshold":
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, processed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            elif operation == "dilate":
                kernel = np.ones((5, 5), np.uint8)
                processed = cv2.dilate(image, kernel, iterations=1)
            elif operation == "erode":
                kernel = np.ones((5, 5), np.uint8)
                processed = cv2.erode(image, kernel, iterations=1)
            elif operation == "average":
                processed = cv2.blur(image, (5, 5))
            elif operation == "gaussian":
                processed = cv2.GaussianBlur(image, (5, 5), 0)
            elif operation == "laplacian":
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                processed = cv2.filter2D(image, -1, kernel)
            else:
                processed = image.copy()

        except Exception as e:
            print("Processing error:", e)
            error = "An error occurred while processing the image."
            return render_template("index.html", error=error, current_image=current_image)

        # -------------------------------------------------
        # SAVE PROCESSED IMAGE
        # -------------------------------------------------
        output_filename = "processed_" + timestamp + ".jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        saved = cv2.imwrite(output_path, processed)

        if not saved:
            error = "Could not save the processed image."
            return render_template("index.html", error=error, current_image=current_image)

        # -------------------------------------------------
        # CREATE IMAGE URLS
        # -------------------------------------------------
        original_image_url = url_for("static", filename="uploads/" + filename)
        output_image_url = url_for("static", filename="outputs/" + output_filename)

        return render_template(
            "index.html",
            original_image=original_image_url,
            output_image=output_image_url,
            current_image=current_image,
            error=error
        )

    # GET Request
    return render_template("index.html")


# =========================================================
# RUN FLASK
# =========================================================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
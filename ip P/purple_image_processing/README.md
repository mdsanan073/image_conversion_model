# Purple Image Processing

A web-based image processing application built with Python, Flask, and OpenCV.

## Features

- Upload images (JPG, JPEG, PNG, BMP, WEBP)
- Apply various image processing operations:
  - Original (no change)
  - Grayscale
  - Binary threshold
  - Gaussian blur
  - Edge detection (Canny)
  - Threshold

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Run the Flask app:
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Project Structure

```
purple_image_processing/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # HTML template
└── static/
    ├── uploads/          # Uploaded images (auto-created)
    └── outputs/          # Processed images (auto-created)
```

## Technologies Used

- **Flask**: Web framework
- **OpenCV**: Image processing library
- **HTML/CSS**: Frontend styling
- **JavaScript**: File upload interaction

## License

This is a student project for educational purposes.

# CV Document Chunker

A Python package for parsing PDF document layouts using YOLO models, chunking content based on layout, and optionally performing OCR.

## Features

- Convert PDF documents to images for processing.
- Detect document layout elements (e.g., paragraphs, tables, figures) using YOLO.
- Process and refine bounding boxes.
- Chunk document content based on detected layout.
- Generate annotated images showing detected elements.
- **(Optional)** Perform OCR on detected elements using Azure Document Intelligence.
- Save structured document data (layouts, chunks, OCR text) in JSON format.

## Installation

### Prerequisites

- Python 3.8+
- Pip package manager
- (Optional but Recommended) CUDA-capable GPU for YOLO model inference acceleration.

### Steps

1.  **Clone the Repository (for development or local install):**
    ```bash
    git clone <your-repository-url>
    cd cv-doc-parser
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    ```

3.  **Install the Package:**
    *   **Editable mode (recommended for development):**
        ```bash
        pip install -e .
        ```
    *   **Regular install:**
        ```bash
        pip install .
        ```
    *   **(If published on PyPI):**
        ```bash
        # pip install cv-doc-chunker
        ```

## User-Provided Data

This package requires the user to provide certain data externally:

1.  **Input Directory (`input/`):** Place the PDF documents you want to process in a directory (e.g., `input/`). You will need to provide the path to your input file(s) when using the package.
2.  **Models Directory (`models/`):** Download the necessary YOLO model(s) (e.g., `doclayout_yolo_docstructbench_imgsz1024.pt`) and place them in a dedicated directory (e.g., `models/`). The path to this directory (or the specific model file) will be needed by the parser.

## Usage

*(This section needs specific examples based on your library's API)*

Provide examples of how to import and use your library functions or the command-line tool.

**Example (Conceptual Python Usage):**

```python
from cv_doc_chunker import PDFProcessor

# --- User Configuration ---
input_pdf_path = "path/to/your/input/document.pdf" # Path to user's PDF
model_path = "path/to/your/models/doclayout_yolo.pt" # Path to user's model
output_dir = "path/to/your/output/" # Directory to save results

# --- Initialize and Run ---
processor = PDFProcessor(model_path=model_path, output_dir=output_dir)

# Process the document (layout detection, chunking, etc.)
results = processor.process_document(pdf_path=input_pdf_path)

# Optional: Perform OCR (requires Azure setup)
# ocr_results = processor.perform_ocr(results)

print(f"Processing complete. Results saved in {output_dir}")
```

**Example (Conceptual Command-Line Usage):**

*(Assumes the `cv-chunker` entry point is configured)*

```bash
cv-chunker --input path/to/your/input/document.pdf \
           --model path/to/your/models/doclayout_yolo.pt \
           --output path/to/your/output/ \
           [--ocr] [--azure-endpoint YOUR_ENDPOINT] [--azure-key YOUR_KEY]
```

**Note:** Update the conceptual examples above with the actual function names, class names, and command-line arguments provided by your `cv-doc-chunker` package.

## Understanding the Output

After running the parser, the following outputs will typically be available in the specified `output_dir`:

1.  `{your-document}_parsed.json`: JSON file containing the detected document structure (element labels, coordinates, confidence).
2.  `{your-document}_annotations/`: Directory containing annotated images showing the detected elements for each page (if `generate_annotations=True`).
3.  `{your-document}_boxes/`: Directory containing individual images for each detected element, organized by page number (if `save_bounding_boxes=True`). This is required for OCR.
4.  **`{your-document}_sorted_text.json`**: (Only if `ocr=True`) JSON file containing the extracted text for each element, sorted according to the structure defined in `_parsed.json`.

If debug mode is enabled (`debug_mode=True`), additional debug images might be saved, typically in a `debug/` subdirectory within the `output_dir`, showing intermediate steps of the parsing process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
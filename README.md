# Adobe Hackathon - Round 1A: PDF Outline Generation

This project is a solution for Round 1A of the Adobe India Hackathon. It parses PDF documents to automatically generate a structured outline, identifying the document's Title and various heading levels (H1, H2, H3).

---

## Our Approach

The core of our solution is a robust, heuristic-based approach to identify headings in PDFs, which often lack explicit structural metadata. Our process involves two main stages:

1.  **Parsing with PyMuPDF**: We use the `PyMuPDF` library to parse the input PDF. Instead of just extracting raw text, we extract structured text **blocks**, which correspond closely to paragraphs. This method preserves the document's reading order and provides a clean foundation for analysis. We chose `PyMuPDF` for its exceptional speed and reliability.

2.  **Heuristic Scoring for Heading Detection**: Once we have the text blocks, we analyze each one to determine if it's a heading. We use a flexible scoring system where each block gets points based on various clues:
    * **Numbered Patterns**: Blocks starting with patterns like `1.`, `2.1.`, etc., receive a high score.
    * **Case Formatting**: Blocks written in `ALL CAPS` or `Title Case` are strong indicators of headings.
    * **Structural Clues**: Short blocks (those with few words) that don't end with punctuation are also considered likely headings.

A block with a score above a set threshold is identified as a heading. The first heading found is designated as the **Title**, and subsequent headings are assigned levels (H1, H2, H3) based on their numbering pattern or a default level.

---

## Libraries Used

* **Python 3.9**: The core programming language.
* **PyMuPDF (fitz)**: A high-performance Python library for PDF parsing and text extraction.
* **Docker**: For containerizing the application to ensure a consistent and reproducible runtime environment.

---

## How to Build and Run Your Solution

To build and run this solution locally, please ensure you have Docker Desktop installed and running.

### 1. Build the Docker Image

Navigate to the project's root directory in your terminal and run the following command to build the Docker image:

```bash
docker build -t adobe-hackathon-1a .
```
### 2. Run the Docker Container

Before running, make sure your sample PDFs are placed inside the /app/input directory.

Use the following command to run the container. This command maps your local input and output folders to the folders inside the container.

(Note: This command is for bash/PowerShell. For cmd.exe, replace "/$(pwd)/..." with "%CD%\\...")

```bash
docker run --rm -v "/$(pwd)/app/input:/app/input" -v "/$(pwd)/app/output:/app/output" adobe-hackathon-1a
```
After the script finishes, the generated JSON outline files will appear in your local /app/output directory.

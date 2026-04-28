"""PDF processor for converting PDF pages to images."""

import os
from io import BytesIO
from typing import List

import fitz  # PyMuPDF
from PIL import Image

from .logger import get_logger


class PDFProcessor:
    """Process PDF files and convert pages to images."""

    def __init__(self, logger_name: str = "PDFProcessor"):
        """Initialize PDF processor.

        Args:
            logger_name: Name for the logger instance
        """
        self.logger = get_logger(logger_name)
        self.logger.info("PDFProcessor initialized")

    def validate_pdf(self, pdf_path: str) -> bool:
        """Validate if the file is a valid PDF.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            True if valid PDF, False otherwise
        """
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return False

        if not pdf_path.lower().endswith('.pdf'):
            self.logger.warning(f"File does not have .pdf extension: {pdf_path}")
            return False

        try:
            with fitz.open(pdf_path) as doc:
                if len(doc) == 0:
                    self.logger.error(f"PDF file is empty: {pdf_path}")
                    return False
                self.logger.info(f"PDF validated successfully: {pdf_path}", pages=len(doc))
                return True
        except Exception as e:
            self.logger.error(f"Failed to validate PDF: {pdf_path}", exception=e)
            return False

    def get_page_count(self, pdf_path: str) -> int:
        """Get the number of pages in the PDF.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Number of pages, or 0 if error occurs
        """
        try:
            with fitz.open(pdf_path) as doc:
                page_count = len(doc)
                self.logger.info(f"PDF page count: {page_count}", pdf_path=pdf_path)
                return page_count
        except Exception as e:
            self.logger.error(f"Failed to get page count: {pdf_path}", exception=e)
            return 0

    def pdf_to_images(self, pdf_path: str, dpi: int = 200) -> List[Image.Image]:
        """Convert PDF pages to PIL Image objects.

        Args:
            pdf_path: Path to the PDF file
            dpi: DPI for rendering (higher = better quality, larger size)

        Returns:
            List of PIL Image objects for each page
        """
        if not self.validate_pdf(pdf_path):
            return []

        images = []
        try:
            self.logger.info(f"Converting PDF to images: {pdf_path}", dpi=dpi)

            with fitz.open(pdf_path) as doc:
                total_pages = len(doc)
                zoom = dpi / 72.0  # Convert DPI to zoom factor

                for page_num in range(total_pages):
                    self.logger.log_page_progress(page_num + 1, total_pages, "Rendering")

                    page = doc[page_num]
                    mat = fitz.Matrix(zoom, zoom)  # Create transformation matrix
                    pix = page.get_pixmap(matrix=mat)  # Render page to pixmap

                    # Convert pixmap to PIL Image
                    img_bytes = pix.tobytes("png")
                    img = Image.open(BytesIO(img_bytes))
                    images.append(img)

                    self.logger.debug(f"Page {page_num + 1} converted to image",
                                     width=img.width,
                                     height=img.height)

            self.logger.info(f"Successfully converted {len(images)} pages to images")
            return images

        except Exception as e:
            self.logger.error(f"Failed to convert PDF to images: {pdf_path}", exception=e)
            return []

    def pdf_page_to_image(self, pdf_path: str, page_num: int, dpi: int = 200) -> Image.Image:
        """Convert a single PDF page to PIL Image object.

        Args:
            pdf_path: Path to the PDF file
            page_num: Page number (0-indexed)
            dpi: DPI for rendering

        Returns:
            PIL Image object for the requested page, or None if error
        """
        if not self.validate_pdf(pdf_path):
            return None

        try:
            self.logger.info(f"Converting page {page_num} to image: {pdf_path}", page_num=page_num)

            with fitz.open(pdf_path) as doc:
                if page_num < 0 or page_num >= len(doc):
                    self.logger.error(f"Invalid page number: {page_num}", total_pages=len(doc))
                    return None

                page = doc[page_num]
                zoom = dpi / 72.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                img_bytes = pix.tobytes("png")
                img = Image.open(BytesIO(img_bytes))

                self.logger.info(f"Page {page_num} converted successfully",
                                width=img.width,
                                height=img.height)
                return img

        except Exception as e:
            self.logger.error(f"Failed to convert page {page_num}: {pdf_path}",
                            page_num=page_num,
                            exception=e)
            return None
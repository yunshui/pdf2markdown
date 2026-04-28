"""PDF to Markdown converter main logic."""

import os
import time
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image

from .config import Config
from .logger import get_logger
from .model_client import ModelClient
from .pdf_processor import PDFProcessor
from .state_manager import StateManager


class PDFToMarkdownConverter:
    """Main converter class for PDF to Markdown conversion."""

    def __init__(self, config: Config, resume: bool = False):
        """Initialize converter.

        Args:
            config: Configuration object
            resume: Whether to resume from previous state
        """
        self.config = config
        self.resume = resume
        self.logger = get_logger("PDFToMarkdownConverter")

        # Initialize components
        self.pdf_processor = PDFProcessor()
        self.model_client = ModelClient(
            model_name=config.model_name,
            api_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout,
            max_retries=config.max_retries
        )

        # State manager will be initialized with PDF name
        self.state_manager = None

        self.logger.info("PDFToMarkdownConverter initialized",
                        model=config.model_name,
                        max_retries=config.max_retries)

    def convert(self, pdf_path: str) -> Tuple[bool, str]:
        """Convert PDF to Markdown.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Tuple of (success, output_path_or_error_message)
        """
        self.logger.info(f"Starting conversion: {pdf_path}")

        # Validate PDF
        if not self.pdf_processor.validate_pdf(pdf_path):
            return False, "Invalid PDF file"

        # Get page count
        page_count = self.pdf_processor.get_page_count(pdf_path)
        if page_count == 0:
            return False, "PDF has no pages"

        self.logger.info(f"PDF has {page_count} page(s)", page_count=page_count)

        # Convert based on page count
        if page_count == 1:
            return self._convert_single_page(pdf_path)
        else:
            return self._convert_multi_page(pdf_path, page_count)

    def _convert_single_page(self, pdf_path: str) -> Tuple[bool, str]:
        """Convert single-page PDF to Markdown.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Tuple of (success, output_path_or_error_message)
        """
        self.logger.info("Converting single-page PDF")

        # Convert PDF to images
        images = self.pdf_processor.pdf_to_images(pdf_path)
        if not images:
            return False, "Failed to convert PDF to images"

        # Call model to convert to Markdown
        try:
            start_time = time.time()
            markdown_content = self.model_client.call(
                prompt=self.config.single_page_prompt,
                images=images
            )
            duration = time.time() - start_time

            # Save to output
            output_path = self._get_single_page_output_path(pdf_path)
            self._save_markdown(output_path, markdown_content)

            self.logger.info(f"Single-page conversion complete: {output_path} (took {duration:.1f}s)")
            return True, output_path

        except Exception as e:
            self.logger.error("Single-page conversion failed", exception=e)
            return False, f"Conversion failed: {str(e)}"

    def _convert_multi_page(self, pdf_path: str, page_count: int) -> Tuple[bool, str]:
        """Convert multi-page PDF to Markdown with page structure.

        Args:
            pdf_path: Path to the PDF file
            page_count: Total number of pages

        Returns:
            Tuple of (success, output_directory_path_or_error_message)
        """
        base_name = Path(pdf_path).stem
        output_base_dir = os.path.join(self.config.output_dir, f"{base_name}_md")

        # Initialize state manager
        self.state_manager = StateManager(self.config.output_dir, base_name)

        # Check if resuming
        if self.resume:
            self.logger.info("Resuming from previous state")
            self.state_manager.show_progress()
            completed = self.state_manager.get_completed_pages()
            failed = self.state_manager.get_failed_pages()
            self.logger.info(f"Skipping {len(completed)} completed pages, {len(failed)} failed pages")
        else:
            # Reset state if not resuming
            self.state_manager.reset()
            self.state_manager.initialize(page_count)
            completed = set()
            failed = []

        # Convert PDF to images
        images = self.pdf_processor.pdf_to_images(pdf_path)
        if not images or len(images) != page_count:
            return False, "Failed to convert PDF to images"

        # Prepare output directories
        pages_dir = os.path.join(output_base_dir, "pages")
        os.makedirs(pages_dir, exist_ok=True)

        # Convert each page and collect summaries
        page_summaries = []
        self.logger.info(f"Processing {page_count} pages")

        print(f"\n{'='*60}")
        print(f"Converting PDF: {base_name}")
        print(f"{'='*60}")
        if self.resume:
            print(f"Resuming from page {len(completed) + 1}")
        print()

        for page_num in range(page_count):
            page_num_1based = page_num + 1

            # Skip if already completed
            if page_num_1based in completed:
                self.logger.info(f"Skipping already completed page {page_num_1based}")
                # Load existing summary if available
                summary_file = os.path.join(pages_dir, f"page_{page_num_1based}_summary.txt")
                if os.path.exists(summary_file):
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        summary = f.read()
                    page_summaries.append((page_num_1based, summary))
                else:
                    page_summaries.append((page_num_1based, f"Page {page_num_1based} (completed previously)"))
                continue

            # Check if failed previously
            was_failed = any(f['page'] == page_num_1based for f in failed)

            self.logger.log_page_progress(page_num_1based, page_count, "Converting")

            start_time = time.time()

            # Convert single page to full Markdown
            try:
                page_content = self.model_client.call(
                    prompt=self.config.single_page_prompt,
                    images=[images[page_num]]
                )

                # Save page content
                page_filename = f"page_{page_num_1based}.md"
                page_path = os.path.join(pages_dir, page_filename)
                self._save_markdown(page_path, page_content)

                # Get summary for navigation
                try:
                    summary = self.model_client.call(
                        prompt=self.config.multi_page_summary_prompt,
                        images=[images[page_num]]
                    )

                    # Save summary for recovery
                    summary_file = os.path.join(pages_dir, f"page_{page_num_1based}_summary.txt")
                    with open(summary_file, 'w', encoding='utf-8') as f:
                        f.write(summary)

                    page_summaries.append((page_num_1based, summary))
                    self.logger.debug(f"Page {page_num_1based} summary: {summary[:50]}...")
                except Exception as e:
                    self.logger.warning(f"Failed to get summary for page {page_num_1based}",
                                      exception=e)
                    page_summaries.append((page_num_1based, f"Page {page_num_1based}"))

                # Mark page as completed
                duration = time.time() - start_time
                self.state_manager.mark_page_completed(page_num_1based, duration)
                completed.add(page_num_1based)

                # Show progress
                avg_time = self.state_manager.get_average_time()
                estimated_remaining = self.state_manager.get_estimated_remaining_time()
                self.logger.print_progress(
                    completed=len(completed),
                    total=page_count,
                    failed=len(failed),
                    average_time=avg_time,
                    estimated_remaining=estimated_remaining,
                    current_page=page_num_1based
                )
                self.logger.log_time_estimation(page_num_1based, page_count, avg_time,
                                                self.state_manager.state['total_time'])

            except Exception as e:
                error_msg = str(e)
                self.logger.error(f"Failed to convert page {page_num_1based}", exception=e)

                # Create error placeholder file
                error_filename = f"page_{page_num_1based}_error.md"
                error_path = os.path.join(pages_dir, error_filename)
                error_content = f"""# Page {page_num_1based} - Conversion Failed

**Error:** {error_msg}

This page could not be converted to Markdown. Please check:
- The PDF page content is valid
- Your API key is valid and has sufficient quota
- Network connectivity is stable

You can try converting this page separately or increasing the timeout setting.
"""
                self._save_markdown(error_path, error_content)

                # Mark page as failed
                self.state_manager.mark_page_failed(page_num_1based, error_msg)

                # Add to failed list
                failed.append({"page": page_num_1based, "error": error_msg})

                # Show progress with failed page
                self.logger.print_progress(
                    completed=len(completed),
                    total=page_count,
                    failed=len(failed),
                    current_page=page_num_1based
                )
                print(f"\n  ⚠️  Page {page_num_1based} failed: {error_msg[:50]}...")

                # Continue to next page (don't return error)
                continue

        # Create main index file with links
        main_content = self._create_multi_page_index(base_name, page_summaries, failed)
        main_path = os.path.join(output_base_dir, f"{base_name}.md")
        self._save_markdown(main_path, main_content)

        # Mark conversion as completed
        self.state_manager.mark_completed()

        print()
        print(f"{'='*60}")
        if len(failed) == 0:
            print(f"✓ Multi-page conversion complete: {output_base_dir}")
        else:
            print(f"⚠️  Conversion complete with {len(failed)} failed page(s)")
            print(f"  Output: {output_base_dir}")
            print(f"\nFailed pages:")
            for fail in failed:
                print(f"  - Page {fail['page']}: {fail['error'][:60]}...")
        print(f"{'='*60}")

        self.logger.info(f"Multi-page conversion complete: {output_base_dir}",
                        completed=len(completed),
                        failed=len(failed))

        return True, output_base_dir

    def _create_multi_page_index(self, base_name: str,
                                  page_summaries: List[Tuple[int, str]],
                                  failed: List[dict] = None) -> str:
        """Create main index content for multi-page PDF.

        Args:
            base_name: Base name of the PDF file
            page_summaries: List of (page_num, summary) tuples
            failed: List of failed page information

        Returns:
            Markdown content for the index file
        """
        lines = [
            f"# {base_name}\n",
            "",
            "## 页面导航\n",
            "",
            "以下是各页面的转换结果：\n",
            ""
        ]

        for page_num, summary in page_summaries:
            page_filename = f"page_{page_num}.md"
            relative_path = f"pages/{page_filename}"
            lines.append(f"- [第 {page_num} 页: {summary}]({relative_path})")
            lines.append("")

        # Add failed pages section
        if failed:
            lines.extend([
                "---",
                "",
                "## 转换失败的页面\n",
                ""
            ])
            for fail in failed:
                lines.append(f"- **页面 {fail['page']}**: {fail['error']}")
                lines.append("")
            lines.append("")
            lines.append("可以尝试：")
            lines.append("1. 增加超时时间")
            lines.append("2. 检查网络连接")
            lines.append("3. 验证API密钥")
            lines.append("4. 使用 --resume 从失败处继续")

        lines.extend([
            "---",
            "",
            "*本文档由 PDF 转 Markdown 工具自动生成*"
        ])

        return "\n".join(lines)

    def _get_single_page_output_path(self, pdf_path: str) -> str:
        """Get output path for single-page PDF conversion.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Output Markdown file path
        """
        base_name = Path(pdf_path).stem
        os.makedirs(self.config.output_dir, exist_ok=True)
        return os.path.join(self.config.output_dir, f"{base_name}.md")

    def _save_markdown(self, file_path: str, content: str) -> None:
        """Save Markdown content to file.

        Args:
            file_path: Path to save the file
            content: Markdown content to save
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.logger.debug(f"Saved Markdown to: {file_path}",
                         content_length=len(content))
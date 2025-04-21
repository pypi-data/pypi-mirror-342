"""Tests for document processing functionality."""

import logging
import shutil
from pathlib import Path

import pytest

from pdfbaker.baker import PDFBaker, PDFBakerOptions
from pdfbaker.document import PDFBakerDocument
from pdfbaker.errors import ConfigurationError


@pytest.fixture(name="baker_config")
def fixture_baker_config(tmp_path: Path) -> Path:
    """Create a baker configuration file."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
    documents: [test_doc]
    """)
    return config_file


@pytest.fixture(name="baker_options")
def fixture_baker_options(tmp_path: Path) -> PDFBakerOptions:
    """Create baker options with test-specific build/dist directories."""
    return PDFBakerOptions(
        default_config_overrides={
            "directories": {
                "build": str(tmp_path / "build"),
                "dist": str(tmp_path / "dist"),
            }
        }
    )


@pytest.fixture(name="doc_dir")
def fixture_doc_dir(tmp_path: Path) -> Path:
    """Create a document directory with all necessary files."""
    doc_path = tmp_path / "test_doc"
    doc_path.mkdir()

    # Create config file
    config_file = doc_path / "config.yaml"
    config_file.write_text("""
    pages: [page1.yaml]
    directories:
        build: build
    """)

    # Create page config
    pages_dir = doc_path / "pages"
    pages_dir.mkdir()
    page_file = pages_dir / "page1.yaml"
    page_file.write_text("template: template.svg")

    # Create template
    templates_dir = doc_path / "templates"
    templates_dir.mkdir()
    template_file = templates_dir / "template.svg"
    template_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
    )

    yield doc_path

    # Cleanup
    shutil.rmtree(doc_path, ignore_errors=True)


def test_document_init_with_dir(
    baker_config: Path, baker_options: PDFBakerOptions, doc_dir: Path
) -> None:
    """Test document initialization with directory."""
    baker = PDFBaker(config_file=baker_config, options=baker_options)
    doc = PDFBakerDocument(
        baker=baker,
        base_config=baker.config,
        config_path=doc_dir,  # this will default to config.yaml in the directory
    )
    assert doc.config.name == "test_doc"
    assert doc.config["pages"] == ["page1.yaml"]

    # We need to manually determine pages now
    doc.config.determine_pages(doc.config)
    assert len(doc.config.pages) > 0
    assert doc.config.pages[0].name == "page1.yaml"


def test_document_init_with_file(
    tmp_path: Path, baker_config: Path, baker_options: PDFBakerOptions
) -> None:
    """Test document initialization with config file."""
    # Create document config
    config_file = tmp_path / "test_doc.yaml"
    config_file.write_text("""
    pages: [page1.yaml]
    directories:
        build: build
    """)

    # Create page config
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    page_file = pages_dir / "page1.yaml"
    page_file.write_text("template: template.svg")

    # Create template
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    template_file = templates_dir / "template.svg"
    template_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
    )

    baker = PDFBaker(baker_config, options=baker_options)
    doc = PDFBakerDocument(baker, baker.config, config_file)
    assert doc.config.name == "test_doc"
    assert doc.config["pages"] == ["page1.yaml"]


def test_document_init_missing_pages(tmp_path: Path, baker_config: Path) -> None:
    """Test document initialization with missing pages key."""
    config_file = tmp_path / "test_doc.yaml"
    config_file.write_text("""
    title: Test Document
    directories:
        build: build
    """)

    baker = PDFBaker(baker_config)
    with pytest.raises(ConfigurationError, match="Cannot determine pages"):
        PDFBakerDocument(baker, baker.config, config_file)


def test_document_custom_bake(
    baker_config: Path, baker_options: PDFBakerOptions, doc_dir: Path
) -> None:
    """Test document processing with custom bake module."""
    # Create custom bake module
    bake_file = doc_dir / "bake.py"
    bake_file.write_text("""
def process_document(document):
    return document.config.build_dir / "custom.pdf"
""")

    baker = PDFBaker(baker_config, options=baker_options)
    doc = PDFBakerDocument(baker, baker.config, doc_dir)
    assert doc.config.name == "test_doc"
    assert doc.config["pages"] == ["page1.yaml"]


def test_document_custom_bake_error(
    baker_config: Path, baker_options: PDFBakerOptions, doc_dir: Path
) -> None:
    """Test document processing with invalid custom bake module."""
    # Create invalid bake module
    bake_file = doc_dir / "bake.py"
    bake_file.write_text("raise Exception('Test error')")

    baker = PDFBaker(baker_config, options=baker_options)
    doc = PDFBakerDocument(baker, baker.config, doc_dir)
    assert doc.config.name == "test_doc"
    assert doc.config["pages"] == ["page1.yaml"]


def test_document_variants(
    baker_config: Path, baker_options: PDFBakerOptions, doc_dir: Path
) -> None:
    """Test document processing with variants."""
    # Update config file
    config_file = doc_dir / "config.yaml"
    config_file.write_text("""
    pages: [page1.yaml]
    directories:
        build: build
    variants:
        - name: variant1
          filename: variant1
        - name: variant2
          filename: variant2
    """)

    baker = PDFBaker(baker_config, options=baker_options)
    doc = PDFBakerDocument(baker, baker.config, doc_dir)
    assert doc.config.name == "test_doc"
    assert doc.config["pages"] == ["page1.yaml"]
    assert len(doc.config["variants"]) == 2


def test_document_variants_with_different_pages(
    tmp_path: Path, baker_config: Path, baker_options: PDFBakerOptions
) -> None:
    """Test document with variants where each variant has different pages."""
    # Create document config with variants but no pages
    config_file = tmp_path / "test_doc.yaml"
    config_file.write_text("""
    filename: "{{ variant.name }}_doc"
    directories:
        build: build
        dist: dist
    variants:
        - name: variant1
          filename: variant1
          pages: [page1.yaml]
        - name: variant2
          filename: variant2
          pages: [page2.yaml]
    """)

    # Create page configs
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()

    page_file1 = pages_dir / "page1.yaml"
    page_file1.write_text("""
    template: template.svg
    content: "Variant 1 content"
    """)

    page_file2 = pages_dir / "page2.yaml"
    page_file2.write_text("""
    template: template.svg
    content: "Variant 2 content"
    """)

    # Create template
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    template_file = templates_dir / "template.svg"
    template_file.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>'
    )

    baker = PDFBaker(baker_config, options=baker_options)
    doc = PDFBakerDocument(baker, baker.config, config_file)

    # Check that document initialization works without pages at doc level
    assert doc.config.name == "test_doc"
    assert "pages" not in doc.config
    assert len(doc.config["variants"]) == 2

    # Check that each variant has its own pages definition
    assert doc.config["variants"][0]["pages"] == ["page1.yaml"]
    assert doc.config["variants"][1]["pages"] == ["page2.yaml"]

    # Test that processing works with per-variant pages
    # We don't need to call process for this basic functionality test
    # as that would require inkapscape/cairosvg and be more integration testing

    # Instead, test that we can determine pages from variant configs
    variant1_config = doc.config.copy()
    variant1_config.update(doc.config["variants"][0])
    assert "pages" in variant1_config
    doc.config.determine_pages(variant1_config)
    assert len(doc.config.pages) > 0
    assert doc.config.pages[0].name == "page1.yaml"

    variant2_config = doc.config.copy()
    variant2_config.update(doc.config["variants"][1])
    assert "pages" in variant2_config
    doc.config.determine_pages(variant2_config)
    assert len(doc.config.pages) > 0
    assert doc.config.pages[0].name == "page2.yaml"


def test_document_teardown(
    baker_config: Path,
    baker_options: PDFBakerOptions,
    doc_dir: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test document teardown."""
    # Create build directory and some files
    build_dir = doc_dir / "build" / "test_doc"
    build_dir.mkdir(parents=True)
    (build_dir / "file1.pdf").write_text("test")
    (build_dir / "file2.pdf").write_text("test")

    baker = PDFBaker(baker_config, options=baker_options)
    doc = PDFBakerDocument(baker, baker.config, doc_dir)
    assert doc.config.name == "test_doc"
    assert doc.config["pages"] == ["page1.yaml"]

    with caplog.at_level(logging.DEBUG):
        # Manually reinstall caplog handler to the root logger
        logging.getLogger().addHandler(caplog.handler)
        doc.teardown()

    assert not build_dir.exists()
    assert "Tearing down build directory" in caplog.text
    assert "Removing files in build directory" in caplog.text
    assert "Removing build directory" in caplog.text

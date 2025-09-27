"""
__init__.py to make headline_scraper a package
"""

# src/headline_scraper/__init__.py
from .log_setup import setup_logging

__all__ = ["setup_logging"]  # only expose these names

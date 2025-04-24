"""
Robot Framework AI DomRetryLibrary
==================================

A Robot Framework library that provides an AI-powered fallback mechanism for locator variables.
This library enhances test reliability by using OpenAI to dynamically generate element locators
when the primary locators fail.

For more information and usage examples, see:
https://github.com/plaushku/robot-ai-domretrylibrary
"""

from .dom_retry_library import DomRetryLibrary

__version__ = "0.1.0"
__author__ = "Kristijan Plaushku" 
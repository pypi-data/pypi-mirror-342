#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from robot.api.deco import keyword
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium import webdriver

@keyword
def get_edge_driver():
    """
    Get an Edge WebDriver instance with automatic driver management.
    
    This keyword automatically downloads and configures the appropriate
    Edge WebDriver for the installed Edge browser version.
    
    Returns:
        WebDriver: A configured Edge WebDriver instance
    """
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=service, options=options)
    return driver 
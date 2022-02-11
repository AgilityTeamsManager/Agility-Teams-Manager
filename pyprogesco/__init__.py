#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyprogesco main module.
"""
import logging

from pyprogesco.scrapers.calendar import Calendar

logging.info("Loading calendar...")
calendar: Calendar = Calendar()
logging.info("Loading calendar... Done.")
"""Events calendar."""

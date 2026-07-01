"""Parser package — adapter over Behave's built-in parser."""

from behave_model.parser.adapter import BehaveParserAdapter
from behave_model.parser.loader import load_feature, load_project
from behave_model.parser.parser import parse_feature, parse_project

__all__ = [
    "BehaveParserAdapter",
    "load_feature",
    "load_project",
    "parse_feature",
    "parse_project",
]

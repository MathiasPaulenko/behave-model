"""behave-model — Canonical object model for Behave projects.

Public API:

    from behave_model import (
        load_project,
        load_feature,
        Project,
        Feature,
        Scenario,
        ScenarioOutline,
        Step,
        Table,
        Tag,
        Background,
        Examples,
        DocString,
        Comment,
        Location,
        Metadata,
        Visitor,
        Validator,
        DictSerializer,
        JsonSerializer,
        PrettyPrinter,
    )

    project = load_project("features/")
    print(project.statistics())
"""

from behave_model.exceptions import (
    BehaveModelError,
    ParseError,
    SerializationError,
    TransformationError,
    ValidationError,
)
from behave_model.model import (
    Background,
    Comment,
    DocString,
    Examples,
    Feature,
    Location,
    Metadata,
    Project,
    Rule,
    Scenario,
    ScenarioOutline,
    Step,
    Table,
    TableRow,
    Tag,
)
from behave_model.parser import (
    BehaveParserAdapter,
    load_feature,
    load_project,
    parse_feature,
    parse_project,
)
from behave_model.queries import (
    find_feature,
    find_features_with_tag,
    find_outlines,
    find_plain_scenarios,
    find_scenarios,
    find_scenarios_with_tag,
    find_steps,
    find_tag,
)
from behave_model.serializers import DictSerializer, JsonSerializer, PrettyPrinter
from behave_model.transformations import (
    add_tag_to_feature,
    normalize_whitespace,
    remove_tag,
    rename_scenario,
    rename_tag,
    sort_features,
    sort_scenarios,
    sort_tags,
)
from behave_model.validation import (
    DuplicateFeatureNamesRule,
    DuplicateScenarioNamesRule,
    EmptyFeatureRule,
    EmptyScenarioRule,
    InvalidTableRule,
    ValidationIssue,
    ValidationRule,
    Validator,
)
from behave_model.visitors import CollectingVisitor, CountingVisitor, Visitor

__version__ = "0.1.0"

__all__ = [
    # model
    "Background",
    "Comment",
    "DocString",
    "Examples",
    "Feature",
    "Location",
    "Metadata",
    "Project",
    "Rule",
    "Scenario",
    "ScenarioOutline",
    "Step",
    "Table",
    "TableRow",
    "Tag",
    # parser
    "BehaveParserAdapter",
    "load_feature",
    "load_project",
    "parse_feature",
    "parse_project",
    # queries
    "find_feature",
    "find_features_with_tag",
    "find_outlines",
    "find_plain_scenarios",
    "find_scenarios",
    "find_scenarios_with_tag",
    "find_steps",
    "find_tag",
    # visitors
    "CollectingVisitor",
    "CountingVisitor",
    "Visitor",
    # serializers
    "DictSerializer",
    "JsonSerializer",
    "PrettyPrinter",
    # transformations
    "add_tag_to_feature",
    "normalize_whitespace",
    "remove_tag",
    "rename_scenario",
    "rename_tag",
    "sort_features",
    "sort_scenarios",
    "sort_tags",
    # validation
    "DuplicateFeatureNamesRule",
    "DuplicateScenarioNamesRule",
    "EmptyFeatureRule",
    "EmptyScenarioRule",
    "InvalidTableRule",
    "ValidationIssue",
    "ValidationRule",
    "Validator",
    # exceptions
    "BehaveModelError",
    "ParseError",
    "SerializationError",
    "TransformationError",
    "ValidationError",
    # version
    "__version__",
]

"""Tests for Rule support (Gherkin v6)."""

from __future__ import annotations

from pathlib import Path

import pytest

from behave_model.model import Project, Scenario
from behave_model.parser.adapter import BehaveParserAdapter
from behave_model.parser.loader import load_feature, load_project
from behave_model.parser.parser import parse_feature
from behave_model.serializers import DictSerializer, JsonSerializer, PrettyPrinter
from behave_model.visitors import CollectingVisitor, CountingVisitor, Visitor

RULES_FEATURE_TEXT = """\
@auth
Feature: User Account Management
  As a registered user

  Background:
    Given the user is logged in

  Rule: Profile updates
    Background:
      Given the user has a profile

    Scenario: Update display name
      When the user changes their display name to "Alice"
      Then the profile should show "Alice"

  Rule: Password management
    @security
    Scenario: Change password
      When the user changes their password
      Then the password should be updated

    Scenario Outline: Password validation
      When the user tries to set password "<password>"
      Then the validation should <result>

      Examples:
        | password  | result  |
        | short     | fail    |
        | longenough| succeed |
"""


@pytest.fixture
def rules_feature():
    bf = parse_feature(RULES_FEATURE_TEXT, filename="rules.feature")
    adapter = BehaveParserAdapter()
    return adapter.adapt_feature(bf, filename="rules.feature")


@pytest.fixture
def rules_project(rules_feature):
    return Project(features=[rules_feature])


class TestRuleModel:
    def test_rule_has_name(self, rules_feature):
        assert len(rules_feature.rules) == 2
        assert rules_feature.rules[0].name == "Profile updates"
        assert rules_feature.rules[1].name == "Password management"

    def test_rule_has_scenarios(self, rules_feature):
        rule = rules_feature.rules[0]
        assert len(rule.scenarios) == 1
        assert isinstance(rule.scenarios[0], Scenario)
        assert rule.scenarios[0].name == "Update display name"

    def test_rule_has_background(self, rules_feature):
        rule = rules_feature.rules[0]
        assert rule.background is not None
        assert len(rule.background.steps) == 1
        assert rule.background.steps[0].name == "the user has a profile"

    def test_rule_has_tags(self, rules_feature):
        # @security is on the scenario inside the rule, not on the rule itself
        rule = rules_feature.rules[1]
        assert len(rule.tags) == 0
        assert rule.scenarios[0].has_tag("@security")

    def test_rule_all_steps(self, rules_feature):
        rule = rules_feature.rules[0]
        steps = rule.all_steps()
        # background(1) + scenario(2) = 3
        assert len(steps) == 3

    def test_rule_all_scenarios(self, rules_feature):
        rule = rules_feature.rules[1]
        scenarios = rule.all_scenarios()
        assert len(scenarios) == 2

    def test_rule_has_tag(self, rules_feature):
        # @security is on the scenario inside the rule
        assert rules_feature.rules[1].scenarios[0].has_tag("@security")
        assert not rules_feature.rules[1].has_tag("@nonexistent")

    def test_rule_tag_names(self, rules_feature):
        # Rule itself has no tags; the scenario inside does
        assert rules_feature.rules[1].tag_names == []
        assert rules_feature.rules[1].scenarios[0].tag_names == ["@security"]

    def test_rule_len(self, rules_feature):
        assert len(rules_feature.rules[0]) == 1
        assert len(rules_feature.rules[1]) == 2

    def test_rule_iter(self, rules_feature):
        rule = rules_feature.rules[1]
        names = [s.name for s in rule]
        assert "Change password" in names


class TestFeatureWithRules:
    def test_all_scenarios_includes_rules(self, rules_feature):
        all_s = rules_feature.all_scenarios()
        # 0 direct + 1 (rule1) + 2 (rule2) = 3
        assert len(all_s) == 3

    def test_all_steps_includes_rules(self, rules_feature):
        steps = rules_feature.all_steps()
        # feature bg(1) + rule1 bg(1) + rule1 scenario(2) + rule2 scenario(2) + rule2 outline(2) = 8
        assert len(steps) == 8

    def test_all_tags_includes_rules(self, rules_feature):
        tags = rules_feature.all_tags()
        names = {t.name for t in tags}
        assert "@auth" in names
        assert "@security" in names


class TestRuleParsing:
    def test_load_from_file(self):
        path = Path(__file__).resolve().parent.parent / "examples" / "rules.feature"
        f = load_feature(path)
        assert f.name == "User Account Management"
        assert len(f.rules) == 2
        assert len(f.all_scenarios()) == 4
        assert len(f.all_steps()) == 10

    def test_load_project_with_rules(self):
        path = Path(__file__).resolve().parent.parent / "examples"
        project = load_project(path)
        rules_feature = project.find_feature("User Account Management")
        assert rules_feature is not None
        assert len(rules_feature.rules) == 2


class TestRuleVisitor:
    def test_counting_visitor_counts_rules(self, rules_project):
        v = CountingVisitor()
        rules_project.accept(v)
        assert v.counts.get("rule", 0) == 2

    def test_collecting_visitor_collects_rules(self, rules_project):
        v = CollectingVisitor()
        rules_project.accept(v)
        assert "rule" in v.collection
        assert len(v.collection["rule"]) == 2

    def test_custom_visitor_visits_rule_scenarios(self, rules_project):
        class RuleScenarioCollector(Visitor):
            def __init__(self):
                self.scenarios = []

            def visit_scenario(self, scenario):
                self.scenarios.append(scenario.name)

        v = RuleScenarioCollector()
        rules_project.accept(v)
        assert "Update display name" in v.scenarios
        assert "Change password" in v.scenarios


class TestRuleTraversal:
    def test_dfs_includes_rules(self, rules_project):
        nodes = list(rules_project.walk())
        types = [type(n).__name__ for n in nodes]
        assert "Rule" in types

    def test_bfs_includes_rules(self, rules_project):
        nodes = list(rules_project.walk(strategy="bfs"))
        types = [type(n).__name__ for n in nodes]
        assert "Rule" in types

    def test_dfs_and_bfs_same_count(self, rules_project):
        dfs = list(rules_project.walk())
        bfs = list(rules_project.walk(strategy="bfs"))
        assert len(dfs) == len(bfs)


class TestRuleSerialization:
    def test_dict_serializer_includes_rules(self, rules_feature):
        ser = DictSerializer()
        data = ser.serialize_feature(rules_feature)
        assert "rules" in data
        assert len(data["rules"]) == 2
        assert data["rules"][0]["type"] == "rule"
        assert data["rules"][0]["name"] == "Profile updates"

    def test_dict_serializer_rule_background(self, rules_feature):
        ser = DictSerializer()
        data = ser.serialize_feature(rules_feature)
        assert data["rules"][0]["background"] is not None
        assert len(data["rules"][0]["background"]["steps"]) == 1

    def test_json_serializer_includes_rules(self, rules_feature):
        import json

        ser = JsonSerializer()
        text = ser.serialize_feature(rules_feature)
        data = json.loads(text)
        assert len(data["rules"]) == 2


class TestRulePrettyPrinter:
    def test_print_feature_with_rules(self, rules_feature):
        printer = PrettyPrinter()
        text = printer.print_feature(rules_feature)
        assert "Rule: Profile updates" in text
        assert "Rule: Password management" in text
        assert "Scenario: Update display name" in text
        assert "Scenario: Change password" in text
        assert "Scenario Outline: Password validation" in text

    def test_roundtrip(self, rules_feature):
        printer = PrettyPrinter()
        text = printer.print_feature(rules_feature)
        bf = parse_feature(text, filename="rt.feature")
        adapter = BehaveParserAdapter()
        f2 = adapter.adapt_feature(bf, filename="rt.feature")
        assert f2.name == rules_feature.name
        assert len(f2.rules) == len(rules_feature.rules)
        assert len(f2.all_scenarios()) == len(rules_feature.all_scenarios())
        assert len(f2.all_steps()) == len(rules_feature.all_steps())

    def test_roundtrip_from_file(self):
        path = Path(__file__).resolve().parent.parent / "examples" / "rules.feature"
        f = load_feature(path)
        printer = PrettyPrinter()
        text = printer.print_feature(f)
        bf = parse_feature(text, filename="rt.feature")
        adapter = BehaveParserAdapter()
        f2 = adapter.adapt_feature(bf, filename="rt.feature")
        assert f2.name == f.name
        assert len(f2.rules) == len(f.rules)
        assert len(f2.all_scenarios()) == len(f.all_scenarios())
        assert len(f2.all_steps()) == len(f.all_steps())


class TestRuleQueries:
    def test_find_scenarios_in_rules(self, rules_project):
        results = rules_project.find_scenarios(name="Update display name")
        assert len(results) == 1

    def test_find_scenarios_by_tag_in_rules(self, rules_project):
        results = rules_project.find_scenarios(tag="@security")
        assert len(results) == 1
        assert results[0].name == "Change password"

    def test_find_steps_in_rules(self, rules_project):
        results = rules_project.find_steps(keyword="When")
        assert len(results) > 0

    def test_statistics_with_rules(self, rules_project):
        stats = rules_project.statistics()
        assert stats["scenarios"] == 3
        assert stats["steps"] == 8

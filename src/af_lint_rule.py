# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------
import logging
import verible_verilog_syntax
import textwrap
from abc import ABC, abstractmethod

class AsFigoLintRule(ABC):
    """Base class for all linting rules."""

    VeribleSyntax = verible_verilog_syntax
    rule_count = 0  # Class variable to track rules executed

    
    def __init__(self, linter):
        self.linter = linter  # Store the linter instance
        self.ruleID = 'FCOVLintDefaultRuleID'
        '''
        if not hasattr(self, "ruleID"):  # Ensure ruleID exists in subclasses
            raise ValueError(f"{self.__class__.__name__} must define a `ruleID` attribute!")
        '''


    @classmethod
    def get_rule_count(cls):
        return cls.rule_count  # Get the count of rules applied

    @abstractmethod
    def apply(self, filePath: str, data: verible_verilog_syntax.SyntaxData):
        """Abstract method to apply the rule."""
        raise NotImplementedError

    def getClassName(self, classNode):
        """Extracts the class name from a class declaration."""
        for header in classNode.iter_find_all({"tag": "kClassHeader"}):
            for identifier in header.iter_find_all({"tag": "SymbolIdentifier"}):
                return identifier.text
        return "Unknown"

    def getQualifiers(self, varNode):
        """Extracts variable qualifiers (e.g., local, protected, rand)."""
        qualifiers = set()
        for qualList in varNode.iter_find_all({"tag": "kQualifierList"}):
            qualifiers.update(qualList.text.split())  # Extract words
        return qualifiers

    def run(self, filePath: str, data: verible_verilog_syntax.SyntaxData):
        """Wrapper method to automatically count and apply the rule."""
        AsFigoLintRule.rule_count += 1  # Automatically increment rule count
        message = (
                f"Running lint ruleID: {self.ruleID} on file: {filePath}\n"
                )

        self.linter.logInfo(self.ruleID, message)

        self.apply(filePath, data)  # Call the actual rule logic

    def formatViolationMessage(
        self,
        description: str,
        code_snippet: str = None,
        fix_suggestion: str = None,
    ) -> str:
        """
        Pretty-formats a linter violation with structured layout and indented code blocks.
        """
        lines = []
        # Add structured description and fix guidance
        if description:
            lines.append(f"  = Description: {description}")

        # Add code snippet block with visual margin
        if code_snippet:
            snippet_clean = textwrap.dedent(code_snippet.strip())
            lines.append("   |")
            for line in snippet_clean.splitlines():
                lines.append(f"   | {line}")
            lines.append("   |")

        if fix_suggestion:
            lines.append(f"  = Fix: {fix_suggestion}")

        return "\n".join(lines)


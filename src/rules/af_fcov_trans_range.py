# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVTransRangeVlt(AsFigoLintRule):
    """
    AF_VLT_FCOV_TRANS_RANGE:
    Covergroup transition bins shall not contain value ranges ([low:high]).
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_VLT_FCOV_TRANS_RANGE"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        # 1. Search for all bin declarations in covergroups
        for binNode in data.tree.iter_find_all({"tag": "kCoverageBin"}):

            # 2. Look for transition parenthesis groups
            for parenGroup in binNode.iter_find_all({"tag": "kParenGroup"}):

                # Look for '=>' anywhere within the parenGroup subtree
                has_transition = any(
                    hasattr(node, "text") and node.text.strip() == "=>"
                    for node in parenGroup.descendants
                )

                if has_transition:
                    # Check if a kValueRange exists anywhere in this paren group
                    has_range = any(
                        parenGroup.iter_find_all({"tag": "kValueRange"})
                    )

                    if has_range:
                        raw_code = binNode.text

                        message = self.formatViolationMessage(
                                description="Verilator compatibility: Transition sequence bin uses an unsupported value range '[...]' in transition.",
                            code_snippet=raw_code,
                            fix_suggestion="Replace the value range ([low:high] => ...) with discrete values or explicit bin lists."
                        )

                        self.linter.logViolation(
                            self.ruleID,
                            message,
                        )


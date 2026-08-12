# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVNoILBinsFunc(AsFigoLintRule):
    """
    AF_FCOV_AVOID_ILLEGAL_BINS:
    Covergroups shall not use 'illegal_bins'. Use SystemVerilog Assertions (SVA) 
    or a Scoreboard to catch illegal states/transitions to prevent masking errors.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_AVOID_ILLEGAL_BINS"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        # 1. Iterate over all coverage bin nodes in covergroups
        for binNode in data.tree.iter_find_all({"tag": "kCoverageBin"}):

            # 2. Check if 'illegal_bins' token exists in the bin subtree
            is_illegal_bin = any(
                hasattr(node, "text") and node.text.strip() == "illegal_bins"
                for node in binNode.descendants
            )

            if is_illegal_bin:
                raw_code = binNode.text

                message = self.formatViolationMessage(
                    description="Avoid using 'illegal_bins' in functional coverage as it causes simulation errors that can disrupt testbench flow or mask UVM error reporting.",
                    code_snippet=raw_code,
                    fix_suggestion="Use 'ignore_bins' to exclude unwanted values from coverage metrics, and enforce illegal state checking via SVA (SystemVerilog Assertions) or Scoreboard checks."
                )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

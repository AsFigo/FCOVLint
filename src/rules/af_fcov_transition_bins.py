# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVTrBinsRuleVlt(AsFigoLintRule):
    """AF_FCOV_TRANS_BINS_VLT : Avoid multi-value transition bins."""

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_TRANS_BINS_VLT"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):

        #
        # Search all bins declarations
        #
        for curNode in data.tree.iter_find_all({"tag": "kCoverageBin"}):

            lvBinCode = curNode.text

            #
            # Only transition bins contain =>
            #
            if "=>" not in lvBinCode:
                continue

            #
            # Extract transition expression
            #
            expr = lvBinCode.split("=>")

            if len(expr) != 2:
                continue

            lhs = expr[0]
            rhs = expr[1]

            #
            # Remove parentheses
            #
            lhs = lhs.replace("(", "").replace(")", "")
            rhs = rhs.replace("(", "").replace(")", "")

            #
            # Count comma-separated values
            #
            lhs_values = [x.strip() for x in lhs.split(",") if x.strip()]
            rhs_values = [x.strip() for x in rhs.split(",") if x.strip()]

            #
            # FCOV-008 violation
            #
            if len(lhs_values) > 1 or len(rhs_values) > 1:

                message = (
                    "Verilator compatibility: "
                    "FCOV: Multi-value transition bins are not supported.\n"
                    "Use one value on each side of the transition operator.\n"
                    f"{lvBinCode}\n"
                )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

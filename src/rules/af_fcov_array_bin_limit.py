# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVArrayBinLimitRule(AsFigoLintRule):
    """
    AF_FCOV_VLT_TRANS_RANGE :
    Array-based coverpoint bins shall not expand
    beyond the supported maximum bin count.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_VLT_TRANS_RANGE"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):

        MAX_BINS = 1024

        #
        # Search all coverage bins
        #
        for binNode in data.tree.iter_find_all({"tag": "kCoverageBin"}):

            #
            # Array bins only
            #
            bracketNode = next(
                binNode.iter_find_all({"tag": "kBracketGroup"}),
                None,
            )

            if bracketNode is None:
                continue

            #
            # Get value range
            #
            rangeNode = next(
                binNode.iter_find_all({"tag": "kValueRange"}),
                None,
            )

            if rangeNode is None:
                continue

            exprList = list(
                rangeNode.iter_find_all({"tag": "kExpression"})
            )

            if len(exprList) != 2:
                continue

            lowNode = next(
                exprList[0].iter_find_all({"tag": "kNumber"}),
                None,
            )

            highNode = next(
                exprList[1].iter_find_all({"tag": "kNumber"}),
                None,
            )

            if lowNode is None or highNode is None:
                continue

            low = int(lowNode.text)
            high = int(highNode.text)

            binCount = high - low + 1

            #
            # FCOV-005 violation
            #
            if binCount > MAX_BINS:

                message = (
                    "Verilator compatibility: "
                    "FCOV: Array-based coverpoint bins shall not "
                    "expand beyond the supported maximum bin count.\n"
                    f"{binNode.text}\n"
                )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

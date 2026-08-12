# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVConstOptionVlt(AsFigoLintRule):
    """
    AF_VLT_FCOV_USE_CONST_OPT :
    option.at_least and option.auto_bin_max shall be
    assigned constant integer values.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_VLT_FCOV_USE_CONST_OPT"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):

        #
        # Search all coverage options
        #
        for optionNode in data.tree.iter_find_all({"tag": "kCoverageOption"}):

            #
            # Get option name
            #
            lvOptionName = None

            optionNameIter = optionNode.iter_find_all(
                {"tag": "SymbolIdentifier"}
            )

            optionNameNode = next(optionNameIter, None)

            if optionNameNode is not None:
                lvOptionName = optionNameNode.text.strip()

            if lvOptionName not in ("at_least", "auto_bin_max"):
                continue

            #
            # Get option expression
            #
            exprIter = optionNode.iter_find_all(
                {"tag": "kExpression"}
            )

            exprNode = next(exprIter, None)

            if exprNode is None:
                continue

            #
            # Expression shall be a constant number
            #
            lvIsConstant = False

            for child in exprNode.children:

                if child.tag == "kNumber":
                    lvIsConstant = True
                    break

            #
            # AF_VLT_FCOV_USE_CONST_OPT violation
            #
            if not lvIsConstant:
                raw_code = optionNode.text

                lvMsg = (
                    "Verilator compatibility: "
                    "FCOV: option.at_least and option.auto_bin_max "
                    "shall be assigned constant integer values.\n"
                )
                message = self.formatViolationMessage(
                        description=lvMsg,
                        code_snippet=raw_code,
                        fix_suggestion="Replace the value with a constant."
                        )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

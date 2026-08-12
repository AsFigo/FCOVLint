# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVNoHierCrossRule(AsFigoLintRule):
    """
    AF_VLT_FCOV_006 :
    Cross coverage shall not use hierarchical references.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_VLT_FCOV_006"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):

        #
        # Search all cross coverage declarations
        #
        for crossNode in data.tree.iter_find_all({"tag": "kCoverCross"}):

            #
            # Check every cross item
            #
            for refNode in crossNode.iter_find_all({"tag": "kReference"}):

                #
                # Hierarchical reference found
                #
                hierNode = next(
                    refNode.iter_find_all(
                        {"tag": "kHierarchyExtension"}
                    ),
                    None,
                )

                if hierNode is None:
                    continue

                message = (
                    "Verilator compatibility: "
                    "FCOV: Cross coverage shall not use "
                    "hierarchical references.\n"
                    f"{crossNode.text}\n"
                )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

                #
                # Report only one violation per cross
                #
                break

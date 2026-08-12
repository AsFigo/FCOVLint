# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVCrossCptRuleVlt(AsFigoLintRule):
    """
    AF_FCOV_CROSS_CPT_VLT:
    Every item in a cross statement shall be an explicitly
    declared coverpoint name. Raw variable references are
    unsupported by Verilator and may cause the cross to be ignored.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_CROSS_CPT_VLT"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):

        #
        # Iterate over every covergroup
        #
        for cgNode in data.tree.iter_find_all({"tag": "kCovergroupDeclaration"}):

            #
            # Collect declared coverpoint names
            #
            lvCoverpoints = set()

            for cpNode in cgNode.iter_find_all({"tag": "kCoverPoint"}):

                cpNameIter = cpNode.iter_find_all({"tag": "kUnqualifiedId"})
                cpNameNode = next(cpNameIter, None)

                if cpNameNode is not None:
                    lvCoverpoints.add(cpNameNode.text.strip())

            #
            # Check every cross
            #
            for crossNode in cgNode.iter_find_all({"tag": "kCoverCross"}):

                lvCrossCode = crossNode.text

                lvInvalidItem = None

                for refNode in crossNode.iter_find_all({"tag": "kReference"}):

                    refNameIter = refNode.iter_find_all({"tag": "kUnqualifiedId"})
                    refNameNode = next(refNameIter, None)

                    if refNameNode is None:
                        continue

                    lvRefName = refNameNode.text.strip()

                    if lvRefName not in lvCoverpoints:
                        lvInvalidItem = lvRefName
                        break

                #
                # One violation per cross
                #
                if lvInvalidItem is not None:

                    message = (
                        "Verilator compatibility: "
                        "FCOV: Every item in a cross statement shall be an "
                        "explicitly declared coverpoint.\n"
                        f"Found raw variable '{lvInvalidItem}' in cross.\n"
                        f"{lvCrossCode}\n"
                    )

                    self.linter.logViolation(
                        self.ruleID,
                        message,
                    )

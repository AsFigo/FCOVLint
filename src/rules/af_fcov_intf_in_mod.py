# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVInterfaceInModuleRule(AsFigoLintRule):
    """
    AF_VLT_INTF_IN_MOD:
    Interface declarations shall not be nested inside module declarations.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_VLT_INTF_IN_MOD"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        # Search all module declarations
        for modNode in data.tree.iter_find_all({"tag": "kModuleDeclaration"}):

            # Check for nested interface declarations inside module items
            intfNodes = modNode.iter_find_all({"tag": "kInterfaceDeclaration"})

            for intfNode in intfNodes:
                raw_code = intfNode.text

                message = self.formatViolationMessage(
                    description="Interface declarations are not supported inside module blocks.",
                    code_snippet=raw_code,
                    fix_suggestion="Move the interface definition outside the module into global or package scope."
                    )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                    )

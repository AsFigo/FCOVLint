# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging


class FCOVEndlabelStyle(AsFigoLintRule):
    """
    AF_FCOV_STYLE_ENDLABEL:
    Covergroups shall include an explicit endlabel following 'endgroup' (e.g., endgroup : cg_name;).
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_STYLE_ENDLABEL"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        # 1. Iterate over every kCovergroupDeclaration node
        for cgNode in data.tree.iter_find_all({"tag": "kCovergroupDeclaration"}):

            # 2. Extract cg_name from child 1 (SymbolIdentifier) of kCovergroupHeader (child 0)
            cg_name = "covergroup"
            if cgNode.children and len(cgNode.children) > 0:
                cg_header = cgNode.children[0]
                if (
                    cg_header 
                    and getattr(cg_header, "tag", None) == "kCovergroupHeader"
                    and len(cg_header.children) > 1
                ):
                    name_node = cg_header.children[1]
                    if name_node and hasattr(name_node, "text"):
                        cg_name = name_node.text.strip()

            # 3. Check direct children of kCovergroupDeclaration for a kLabel node
            has_endlabel = any(
                child is not None and getattr(child, "tag", None) == "kLabel"
                for child in cgNode.children
            )

            # 4. Flag violation if kLabel is missing
            if not has_endlabel:
                message = self.formatViolationMessage(
                    description=f"Covergroup '{cg_name}' is missing an explicit endlabel.",
                    code_snippet=cgNode.text,
                    fix_suggestion=f"Add ': {cg_name}' after 'endgroup' (e.g., 'endgroup : {cg_name}').",
                )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

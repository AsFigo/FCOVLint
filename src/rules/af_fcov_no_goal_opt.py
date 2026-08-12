# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class FcovNoGoalInCode(AsFigoLintRule):
    """
    AF_FCOV_FUNC_NO_GOAL_IN_CODE:
    Disallows setting 'option.goal' in SystemVerilog source code.
    Coverage goals and targets should be managed via vPlan/HVP or coverage
    reporting tools, not hardcoded inside covergroups, coverpoints, or crosses.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_FUNC_NO_GOAL_IN_CODE"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        for cgNode in data.tree.iter_find_all({"tag": "kCovergroupDeclaration"}):
            if not cgNode.children:
                continue

            # Extract covergroup identifier name for clear messaging
            cg_header = cgNode.children[0]
            cg_name = "covergroup"
            if cg_header and getattr(cg_header, "tag", None) == "kCovergroupHeader":
                if len(cg_header.children) > 1 and cg_header.children[1]:
                    name_node = cg_header.children[1]
                    if hasattr(name_node, "text"):
                        cg_name = name_node.text.strip()

            # Find any kCoverageOption node specifying option.goal
            for opt_node in cgNode.iter_find_all({"tag": "kCoverageOption"}):
                opt_text = opt_node.text.replace(" ", "")
                if "option.goal" in opt_text:
                    message = self.formatViolationMessage(
                        description=f"Covergroup '{cg_name}' sets 'option.goal' in source code.",
                        code_snippet=opt_node.text,
                        fix_suggestion=f"Remove 'option.goal' from 'covergroup {cg_name}'. Manage coverage goals externally via vPlan/HVP or report generation tools.",
                    )

                    self.linter.logViolation(
                        self.ruleID,
                        message,
                    )

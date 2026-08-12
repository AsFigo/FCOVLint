# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class FcovRequirePerInstance(AsFigoLintRule):
    """
    AF_FCOV_REQUIRE_PER_INSTANCE:
    Enforces that covergroups define 'option.per_instance = 1;'
    to ensure individual instance coverage collection in reusable components.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_REQUIRE_PER_INSTANCE"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        for cgNode in data.tree.iter_find_all({"tag": "kCovergroupDeclaration"}):
            if not cgNode.children:
                continue

            # Extract covergroup name from header
            cg_header = cgNode.children[0]
            cg_name = "covergroup"
            if cg_header and getattr(cg_header, "tag", None) == "kCovergroupHeader":
                if len(cg_header.children) > 1 and cg_header.children[1]:
                    name_node = cg_header.children[1]
                    if hasattr(name_node, "text"):
                        cg_name = name_node.text.strip()

            # Check for option.per_instance inside kCoverageSpecOptionList
            has_per_instance = False
            for child in cgNode.children:
                if child and getattr(child, "tag", None) == "kCoverageSpecOptionList":
                    for opt_node in child.iter_find_all({"tag": "kCoverageOption"}):
                        opt_text = opt_node.text.replace(" ", "")
                        if "option.per_instance" in opt_text:
                            has_per_instance = True
                            break
                if has_per_instance:
                    break

            if not has_per_instance:
                message = self.formatViolationMessage(
                    description=f"Covergroup '{cg_name}' does not specify 'option.per_instance = 1;'.",
                    code_snippet=cg_header.text if cg_header else f"covergroup {cg_name}",
                    fix_suggestion=f"Add 'option.per_instance = 1;' inside covergroup '{cg_name}'.",
                )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

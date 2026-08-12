# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class FcovNoMergeInstances(AsFigoLintRule):
    """
    AF_FCOV_FUNC_NO_MERGE_INST:
    Disallows setting 'type_option.merge_instances = 1'.
    Merging coverage across covergroup instances can mask coverage holes
    in individual instances and create a false impression of coverage completeness.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_FUNC_NO_MERGE_INST"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        for cgNode in data.tree.iter_find_all({"tag": "kCovergroupDeclaration"}):
            if not cgNode.children:
                continue

            # Extract covergroup identifier name
            cg_header = cgNode.children[0]
            cg_name = "covergroup"
            if cg_header and getattr(cg_header, "tag", None) == "kCovergroupHeader":
                if len(cg_header.children) > 1 and cg_header.children[1]:
                    name_node = cg_header.children[1]
                    if hasattr(name_node, "text"):
                        cg_name = name_node.text.strip()

            # Inspect kCoverageSpecOptionList for type_option.merge_instances
            for opt_node in cgNode.iter_find_all({"tag": "kCoverageOption"}):
                opt_text = opt_node.text.replace(" ", "")
                if "type_option.merge_instances" in opt_text:
                    message = self.formatViolationMessage(
                        description=f"Covergroup '{cg_name}' enables 'type_option.merge_instances', which can mask coverage holes across individual instances.",
                        code_snippet=opt_node.text,
                        fix_suggestion=f"Remove 'type_option.merge_instances' from covergroup '{cg_name}' to maintain instance-level visibility.",
                    )

                    self.linter.logViolation(
                        self.ruleID,
                        message,
                    )

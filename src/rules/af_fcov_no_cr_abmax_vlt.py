# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class FcovNoCrAbinMaxVlt(AsFigoLintRule):
    """
    AF_FCOV_NO_CR_ABIN_MAX_VLT:
    Flags the use of 'option.cross_auto_bin_max' in cross coverage declarations.
    This option is unsupported in Verilator and will lead to compilation or coverage generation errors.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_NO_CR_ABIN_MAX_VLT"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        for crossNode in data.tree.iter_find_all({"tag": "kCoverCross"}):
            if not crossNode.children:
                continue

            # Extract cross name if present (e.g., "x_ab : cross ...")
            cross_name = "cross"
            first_child = crossNode.children[0]
            if first_child and getattr(first_child, "tag", None) == "kDataTypeImplicitBasicId":
                if hasattr(first_child, "text"):
                    cross_name = first_child.text.strip()

            # Find any kCoverageOption containing option.cross_auto_bin_max
            for opt_node in crossNode.iter_find_all({"tag": "kCoverageOption"}):
                opt_text = opt_node.text.replace(" ", "")
                if "option.cross_auto_bin_max" in opt_text:
                    message = self.formatViolationMessage(
                        description=f"Cross coverage '{cross_name}' uses 'option.cross_auto_bin_max', which is unsupported by Verilator.",
                        code_snippet=opt_node.text,
                        fix_suggestion=f"Remove 'option.cross_auto_bin_max' from cross '{cross_name}' for Verilator compatibility.",
                    )

                    self.linter.logViolation(
                        self.ruleID,
                        message,
                    )

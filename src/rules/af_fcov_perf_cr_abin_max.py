# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class FcovPerfUseCrAbinMax(AsFigoLintRule):
    """
    AF_FCOV_PERF_USE_CR_ABIN_MAX:
    Enforces that all 'cross' coverage specifications define 'option.cross_auto_bin_max'
    to prevent combinatorial explosion of cross bins and high memory utilization.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_PERF_USE_CR_ABIN_MAX"

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

            # Inspect kBraceGroup -> kCrossBodyItemList -> kCoverageOption
            has_cross_auto_bin_max = False
            for opt_node in crossNode.iter_find_all({"tag": "kCoverageOption"}):
                opt_text = opt_node.text.replace(" ", "")
                if "option.cross_auto_bin_max" in opt_text:
                    has_cross_auto_bin_max = True
                    break

            if not has_cross_auto_bin_max:
                message = self.formatViolationMessage(
                    description=f"Cross coverage '{cross_name}' does not specify 'option.cross_auto_bin_max'.",
                    code_snippet=crossNode.text,
                    fix_suggestion=f"Add 'option.cross_auto_bin_max = <limit>;' inside cross '{cross_name}' to limit cross bin growth.",
                )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

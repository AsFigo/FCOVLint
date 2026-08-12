# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class FcovPerfNoImplSamp(AsFigoLintRule):
    """
    AF_FCOV_PERF_NO_IMPL_SAMP:
    Disallows implicit (event-triggered) sampling in covergroups (e.g., @(posedge clk)).
    Implicit sampling runs on every clock edge, degrading simulation performance.
    Coverage should be sampled explicitly using .sample() when transactions occur.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_PERF_NO_IMPL_SAMP"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        for cgNode in data.tree.iter_find_all({"tag": "kCovergroupDeclaration"}):
            if not cgNode.children:
                continue

            cg_header = cgNode.children[0]
            if not cg_header or getattr(cg_header, "tag", None) != "kCovergroupHeader":
                continue

            # Extract covergroup identifier name
            cg_name = "covergroup"
            if len(cg_header.children) > 1 and cg_header.children[1]:
                name_node = cg_header.children[1]
                if hasattr(name_node, "text"):
                    cg_name = name_node.text.strip()

            # Check for kEventControl node in kCovergroupHeader
            has_implicit_sampling = any(
                child is not None and getattr(child, "tag", None) == "kEventControl"
                for child in cg_header.children
            )

            if has_implicit_sampling:
                message = self.formatViolationMessage(
                    description=f"Covergroup '{cg_name}' uses implicit event-triggered sampling.",
                    code_snippet=cg_header.text,
                    fix_suggestion=f"Remove the event control '@(...)' from 'covergroup {cg_name}' and sample explicitly using .sample().",
                )

                self.linter.logViolation(
                    self.ruleID,
                    message,
                )

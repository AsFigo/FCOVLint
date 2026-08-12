# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class FcovPerfNoEdgeImplSamp(AsFigoLintRule):
    """
    AF_FCOV_PERF_NO_EDGE_IMPL_SAMP:
    Disallows clock-based/edge-based implicit sampling in covergroups (e.g., @(posedge clk) or @(negedge clk)).
    Non-edge event sampling (e.g., @(my_trans_event)) is permitted.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_FCOV_PERF_NO_EDGE_IMPL_SAMP"

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

            # Find kEventControl node in header
            event_control_node = next(
                (
                    child
                    for child in cg_header.children
                    if child is not None
                    and getattr(child, "tag", None) == "kEventControl"
                ),
                None,
            )

            if event_control_node:
                event_text = event_control_node.text.lower()
                # Flag only if sampled on posedge or negedge clock/signal edges
                if "posedge" in event_text or "negedge" in event_text:
                    message = self.formatViolationMessage(
                        description=f"Covergroup '{cg_name}' uses clock-edge-style implicit sampling ('{event_control_node.text.strip()}').",
                        code_snippet=cg_header.text,
                        fix_suggestion=f"Remove posedge/negedge from 'covergroup {cg_name}'. Use transaction-based event sampling or explicit .sample().",
                    )

                    self.linter.logViolation(
                        self.ruleID,
                        message,
                    )

# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class _FCovRepetitionHelper:
    """
    MIXIN HELPER: Shared AST logic for covergroup repetition operators.
    This class is NOT a lint rule and is ignored by linter auto-discovery.
    """

    def checkRepetitionTag(self, data, target_tag: str):
        """
        Generic traversal to detect specific repetition operator AST tags:
        - kConsecutiveRepetition ([*])
        - kNonconsecutiveRepetition ([=])
        - kGotoRepetition ([->])
        """
        for binNode in data.tree.iter_find_all({"tag": "kCoverageBin"}):
            for repExpr in binNode.iter_find_all({"tag": "kSequenceRepetitionExpression"}):
                has_tag = any(
                    getattr(node, "tag", None) == target_tag
                    for node in repExpr.descendants
                )
                if has_tag:
                    code_snippet = binNode.text.strip()
                    message = f"{self.lvMsg}\nCode snippet:\n  {code_snippet}\n"
                    self.linter.logViolation(self.ruleID, message)


# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
from rules.af_fcov_rept_helper import _FCovRepetitionHelper


class FCovCnsqRptVlt(AsFigoLintRule, _FCovRepetitionHelper):
    lvMsg = """[AF_VLT_FCOV_CNSQ_RPT]: Consecutive repetition '[*]' detected in covergroup bin.
Tool Limit: Verilator throws '%Warning-COVERIGN' for consecutive repetitions in coverage bins.
Functional Impact: Bin is ignored during compilation, leaving contiguous state transitions unmonitored.
Recommendation: Replace (sig [*2]) with explicit transitions like (sig => sig)."""

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_VLT_FCOV_CNSQ_RPT"

    def apply(self, filePath: str, data: AsFigoLintRule.VeribleSyntax.SyntaxData):
        self.checkRepetitionTag(data, "kConsecutiveRepetition")


class FCovNCsqRptVlt(AsFigoLintRule, _FCovRepetitionHelper):
    lvMsg = """[AF_VLT_FCOV_NCSQ_RPT]: Non-consecutive repetition '[=]' detected in covergroup bin.
Tool Limit: Verilator throws '%Warning-COVERIGN' for non-consecutive repetitions in coverage bins.
Functional Impact: Bin is ignored during compilation, resulting in silent coverage loss for sparse events.
Recommendation: Reframe the coverage model using explicit transition sequences."""

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_VLT_FCOV_NCSQ_RPT"

    def apply(self, filePath: str, data: AsFigoLintRule.VeribleSyntax.SyntaxData):
        self.checkRepetitionTag(data, "kNonconsecutiveRepetition")


class FCovGotoRptVlt(AsFigoLintRule, _FCovRepetitionHelper):
    lvMsg = """[AF_VLT_FCOV_GOTO_RPT]: Goto repetition '[->]' detected in covergroup bin.
Tool Limit: Verilator throws '%Warning-COVERIGN' for goto repetitions in coverage bins.
Functional Impact: Bin is ignored during compilation, failing to track target reachability across delays.
Recommendation: Restructure using explicit single-step transitions."""

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_VLT_FCOV_GOTO_RPT"

    def apply(self, filePath: str, data: AsFigoLintRule.VeribleSyntax.SyntaxData):
        self.checkRepetitionTag(data, "kGotoRepetition")

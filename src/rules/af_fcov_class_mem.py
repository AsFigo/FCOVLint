# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule
import logging
import anytree


class FCOVClMemVlt(AsFigoLintRule):
    """
    AF_VLT_FCOV_CLASS_MEMBER_REF:
    Coverpoints shall not directly reference member variables of the enclosing class.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "AF_VLT_FCOV_CLASS_MEMBER_REF"

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        # 1. Find all class declarations
        for classNode in data.tree.iter_find_all({"tag": "kClassDeclaration"}):

            # 2. Extract all member variable names declared directly inside the class
            class_members = set()
            classItems = next(
                classNode.iter_find_all({"tag": "kClassItems"}),
                None,
            )
            if not classItems:
                continue

            for dataDecl in classItems.iter_find_all({"tag": "kDataDeclaration"}):
                for varAssign in dataDecl.iter_find_all({"tag": "kVariableDeclarationAssignment"}):
                    # Find the variable identifier
                    for child in varAssign.children:
                        if hasattr(child, "tag") and child.tag == "SymbolIdentifier":
                            class_members.add(child.text.strip())
                        elif hasattr(child, "symbol") and child.symbol == "SymbolIdentifier":
                            class_members.add(child.text.strip())

            if not class_members:
                continue

            # 3. Find covergroups declared inside this class
            for cgNode in classItems.iter_find_all({"tag": "kCovergroupDeclaration"}):
                for cpNode in cgNode.iter_find_all({"tag": "kCoverPoint"}):
                    
                    # 4. Extract target expression referenced by coverpoint
                    exprNode = next(
                        cpNode.iter_find_all({"tag": "kExpression"}),
                        None,
                    )
                    if not exprNode:
                        continue

                    # Find unqualified identifier in the coverpoint target
                    unqualId = next(
                        exprNode.iter_find_all({"tag": "kUnqualifiedId"}),
                        None,
                    )
                    if not unqualId:
                        continue

                    target_var = unqualId.text.strip()

                    # 5. Check if the coverpoint targets a class member variable
                    if target_var in class_members:
                        raw_code = cpNode.text

                        message = self.formatViolationMessage(
                            description=f"Coverpoint references enclosing class member '{target_var}' directly.",
                            code_snippet=raw_code,
                            fix_suggestion=(
                                "Pass the variable as an argument to the covergroup, "
                                "or sample a non-class member in outer scope."
                            )
                        )

                        self.linter.logViolation(
                            self.ruleID,
                            message,
                        )

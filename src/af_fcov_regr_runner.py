# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

import glob
import os
import sys
import unittest

# Resolve absolute paths to repository directories
srcDir = os.path.dirname(os.path.abspath(__file__))
repoRootDir = os.path.abspath(os.path.join(srcDir, ".."))
binDir = os.path.join(repoRootDir, "bin")
testsDir = os.path.join(repoRootDir, "tests")

# Add 'bin' and 'src' to Python import path dynamically
if binDir not in sys.path:
    sys.path.append(binDir)
if srcDir not in sys.path:
    sys.path.append(srcDir)

from fcovlint import FCOVLinter


class TestFCOVLintRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Instantiate linter once for all test runs."""
        # Check tests/ first, then fall back to repository root
        configPath = os.path.join(testsDir, "config.toml")
        if not os.path.exists(configPath):
            configPath = os.path.join(repoRootDir, "config.toml")

        cls.linter = FCOVLinter(configFile=configPath)
        cls.testDir = testsDir

    def testPassCases(self):
        """Files ending with '_p.sv' in tests/ must produce 0 errors."""
        passFiles = [
            f for f in glob.glob(os.path.join(self.testDir, "*_p.sv"))
            if os.path.isfile(f)
        ]

        if not passFiles:
            self.skipTest("No pass test files (*_p.sv) found in tests directory.")

        for filePath in passFiles:
            fileName = os.path.basename(filePath)
            with self.subTest(file=fileName):
                self.linter.resetFileState(filePath)
                self.linter.runOnSingleFile(filePath)

                self.assertEqual(
                    self.linter.errorCount,
                    0,
                    f"Expected 0 errors for {fileName}, but found {self.linter.errorCount}: {self.linter.errorList}",
                )

    def testFailCases(self):
        """Files ending with '_f.sv' in tests/ must trigger at least 1 error."""
        failFiles = [
            f for f in glob.glob(os.path.join(self.testDir, "*_f.sv"))
            if os.path.isfile(f)
        ]

        if not failFiles:
            self.skipTest("No fail test files (*_f.sv) found in tests directory.")

        for filePath in failFiles:
            fileName = os.path.basename(filePath)
            with self.subTest(file=fileName):
                self.linter.resetFileState(filePath)
                self.linter.runOnSingleFile(filePath)

                self.assertGreater(
                    self.linter.errorCount,
                    0,
                    f"Expected lint violations for {fileName}, but 0 were reported.",
                )


if __name__ == "__main__":
    logPath = os.path.join(os.getcwd(), "regression_summary.log")
    
    # Open file and direct the test runner output to it
    with open(logPath, "w") as logFile:
        runner = unittest.TextTestRunner(stream=logFile, verbosity=2)
        
        # exit=False ensures the file closes properly before the script ends
        unittest.main(testRunner=runner, exit=False)
        
    print(f"Regression complete. Log saved to: {logPath}")    


# FCOVLint
Lightweight, open-source SystemVerilog linter for functional coverage (FCOV) rules, designed for custom BYOL (Build Your Own Linter) integration.
**Short Description (GitHub Repo Description)**

`FCOVLint` is an open-source, extensible SystemVerilog linter focused specifically on functional coverage constructs (`covergroup`, `coverpoint`, `cross`, and coverage options) and simulator compatibility. Built for flexible BYOL (Build Your Own Linter) integration, it enforces coverage coding standards and validates Verilator functional coverage compatibility across SystemVerilog testbenches and RTL.

* **Verilator FCOV Compatibility:** Catches unsupported or problematic coverage constructs before passing code to Verilator.
* **Targeted Coverage Linting:** Focuses strictly on functional coverage structure, options, and naming conventions.
* **Extensible (BYOL):** Lightweight, modular architecture for writing and plugging in custom lint rules.
* **Pipeline-Ready:** Easy integration into open-source EDA toolchains and CI/CD pipelines.

// FCOV-004	option.at_least and option.auto_bin_max must be set to constant values. Non-constant expressions are ignored and silently replaced with tool defaults — coverage results may not reflect your intended thresholds.

module fcov004_bad;

  logic [1:0] a;
  int threshold = 10;

  covergroup cg;

    option.per_instance = 1;

    // VIOLATION: 'threshold' is a variable, not a constant value.
    option.at_least = threshold;

    // VIOLATION: expression uses a variable instead of a constant value.
    option.auto_bin_max = threshold + 5;

    cp_a : coverpoint a;

  endgroup : cg

  cg cg_inst = new();

endmodule

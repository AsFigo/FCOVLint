// FCOV-004	option.at_least and option.auto_bin_max must be set to constant values. Non-constant expressions are ignored and silently replaced with tool defaults — coverage results may not reflect your intended thresholds.

module fcov004_good;

  logic [1:0] a;

  covergroup cg;

    option.per_instance = 1;

    // PASS: option.at_least is assigned a constant value.
    option.at_least = 10;

    // PASS: option.auto_bin_max is assigned a constant value.
    option.auto_bin_max = 64;

    cp_a : coverpoint a;

  endgroup : cg

  cg cg_inst = new();

endmodule

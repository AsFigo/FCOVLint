// FCOV-006	Cross coverage must not use a hierarchical reference (e.g. cross a.b) as an implicit coverpoint. Such crosses are unsupported and ignored.

module fcov006_p;

  logic [1:0] a;
  logic [1:0] b;

  covergroup cg;

    option.per_instance = 1;

    cp_a : coverpoint a;
    cp_b : coverpoint b;

    x_ab : cross cp_a, cp_b;

  endgroup : cg

  cg cg_inst = new();

endmodule

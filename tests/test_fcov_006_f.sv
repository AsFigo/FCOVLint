// FCOV-006: Cross coverage must not use a hierarchical reference.

module child;

  logic [1:0] sig;

endmodule


module fcov006_f;

  logic [1:0] a;

  child u_child();

  covergroup cg;

    option.per_instance = 1;

    cp_a : coverpoint a;

    // VIOLATION: hierarchical reference in cross
    x_ab : cross cp_a, u_child.sig;

  endgroup : cg

  cg cg_inst = new();

endmodule

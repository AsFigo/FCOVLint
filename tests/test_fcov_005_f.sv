module fcov005_f;

  bit [15:0] a;

  covergroup cg;

    option.per_instance = 1;

    cp_a : coverpoint a {
      // VIOLATION: Very large array bin expansion
      bins b[] = {[0:65535]};
    }

  endgroup : cg

  cg cg_inst = new();

endmodule

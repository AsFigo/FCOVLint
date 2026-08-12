module fcov005_p;

  bit [15:0] a;

  covergroup cg;

    option.per_instance = 1;

    cp_a : coverpoint a {
      bins b[] = {[0:15]};
    }

  endgroup : cg

  cg cg_inst = new();

endmodule

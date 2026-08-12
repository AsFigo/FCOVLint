module fcov002_pass;

int data;

covergroup cg;

  option.per_instance = 1;

  cp : coverpoint data;

endgroup : cg

cg cg_inst = new();

endmodule

module fcov003_pass;

int value;

covergroup cg;

  cp : coverpoint value;

endgroup

cg c = new();

endmodule

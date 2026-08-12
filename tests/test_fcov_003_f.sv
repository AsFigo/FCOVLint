module fcov003_fail;

class item;

  int data;

endclass

item h = new();

covergroup cg;

  // VIOLATION:
  // Dereferencing class handle member
  cp : coverpoint h.data;

endgroup

cg c = new();

endmodule

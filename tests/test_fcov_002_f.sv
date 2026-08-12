module fcov002_fail;

class env;

  int data;

  covergroup cg;

    option.per_instance = 1;

    // VIOLATION:
    // Direct reference to enclosing class member.
    cp : coverpoint data;

  endgroup : cg

  function new();
    cg = new();
  endfunction

endclass

env e = new();

endmodule

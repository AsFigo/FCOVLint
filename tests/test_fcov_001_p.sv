module fcov001_pass;

bit clk = 0;
bit [3:0] addr;

always #5 clk = ~clk;

class packet;

  covergroup cg;

    option.per_instance = 1;

    cp_addr : coverpoint addr;
  endgroup : cg

  function new();
    cg = new();
  endfunction

endclass

packet pkt = new();

endmodule

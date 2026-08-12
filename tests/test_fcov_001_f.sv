module fcov001_fail;

bit [3:0] addr;

class packet;

  bit clk;

  covergroup cg @(posedge clk);

    option.per_instance = 1;

    cp_addr : coverpoint addr;
  endgroup : cg

  function new();
    cg = new();
  endfunction

endclass

packet pkt = new();

endmodule

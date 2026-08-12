module fcov007_good;

  logic [1:0] addr;
  logic [1:0] data;

  covergroup cg;
         option.per_instance = 1; 
    cp_addr : coverpoint addr;
    cp_data : coverpoint data;

    // PASS: Every cross item is an explicitly declared coverpoint.
    cross_addr_data : cross cp_addr, cp_data;

  endgroup : cg

  cg cg_inst = new();

endmodule

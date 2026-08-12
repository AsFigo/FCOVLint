module fcov007_bad;

  logic [1:0] addr;
  logic [1:0] data;

  covergroup cg;
          option.per_instance = 1;
    cp_addr : coverpoint addr;

    // VIOLATION: 'data' is referenced directly in the cross
    // instead of using a declared coverpoint.
    cross_addr_data : cross cp_addr, data;

  endgroup :cg

  cg cg_inst = new();

endmodule

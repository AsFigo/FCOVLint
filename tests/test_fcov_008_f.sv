module fcov008_bad;

  logic [2:0] state;

  covergroup cg;
	  option.per_instance = 1;

    cp_state : coverpoint state {

      // VIOLATION: Multi-value transition bin.
      bins state_trans = (1,2,3 => 4,5);

    }

  endgroup :cg 

  cg cg_inst = new();

endmodule

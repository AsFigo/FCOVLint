module fcov008_good;

  logic [2:0] state;

  covergroup cg;
	  option.per_instance = 1;

    cp_state : coverpoint state {

      // PASS: Simple transition bin with a single source
      // and destination value.
      bins state_trans = (3 => 4);

    }

  endgroup : cg

  cg cg_inst = new();

endmodule

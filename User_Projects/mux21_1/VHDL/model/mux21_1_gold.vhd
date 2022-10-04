-- Header Section
-- Component Name : mux21_1
-- Title          : 2-to-1 mux, 1-bit data

-- Description    
-- sel is datapath control signal
-- muxOut = muxIn0 when sel  = 0
-- muxOut = muxIn1 when sel  = 1  

-- Author(s)      : Fearghal Morgan
-- Company        : National University of Ireland, Galway 
-- Email          : fearghal.morgan@nuigalway.ie
-- Date           : 14/08/2022

-- entity signal dictionary
-- sel 		datapath control signal
-- muxIn1	datapath 1 input signal
-- muxIn0	datapath 0 input signal
-- muxut	data out signal

-- internal signal dictionary
-- None

-- library declarations 
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- entity declaration
entity mux21_1
Port(
	sel : in std_logic;
	muxIn1 : in std_logic;
	muxIn0 : in std_logic;
	muxOut : out std_logic
    );
end entity mux21_1;

architecture combinational of mux21_1 is
-- Internal signal declarations

-- Component declarations

begin

muxOut_p: process(sel, muxIn1, muxIn0)
begin
    -- Complete the process
	muxOut <= muxIn1;
end process;

end combinational;
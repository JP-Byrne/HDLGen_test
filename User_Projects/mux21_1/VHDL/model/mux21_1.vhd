-- Header Section
-- Component Name : mux21_1
-- Title          : 2-to-1 mux, 1-bit data
-- Description    : signal sel is datapath control signal
 	--muxOut = muxIn0 when sel  = 0
 	--muxOut = muxIn1 when sel  = 1 
-- Author(s)      : Fearghal Morgan
-- Company        : National University of Ireland, Galway
-- Email          : fearghal.morgan@nuigalway.ie
-- Date           : 16/08/2022


-- Library Section
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity Section
entity mux21_1 is 
Port(
	sel : in std_logic;
	muxIn1 : in std_logic;
	muxIn0 : in std_logic;
	muxOut : out std_logic
);
end entity mux21_1;

architecture combinational of mux21_1 is

-- Internal Signals


begin

muxOut_p: process(sel,muxIn1,muxIn0)
begin
	muxOut <= muxIn0;

	-- Complete the process

end process;

end combinational;
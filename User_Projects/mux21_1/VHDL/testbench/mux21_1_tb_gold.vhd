-- Header Section
-- VHDL testbench mux21_1_TB
-- Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen

-- Component Name : mux21_1
-- Title          : 2-to-1 mux, 1-bit data
-- Description    : Refer to component hdl model for function description and signal dictionary 
-- Author(s)      : Fearghal Morgan

-- Company        : National University of Ireland, Galway 
-- Email          : fearghal.morgan@nuigalway.ie
-- Date           : 14/08/2022

-- library declarations 
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- entity declaration
entity mux21_1_TB is end mux21_1_TB; -- testbench has no inputs or outputs

architecture behave of mux21_1_TB is

-- unit under test (UUT) component declaration. Identical to component entity, with 'entity' replaced with 'component' 
component mux21_1 is
Port(
	sel : in std_logic;
	muxIn1 : in std_logic;
	muxIn0 : in std_logic;
	muxOut : out std_logic
	);
end component;

-- testbench signal declarations
-- Typically use the same signal names as in the VHDL entity, with keyword signal added, and without in/out mode keyword
-- excluding clk and rst, if used
signal sel    : std_logic;
signal muxIn1 : std_logic;
signal muxIn0 : std_logic;
signal muxOut : std_logic;

-- <delete (Start) If UUT is a combinational component>
signal clk: std_logic := '1'; -- entity includes signal clk, so declare (and initialise) tetbench clk signal 
signal rst: std_logic;        -- entity may include signal rst (reset), so declare in testbench 
-- <delete (End) 

-- testbench control signal declarations
signal endOfSim : boolean := false; -- assert at end of simulation to highlight simuation done. Stops clk signal generation.
signal testNo: integer; -- aids locating test in simulation waveform

constant period: time := 20 ns; -- Default simulation time. Use as simulation delay constant, or clk period if sequential model ((50MHz clk here)

begin

-- <delete (Start) If UUT is a combinational component>
-- Generate clk signal, if sequential component, and endOfSim is FALSE.
clkStim: clk <= not clk after period/2 when endOfSim = false else '0';  
-- <delete (End) 


-- instantiate unit under test (UUT)
UUT: mux21_1 -- map component internal sigs => testbench signals
port map 
  (sel    => sel,   
  muxIn1 => muxIn1,
  muxIn0 => muxIn0,
  muxOut => muxOut
  );

-- Signal stimulus process
stim_p: process -- process sensitivity list is empty, so process automatically executes at start of simulation. Suspend process at the wait; statement 
-- <delete (Start) if note using variables
variable stimVec : std_logic_vector(2 downto 0);
-- <delete (End) 

begin 
  -- Apply default INPUT signal values. Do not assign output signals (generated by the UUT) in this stim_p process
  -- Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge
  -- if signal type is 
  --   std_logic, use '0'
  --   std_logic_vector use (others => '0')
  --   integer use 0
  sel    <= '0';
  muxIn1 <= '0';
  muxIn0 <= '0';

  report "%N Simulation start";

  -- <delete (Start) If UUT is a combinational component>
  report "Assert and toggle rst"; 
  testNo <= 0;
  rst    <= '1';   
  wait for period*1.2; -- assert rst for 1.2*period, deasserting rst 0.2*period after active clk edge
  rst   <= '0'; 
  wait for period; -- wait 1 clock period
  -- <delete (End) 
  
  -- Include testbench stimulus sequence here. 
  -- Use new testNo for each test set
  -- Generate input signal combinations and 'wait for' 1 or multiple period.
  testNo <= 1;
  wait for period;
    
  -- <delete (Start) if note using variables
  for i in 0 to 7 loop
	stimVec := std_logic_vector( to_unsigned(i,3) );
	sel     <= stimVec(2); 
	muxIn1  <= stimVec(1); 
	muxIn0  <= stimVec(0); 
    wait for period;
  end loop;
  -- <delete (End) 
 
  -- <delete (Start) if not required 
  sel    <= '0';
  muxIn1 <= '0';
  muxIn0 <= '0';
  wait for period;
 -- <delete (End)
   
  report "%N Simulation done";
  endOfSim <= TRUE; -- assert flag to stop clk signal generation
  
  wait; -- wait forever
end process;

end architecture behave;
import os
from xml.dom import minidom
from PySide2.QtWidgets import *
import subprocess
import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager


class Generator(QWidget):

    def __init__(self):
        super().__init__()

        self.entity_name = ""
        self.tcl_path = ""


    def generate_folders(self):

        print("Generating Project folders...")

        # Parsing the xml file
        xml_data_path = ProjectManager.get_xml_data_path()
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        # Accessing the projectManager and genFolder Elements
        project_Manager = HDLGen.getElementsByTagName("projectManager")
        settings = project_Manager[0].getElementsByTagName("settings")[0]
        location = settings.getElementsByTagName("location")[0].firstChild.data
        genFolder_data = HDLGen.getElementsByTagName("genFolder")
        hdl_data = project_Manager[0].getElementsByTagName("HDL")[0]
        hdl_langs = hdl_data.getElementsByTagName("language")

        for hdl_lang in hdl_langs:
            # If vhdl is present in the hdl settings then directory with vhdl_folder tag are read
            if hdl_lang.getElementsByTagName('name')[0].firstChild.data == "VHDL":
                for folder in genFolder_data[0].getElementsByTagName("vhdl_folder"):
                    # Creating the directory
                    path = os.path.join(location, folder.firstChild.data)
                    os.makedirs(path, exist_ok=True)
                    # If verilog is present in the hdl settings then directory with verilog_folder are read
            if hdl_lang.getElementsByTagName('name')[0].firstChild.data == "Verilog":
                for folder in genFolder_data[0].getElementsByTagName("verilog_folder"):
                    # Creating the directory
                    path = os.path.join(location, folder.firstChild.data)
                    os.makedirs(path, exist_ok=True)

        # print("All project folders have been successfully generated at ", self.proj_dir)

    @staticmethod
    def generate_vhdl():

        gen_vhdl = ""

        xml_data_path = ProjectManager.get_xml_data_path()

        test_xml = os.path.join("../Resources", "SampleProject.xml")

        vhdl_database_path = "./Generator/HDL_Database/vhdl_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        vhdl_database = minidom.parse(vhdl_database_path)
        vhdl_root = vhdl_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")

        entity_name = ""
        gen_int_sig = ""
        gen_internal_signal_result = ""
        # Entity Section

        gen_signals = ""
        entity_signal_description = ""
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""

        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:

            for signal in io_port_node[0].getElementsByTagName('signal'):
                signal_declare_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data

                signal_declare_syntax = signal_declare_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                signal_declare_syntax = signal_declare_syntax.replace("$mode",
                                                                      signal.getElementsByTagName('mode')[
                                                                          0].firstChild.data)
                signal_declare_syntax = signal_declare_syntax.replace("$type",
                                                                      signal.getElementsByTagName('type')[
                                                                          0].firstChild.data)
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
                gen_signals += "\t" + signal_declare_syntax + "\n"
            gen_signals = gen_signals.rstrip()
            gen_signals = gen_signals[0:-1]

            entity_syntax = vhdl_root.getElementsByTagName("entity")
            gen_entity = "-- entity declaration\n"
            gen_entity += entity_syntax[0].firstChild.data

            #gen_entity = gen_entity.replace("$comp_name", entity_name)
            gen_entity = gen_entity.replace("$signals", gen_signals)

        #gen_vhdl += gen_entity + "\n\n"
        #gen_vhdl += entity_signal_description + "\n\n"

            # Internal signals
            gen_int_sig = "-- Internal signal declarations"
            int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")
            if int_sig_node[0].firstChild is not None:
                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    int_sig_syntax = vhdl_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_name",
                                                            signal.getElementsByTagName('name')[0].firstChild.data)
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_type",
                                                            signal.getElementsByTagName('type')[0].firstChild.data)
                    int_signal_description = signal.getElementsByTagName('description')[
                        0].firstChild.data

                    gen_int_sig += "\n" + int_sig_syntax
                    gen_internal_signal_result += "-- " + signal.getElementsByTagName('name')[
                                0].firstChild.data + "\t" +int_signal_description + "\n"
                gen_int_sig.rstrip()
            else:
                gen_internal_signal_result = "-- None\n"


        # Header Section

        header_node = hdl_design[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                entity_name = comp_node.firstChild.data

                gen_header = "-- Header Section\n"
                gen_header += "-- Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "-- Title          : " + (title if title != "null" else "")+"\n\n"
                desc = header_node[0].getElementsByTagName("description")[0].firstChild.data
                desc = desc.replace("&#10;", "\n-- ")
                gen_header += "-- Description\n-- "
                gen_header += (desc if desc != "null" else "") + "\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "\n-- Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "-- Company        : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "-- Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "-- Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"

                gen_vhdl += gen_header

                # entity signal dictionary
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                gen_entity_signal = "-- entity signal dictionary\n"
                gen_entity_signal += entity_signal_description+"\n"
                gen_vhdl += gen_entity_signal

                # internal signal dictionary
                gen_internal_signal = "-- internal signal dictionary\n"
                gen_internal_signal_result = gen_internal_signal_result +"\n"
                gen_internal_signal += gen_internal_signal_result
                gen_vhdl += gen_internal_signal
                # Libraries Section

                libraries_node = vhdl_root.getElementsByTagName("libraries")
                libraries = libraries_node[0].getElementsByTagName("library")
                gen_library = "-- library declarations\n"

                for library in libraries:
                    gen_library += library.firstChild.data + "\n"

                gen_library += "\n"
                gen_vhdl += gen_library
                # Entity Section placement
                gen_vhdl += gen_entity + "\n\n"
                # Architecture section

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_process = ""

                if len(arch_node) != 0 and arch_node[0].firstChild is not None:

                    child = arch_node[0].firstChild

                    while child is not None:

                        next = child.nextSibling

                        if (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "process"):

                            process_syntax = vhdl_root.getElementsByTagName("process")[0].firstChild.data

                            process_syntax = process_syntax.replace("$process_label",
                                                                    child.getElementsByTagName("label")[
                                                                        0].firstChild.data)

                            gen_in_sig = ""

                            for input_signal in child.getElementsByTagName("inputSignal"):
                                gen_in_sig += input_signal.firstChild.data + ","

                            gen_in_sig = gen_in_sig[:-1]

                            process_syntax = process_syntax.replace("$input_signals", gen_in_sig)

                            gen_defaults = ""
                            for default_out in child.getElementsByTagName("defaultOutput"):
                                assign_syntax = vhdl_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                                signals = default_out.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                assign_syntax = assign_syntax.replace("$value", signals[1])

                                gen_defaults += "\t" + assign_syntax + "\n"

                            process_syntax = process_syntax.replace("$default_assignments", gen_defaults)
                            gen_process += process_syntax + "\n\n"

                        elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "concurrentStmt"):

                            gen_stmts = ""
                            conc_syntax = vhdl_root.getElementsByTagName("concurrentstmt")[0].firstChild.data

                            conc_syntax = conc_syntax.replace("$concurrentstmt_label",
                                                                    child.getElementsByTagName("label")[
                                                                        0].firstChild.data)

                            for statement in child.getElementsByTagName("statement"):
                                assign_syntax = vhdl_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                                signals = statement.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                assign_syntax = assign_syntax.replace("$value", signals[1])

                                gen_stmts += assign_syntax + "\n"

                            conc_syntax = conc_syntax.replace("$statement", gen_stmts)
                            gen_process += conc_syntax + "\n"

                        child = next

                    arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data
                    arch_name_node = arch_node[0].getElementsByTagName("archName")

                    arch_name = "comb"

                    if len(arch_name_node) != 0 and arch_name_node[0].firstChild is not None:
                        arch_name = arch_name_node[0].firstChild.data

                    gen_arch = arch_syntax.replace("$arch_name", arch_name)
                    gen_arch = gen_arch.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$int_sig_declaration", gen_int_sig)
                    gen_arch = gen_arch.replace("$component_declarations", "-- Component declarations")
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                    gen_vhdl += gen_arch

        return entity_name, gen_vhdl

    def create_vhdl_file(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        entity_name, vhdl_code = self.generate_vhdl()

        vhdl_file_path = os.path.join(proj_path, "VHDL", "model", entity_name + ".vhd")

        print(vhdl_code)

        # Writing xml file
        with open(vhdl_file_path, "w") as f:
            f.write(vhdl_code)

        print("VHDL Model successfully generated at ", vhdl_file_path)

        self.entity_name = entity_name

    def create_tcl_file(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)

        vhdl_path = proj_path + "/VHDL/model/" + self.entity_name + ".vhd"
        self.tcl_path = proj_path + "/VHDL/AMDPrj/" + self.entity_name + ".tcl"
        tcl_database_path = "./Generator/TCL_Database/tcl_database.xml"

        tcl_database = minidom.parse(tcl_database_path)
        tcl_root = tcl_database.documentElement

        tcl_file_template = tcl_root.getElementsByTagName("vivado_vhdl_tcl")[0]
        print(tcl_file_template)
        tcl_file_template = tcl_file_template.firstChild.data
        print(tcl_file_template)

        tb_file_name = self.entity_name + "_tb"
        tcl_vivado_code = tcl_file_template.replace("$tcl_path", self.tcl_path)
        tcl_vivado_code = tcl_vivado_code.replace("$comp_name", self.entity_name)
        tcl_vivado_code = tcl_vivado_code.replace("$tb_name", tb_file_name)
        tcl_vivado_code = tcl_vivado_code.replace("$proj_name", proj_name)
        proj_path = "{" + proj_path + "}"
        tcl_vivado_code = tcl_vivado_code.replace("$proj_dir", proj_path)
        tcl_vivado_code = tcl_vivado_code.replace("$vhdl_path", vhdl_path)

        # Writing xml file
        with open(self.tcl_path, "w") as f:
            f.write(tcl_vivado_code)

        print("TCL file successfully generated at ", self.tcl_path)

        return 1

    def run_tcl_file(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        subprocess.Popen("cd " + proj_path, shell=True)
        vivado_bat_file_path = ProjectManager.get_vivado_bat_path()
        start_vivado_cmd = vivado_bat_file_path + " -source " + self.tcl_path
        subprocess.Popen(start_vivado_cmd, shell=True)

    def create_vhdl_testbench_code(self):
        tb_code = ""

        xml_data_path = ProjectManager.get_xml_data_path()

        test_xml = os.path.join("../Resources", "SampleProject.xml")

        vhdl_tb_database_path = "./Generator/TB_Database/vhdl_tb_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        vhdl_tb_database = minidom.parse(vhdl_tb_database_path)
        vhdl_root = vhdl_tb_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")

        entity_name = ""
        gen_int_sig = ""
        gen_internal_signal_result = ""
        # Entity Section
        inputArray = []
        gen_signals = ""
        io_signals = "-- testbench signal declarations\n"
        io_signals += "-- Typically use the same signal names as in the VHDL entity, with keyword signal added, and without in/out mode keyword\n"
        io_signals += "-- excluding clk and rst, if used\n"
        entity_signal_description = ""
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""
        io_port_map =""
        inputsToZero =""
        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:

            for signal in io_port_node[0].getElementsByTagName('signal'):
                signal_declare_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data
                io_signal_declare_syntax = vhdl_root.getElementsByTagName("IOSignalDeclaration")[0].firstChild.data
                io_port_map_syntax = vhdl_root.getElementsByTagName("portMap")[0].firstChild.data
                signal_declare_syntax = signal_declare_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                io_port_map_syntax = io_port_map_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                signal_declare_syntax = signal_declare_syntax.replace("$mode",
                                                                      signal.getElementsByTagName('mode')[
                                                                          0].firstChild.data)
                signal_declare_syntax = signal_declare_syntax.replace("$type",
                                                                      signal.getElementsByTagName('type')[
                                                                          0].firstChild.data)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$type",
                                                                            signal.getElementsByTagName('type')[
                                                                                0].firstChild.data)
                if signal.getElementsByTagName('mode')[0].firstChild.data == "in":
                    if signal.getElementsByTagName('type')[0].firstChild.data == "std_logic":
                        inputArray.append(signal.getElementsByTagName('name')[0].firstChild.data)
                        inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= \'0\';\n"
                    else:
                        inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= (others => \'0\');\n"
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
                gen_signals += "\t" + signal_declare_syntax + "\n"
                io_port_map += "\t" + io_port_map_syntax + "\n"
                if signal.getElementsByTagName('name')[0].firstChild.data != "clk" and signal.getElementsByTagName('name')[0].firstChild.data != "rst" :
                    io_signals += io_signal_declare_syntax + "\n"
            io_port_map = io_port_map.rstrip()
            io_port_map = io_port_map[0:-1]
            io_signals = io_signals.rstrip()
            #io_signals = io_signals[0:-1]
            other_signals = "\n-- <delete (Start) If UUT is a combinational component>\n"
            other_signals += "signal clk: std_logic := '1'; -- entity includes signal clk, so declare (and initialise) tetbench clk signal\n"
            other_signals += "signal rst: std_logic;        -- entity may include signal rst (reset), so declare in testbench\n"
            other_signals += "-- <delete (End)\n\n-- testbench control signal declarations\n"
            other_signals += "signal endOfSim : boolean := false; -- assert at end of simulation to highlight simuation done. Stops clk signal generation.\n"
            other_signals += "signal testNo: integer; -- aids locating test in simulation waveform\n\n"
            other_signals += "constant period: time := 20 ns; -- Default simulation time. Use as simulation delay constant, or clk period if sequential model ((50MHz clk here)\n"

            gen_signals = gen_signals.rstrip()
            gen_signals = gen_signals[0:-1]

            entity_syntax = vhdl_root.getElementsByTagName("entity")
            gen_entity = "-- entity declaration\n"
            gen_entity += entity_syntax[0].firstChild.data

            # Internal signals
            gen_int_sig = ""
            int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")
            if int_sig_node[0].firstChild is not None:
                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    int_sig_syntax = vhdl_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_name",
                                                            signal.getElementsByTagName('name')[0].firstChild.data)
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_type",
                                                            signal.getElementsByTagName('type')[0].firstChild.data)
                    int_signal_description = signal.getElementsByTagName('description')[
                        0].firstChild.data

                    gen_int_sig += "\n" + int_sig_syntax
                    gen_internal_signal_result += "-- " + signal.getElementsByTagName('name')[
                        0].firstChild.data + "\t" + int_signal_description + "\n"
                gen_int_sig.rstrip()
            else:
                gen_internal_signal_result = "-- None\n"

        # Header Section

        header_node = hdl_design[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                entity_name = comp_node.firstChild.data

                gen_header = "-- Header Section\n"
                gen_header += "-- VHDL testbench "+ entity_name +"_TB\n"
                gen_header += "-- Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen\n"
                gen_header += "-- Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "-- Title          : " + (title if title != "null" else "") + "\n"
                gen_header += "-- Description    : refer to component hdl model fro function description and signal dictionary\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "-- Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "-- Company        : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "-- Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "-- Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"

                tb_code += gen_header

                # entity signal dictionary
                gen_entity_signal = "-- entity signal dictionary\n"
                gen_entity_signal += entity_signal_description + "\n"
                #tb_code += gen_entity_signal

                # internal signal dictionary
                gen_internal_signal = "-- internal signal dictionary\n"
                gen_internal_signal_result = gen_internal_signal_result + "\n"
                gen_internal_signal += gen_internal_signal_result
                #tb_code += gen_internal_signal
                # Libraries Section

                libraries_node = vhdl_root.getElementsByTagName("libraries")
                libraries = libraries_node[0].getElementsByTagName("library")
                gen_library = "-- library declarations\n"

                for library in libraries:
                    gen_library += library.firstChild.data + "\n"

                gen_library += "\n"
                tb_code += gen_library

                # Entity declaration
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                tb_code += gen_entity +"\n\n"
                tbSignalDeclaration = io_signals +"\n" + other_signals
                # Architecture section

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")

                gen_process = "-- <delete (Start) If UUT is a combinational component>\n"
                gen_process += "-- Generate clk signal, if sequential component, and endOfSim is FALSE.\n"
                gen_process += "clkStim: clk <= not clk after period/2 when endOfSim = false else '0';\n"
                gen_process += "-- <delete (End)\n\n"
                gen_process += "-- instantiate unit under test (UUT)\n"
                gen_process += "UUT: "+entity_name+ "-- map component internal sigs => testbench signals\n"
                gen_process += "port map\n\t(\n"
                gen_process += io_port_map+"\n\t);\n\n"
                gen_process += "-- Signal stimulus process\n"
                gen_process += "stim_p: process -- process sensitivity list is empty, so process automatically executes at start of simulation. Suspend process at the wait; statement\n"
                gen_process += "-- <delete (Start) if note using variables\n"
                gen_process += "variable stimVec : std_logic_vector(" + str(len(inputArray)-1)+" downto 0);\n"
                gen_process += "begin\n"
                gen_process += "\t-- Apply default INPUT signal values. Do not assign output signals (generated by the UUT) in this stim_p process\n"
                gen_process += "\t-- Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge\n"
                gen_process += "\t-- if signal type is\n\t-- std_logic, use '0'\n\t-- std_logic_vector use (others => '0')\n\t-- integer use 0\n"
                gen_process += inputsToZero
                gen_process += "\treport \"%N Simulation start\";\n\n"
                gen_process += "\t-- <delete (Start) If UUT is a combinational component>\n"
                gen_process += "\treport \"Assert and toggle rst\";\n\ttestNo <= 0;\n\trst    <= '1';\n"
                gen_process += "\twait for period*1.2; -- assert rst for 1.2*period, deasserting rst 0.2*period after active clk edge\n"
                gen_process += "\trst   <= '0';\n\twait for period; -- wait 1 clock period\n\t-- <delete (End)\n\n"
                gen_process += "\t-- individual tests. Generate input signal combinations and wait for period.\n"
                gen_process += "\ttestNo <= 1;\n\twait for period;\n\n"
                gen_process += "\t-- include testbench stimulus sequence here. USe new testNo for each test set\n\n"
                gen_process += "\t-- <delete (Start) if note using variables\n"
                gen_process += "\tfor i in 0 to " + str(pow(2,len(inputArray))-1) + " loop\n"
                gen_process += "\t\tstimVec := std_logic_vector( to_unsigned(i," + str(len(inputArray)) +") );\n"
                indexOfArray = len(inputArray)
                for x in inputArray:
                    indexOfArray = indexOfArray-1
                    gen_process += "\t\t"+ x + " <= stimVec("+str(indexOfArray)+");\n"
                gen_process += "\t\twait for period;\n"
                gen_process += "\tend loop;\n"
                gen_process += "\t-- <delete (End)\n\n"
                gen_process += "\t-- <delete (Start) if not required\n"
                gen_process += inputsToZero
                gen_process += "\twait for period;\n"
                gen_process += "\t-- <delete (End)\n\n"
                gen_process += "\treport \"%N Simulation done\";\n"
                gen_process += "\tendOfSim <= TRUE; -- assert flag to stop clk signal generation\n\n"
                gen_process += "\twait; -- wait forever\n"
                if len(arch_node) != 0 and arch_node[0].firstChild is not None:

                    arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data
                    arch_name_node = arch_node[0].getElementsByTagName("archName")

                    arch_name = "comb"

                    if len(arch_name_node) != 0 and arch_name_node[0].firstChild is not None:
                        arch_name = arch_name_node[0].firstChild.data

                    gen_arch = arch_syntax.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$component_declarations", "-- unit under test (UUT) component declaration. Identical to component entity, with 'entity' replaced with 'component'")
                    gen_arch = gen_arch.replace("$port", gen_signals)
                    gen_arch = gen_arch.replace("$tbSignalDeclaration", tbSignalDeclaration)
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                    tb_code += gen_arch

        return entity_name, tb_code

    def create_testbench_file(self):
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)

        entity_name, vhdl_tb_code = self.create_vhdl_testbench_code()

        vhdl_tb_path = os.path.join(proj_path, "VHDL", "testbench", self.entity_name + "_tb.vhd")

        print(vhdl_tb_code)

        # Writing xml file
        with open(vhdl_tb_path, "w") as f:
            f.write(vhdl_tb_code)

        print("VHDL Testbench file successfully generated at ", vhdl_tb_path)

# Process4

This is a python based simulation of a single-cycle processor datapath. It models how a simplified CPU executes instructions by breaking execution into key stages: fetch, decode, execute, memory, and write back. The design is modular with each hardware component implemented into a seperate file.

##Supported Instructions
The processor supports a small custom instruction set focused on bitwise AND and bitwise OR. It has optional input inversion(NOT functionality via control signals). These instructions operate on 8 registers.

##Architecture Components
Each datapath component is implemented in its own file.

#Register File (Register.py)
-Stores 8 registers (t0-t7)
-Supports:
  -Register reads (2 inputs)
  -Register writes (1 output)
  -Initial loading of inputs
  -Dumping register state for debugging and snapshots
  
#ALU (InstructionExecute.py)
-Performs arithmetic/logic operations:
  -AND
  -OR
-Supports conditional input inversion
-Outputs result and zero flag

#Control Unit (ControlUnit.py)
-Decodes 32-bit instruction format
-Extracts:
  -Opcode
  -Funct
  -rd, rs1, rs2
-Generates control signals:
  -ALU operation
  -register write enable
  -input inversion signals

#Instruction Memory (InstructionMemory.py)
-Stores program instructions as encoded 32 bits
-Provides fetch using program counter
-Includes human readable mnemonics for debugging

#Multiplexer (mux.py)
-Implemets a 2-input multiplexer, selects between 2 data inputs based on a control signal
-Represents datapath selection 

#Processor (processor.py)
-Main execution engine
-Implements a full single-cyle flow:
  1. Fetch
  2. Decode
  3. Read
  4. Execute
  5. Memory
  6. Writeback
-Prints cycle by cycle trace and register state updates

##Program
The program computes: Y = (A & B) | (~C & D)

##How to Run
python processor.py A B C D
where A-D can be 0 or 1
if no arguments are provided than default values are used

  

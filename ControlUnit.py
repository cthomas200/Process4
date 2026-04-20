from InstructionExecute import ANDu, ORu

opcodeAND = 0b0000
opcodeOR = 0b0001

OpcodeToALU = {
    opcodeAND : ANDu,
    opcodeOR : ORu
}

opnames = {
    opcodeAND : "AND",
    opcodeOR : "OR"
}

class ControlSigns:
    def __init__(self, alu_op, inverta, invertb, reg_write, rd, rs1, rs2):
        self.alu_op = alu_op
        self.inverta = inverta
        self.invertb = invertb
        self.reg_write = reg_write
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def print(self):
        opname = 'AND' if self.alu_op == ANDu else 'OR'
        return {f'ControlSigns(alu_op={opname}, invert_a={self.inverta}, invert_b={self.invertb}, reg_write={self.reg_write}, Destination_reg={self.rd}, rs1={self.rs1}, rs2={self.rs2})'}

class ControlUnit:
    def decode(self, instr):
        opcode = (instr >> 28) & 0xF
        funct = (instr >> 24) & 0xF
        rd = (instr >> 20) & 0xF
        rs1 = (instr >> 16) & 0xF
        rs2 = (instr >> 12) & 0xF

        if opcode not in OpcodeToALU:
            raise ValueError(f'Unknow opcode {opcode}')
        alu_op = OpcodeToALU[opcode]

        inverta = bool(funct & 0b1000)
        invertb = bool(funct & 0b0100)
        reg_write = True
        
        return ControlSigns( alu_op=alu_op, inverta=inverta, invertb=invertb, reg_write=reg_write, rd=rd, rs1=rs1, rs2=rs2)
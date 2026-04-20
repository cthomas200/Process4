
from ControlUnit import opcodeAND, opcodeOR

def encode(opcode, rd, rs1, rs2, inverta=False, invertb=False):
    
    funct = (0b1000 if inverta else 0) | (0b0100 if invertb else 0)
    instr = (opcode & 0xF) << 28
    instr |= (funct & 0xF) << 24
    instr |= (rd & 0xF) << 20
    instr |= (rs1 & 0xF) << 16
    instr |= (rs2 & 0xF) << 12
    return instr

T0, T1, T2, T3, T4, T5, T6, T7 = range(8)
Program = [
    encode(opcode=opcodeAND, rd=T4, rs1=T0, rs2=T1), 
    encode(opcode=opcodeAND, rd=T6, rs1=T2, rs2=T3, inverta=True),
    encode(opcode=opcodeOR, rd=T0, rs1=T4, rs2=T6)
]

mne = [
    'and t4, t0, t1 ; t4 = A & B',
    'and t6, t2, t3 ; t6 = (~C) & D [inverta=1]',
    'or t0, t4, t6 ; t0 = t4 | t6'
]

class InstrMem:
    def __init__(self, program=None):
        self.memory = list(program or Program)

    def fetch(self, pc):
        if not (0 <= pc < len(self.memory)):
            raise IndexError(f'PC {pc} out of instruction bounds')
        return self.memory[pc]
    
    def __len__(self):
        return len(self.memory)
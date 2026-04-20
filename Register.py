
class RegisterFile: 
    def __init__(self):
        self.registers = [0] * 8 # number of regs

    def load(self, A, B, C, D):
        self.registers[0] = A & 0xFFFFFFFF #t0
        self.registers[1] = B & 0xFFFFFFFF #t1
        self.registers[2] = C & 0xFFFFFFFF #t2
        self.registers[3] = D & 0xFFFFFFFF #t3
    
    def read(self, rs1, rs2):
        if not (0 <= rs1 < 8 and 0 <= rs2 < 8):
            raise ValueError(f'Register index out of range: rs1={rs1}, rs2={rs2}')
        return self.registers[rs1], self.registers[rs2]
    
    def write(self, rd, value, enabled):
        if not (0 <= rd < 8):
            raise ValueError(f'Register index out of range: rd={rd}')
        if enabled:
            self.registers[rd] = value & 0xFFFFFFFF 

    def dump(self):
        return {f't{i}': self.registers[i] for i in range(8)}
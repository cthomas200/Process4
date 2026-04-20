
ANDu = 0b00
ORu = 0b01

class ALU:
    def execute(self, a, b, alu_op, inverta, invertb):
        op_a = (~a & 0xFFFFFFFF) if inverta else (a & 0xFFFFFFFF)
        op_b = (~b & 0xFFFFFFFF) if invertb else (b & 0xFFFFFFFF)

        if alu_op == ANDu:
            res = op_a & op_b
        elif alu_op == ORu:
            res = op_a | op_b
        else:
            raise ValueError('Unsupported ALU operation')
        
        res &= 0xFFFFFFFF
        zero = ( res == 0)
        return res, zero
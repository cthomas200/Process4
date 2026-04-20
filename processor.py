#Chyna Thomas

import sys
from Register import RegisterFile
from InstructionExecute import ALU, ANDu
from ControlUnit import ControlUnit, opnames
from InstructionMemory import InstrMem, mne
from mux import mux

OPnames = [ ]
def PC(pc, instrmem: InstrMem):
    next = pc + 1
    return pc, next

def getInstr(pc, instrmem: InstrMem):
    return instrmem.fetch(pc)

def InstrDecode(instr, reg_file: RegisterFile, CU: ControlUnit):
    signs = CU.decode(instr)
    reada, readb = reg_file.read(signs.rs1, signs.rs2)
    return signs, reada, readb

def InstrExe(signs, reada, readb, alu: ALU):
    inputa = mux(False, reada, ~reada & 0xFFFFFFFF)
    inputb = mux(False, readb, ~readb & 0xFFFFFFFF)
    res, zero = alu.execute(inputa, inputb, alu_op=signs.alu_op, inverta=signs.inverta, invertb=signs.invertb)
    return res, zero

def Memory(res):
    return res

def writeBack(signs, res, reg_file:RegisterFile):
    wb = mux(True, 0, res)
    reg_file.write(signs.rd, wb, signs.reg_write)

def printSign(signs, pc, mne):
    opname = opnames[signs.alu_op]
    if signs.inverta and signs.alu_op == ANDu:
        opname = 'AND-NOT(a)'
    elif signs.invertb and signs.alu_op == ANDu:
        opname = 'AND-NOT(b)'
   

    print(f'Instruction [{pc}]: {mne}')
    print(f'    Control Signals     \nalu_op = {opname} reg_write= {"1" if signs.reg_write  else "0"}')
    print(f'invert_a = {"1" if signs.inverta else "0":<10} invert_b = {"1" if signs.invertb else "0"}')
    print(f'rd=t{signs.rd} rs1=t{signs.rs1} rs2=t{signs.rs2}')

def main():
    if len(sys.argv) == 5:
        A, B, C, D = (int(x) & 1 for x in sys.argv[1:]) 
    else:
        A,B,C,D = 1, 1, 1, 1

    reg_file = RegisterFile()
    alu = ALU()
    CU = ControlUnit()
    instrMem = InstrMem()

    reg_file.load(A, B, C, D)
    print('Initial Register State')
    state = reg_file.dump()
    pairs = [f"t{i}={state[f't{i}']}" for i in range(8)]
    print(' '.join(pairs))

    trace = []
    pc = 0
    while pc < len(instrMem):
        print(f'\n CYCLE {pc + 1}')

        current, next = PC(pc, instrMem)
        instr = getInstr(current, instrMem)
        print(f' FETCH : PC={current} instr={instr}')

        signs, reada, readb, = InstrDecode(instr, reg_file, CU)
        print(f' DECODE : rs1=t{signs.rs1}({reada}) rs2=t{signs.rs2}({readb}) rd=t{signs.rd}')
        printSign(signs, current, mne[current])

        alu_res, zero = InstrExe(signs, reada, readb, alu)
        note = ''
        if signs.inverta:
            note = f' (~t{signs.rs1}={~reada & 0xFFFFFFFF}) & t{signs.rs2}={readb}'
        elif signs.invertb:
            note = f' t{signs.rs1}={reada} & (~t{signs.rs2}={~readb & 0xFFFFFFFF})'
        print(f' EXECUTE : ALU result = {alu_res}{note}')

        mem_res = Memory(alu_res)
        print(f' MEMORY : pass = {mem_res}')
        writeBack(signs, mem_res, reg_file)
        print(f' WRITEBACK : t{signs.rd} from {mem_res}')

        print(f'\nRegister State After PC={pc + 1}:')
        state = reg_file.dump()
        pairs = [f"t{i}={state[f't{i}']}" for i in range(8)]
        print(' '.join(pairs))
        trace.append({
            'PC': current,
            'mnemonic': mne[current],
            'rd': signs.rd,
            'result': mem_res
        }
        )

        pc = next
    
    regs = reg_file.dump()
    t4 = regs['t4']
    t6 = regs['t6']
    Y = regs['t0']

    desiredt4 = A & B
    desiredt6 = (1 - C) & D
    desiredY = desiredt4 | desiredt6

    print('Intermediate Values:')
    print(f' t4 = A & B =  {A} & {B} = {t4}')
    print(f' t6 = (~C) & D = ~{C} & {D} = {t6}')
    print(f' Y = t4 | t6 = {t4} | {t6} = {Y}\n')
    print()
    print('Result:')
    print(f'Y = A*B + C`*D = {Y}')
    print(f'Expected value = {desiredY}')
    match = 'PASS' if Y == desiredY else 'FAIL'
    print(f'Verication = {match}')

main()

    






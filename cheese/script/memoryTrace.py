from triton import *


def dump(opType, instruction, operand):

    opAccess         = 'R' if opType == IDREF.OPERAND.MEM_R else 'W'
    memoryAccess     = operand.value
    memoryAccessSize = operand.size
    
    a = str()
    d = '[%c:%d] 0x%016x: %s' %(opAccess, memoryAccessSize, instruction.address, instruction.assembly)
    
    if checkReadAccess(memoryAccess):
        a = '%c:0x%016x:' %(opAccess, memoryAccess)
        for i in range(memoryAccessSize):
            a += ' %02x' %(getMemValue(memoryAccess+i, 1))
    
    print '%s%s%s (%#x)' %(d, ' '*(70-len(d)), a, getMemValue(memoryAccess, memoryAccessSize))
    return


def before(instruction):
    for operand in instruction.operands:
        if operand.type == IDREF.OPERAND.MEM_R:
            dump(IDREF.OPERAND.MEM_R, instruction, operand)
            return
    return


def after(instruction):
    for operand in instruction.operands:
        if operand.type == IDREF.OPERAND.MEM_W:
            dump(IDREF.OPERAND.MEM_W, instruction, operand)
            return
    return


if __name__ == '__main__':

    # Start the symbolic analysis from the entry point
    startAnalysisFromSymbol('main')

    # Add a callback.
    addCallback(before, IDREF.CALLBACK.BEFORE)
    addCallback(after,  IDREF.CALLBACK.AFTER)

    # Run the instrumentation - Never returns
    runProgram()



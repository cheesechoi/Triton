
from triton import *


#0x0000000000400545 <+24>:  mov    eax,DWORD PTR [rbp-0x4]



def dump(opType, instruction, operand):

    opAccess         = 'R' if opType == IDREF.OPERAND.MEM_R else 'W'
    memoryAccess     = operand.getMem().getAddress()
    memoryAccessSize = operand.getMem().getSize()

    a = str()
    d = '[%c:%d] 0x%016x: %s' %(opAccess, memoryAccessSize, instruction.getAddress(), instruction.getDisassembly())

    if checkReadAccess(memoryAccess):
        a = '%c:0x%016x:' %(opAccess, memoryAccess)
        for i in range(memoryAccessSize):
            a += ' %02x' %(getMemValue(memoryAccess+i, 1))

    print '\t Memory Info : %s%s%s (%#x)' %(d, ' '*(70-len(d)), a, getMemValue(memoryAccess, memoryAccessSize))
    return



# callback function called before instruction excute

def cbefore(instruction):
    if 0x400545 == instruction.getAddress():
        print '----- cbefore -----'
        print '%#x: %s' %(instruction.getAddress(), instruction.getDisassembly())
        print 'getRegValue RAX : %x'%getRegValue(IDREF.REG.RAX)

        # print Symbolic information
        for se in instruction.getSymbolicExpressions():
            print '\t -> #%d = %s %s' %(se.getId(), se.getAst(), (('; ' + se.getComment()) if se.getComment() is not None else ''))

        # print Memory information
        for operand in instruction.getOperands():
            if operand.getType() == IDREF.OPERAND.MEM_R:
                dump(IDREF.OPERAND.MEM_R, instruction, operand)



# callback function called after instruction excute

def cafter(instruction):
    if 0x400545 == instruction.getAddress():
        print '----- cafter -----'
        print '%#x: %s' %(instruction.getAddress(), instruction.getDisassembly())
        print 'getRegValue RAX : %x'%getRegValue(IDREF.REG.RAX)

        for se in instruction.getSymbolicExpressions():
            print '\t -> #%d = %s %s' %(se.getId(), se.getAst(), (('; ' + se.getComment()) if se.getComment() is not None else ''))

        for operand in instruction.getOperands():
            if operand.getType() == IDREF.OPERAND.MEM_R:
                dump(IDREF.OPERAND.MEM_R, instruction, operand)


if __name__ == '__main__':

    # Start the symbolic analysis from the 'check' function
    startAnalysisFromSymbol('check')

    # Add a callback.
    # BEFORE: Add the callback before the instruction processing
    # AFTER:  Add the callback after the instruction processing
    # FINI:   Add the callback at the end of the execution
    addCallback(cbefore, IDREF.CALLBACK.BEFORE)
    addCallback(cafter, IDREF.CALLBACK.AFTER)

    # Run the instrumentation - Never returns
    runProgram()


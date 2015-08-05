from triton import *
import sys

BLUE  = "\033[94m"
ENDC  = "\033[0m"
GREEN = "\033[92m"
RED   = "\033[91m"

"""
 To check convertExprToSymVal() affect evaluateAST(expr)
 Output

 root > ⋯ Triton > ./triton ./cheese/tester/semanticsTesting.py ./samples/ir_test_suite/ir
...
[OK] 0x4006d8: bswap ecx
[OK] 0x4006da: bswap rdx
[OK] 0x4006dd: xor rcx, rcx
[TESTING] 0x4006e0: mov cl, 0x3
#516 = SymVar_0
SymVar_0
SymVar_0
terminate called after throwing an instance of 'std::runtime_error'
  what():  smtAstVariableNode: UNSET
  ./triton: line 20: 47458 Aborted                 (core dumped) $PIN_BIN_PATH -t $TRITON_LIB_PATH -script $1 -- ${@:2}
...

"""



def sbefore(instruction):
    concretizeAllMem()
    concretizeAllReg()
    return


def cafter(instruction):

    # To check convertExprToSymVal() affect evaluateAST(expr)
    _debug = 1

    if _debug == 1 and 'mov cl, 0x3' == instruction.getDisassembly():
        print "[%sTESTING%s] %#x: %s" %(BLUE, ENDC, instruction.getAddress(), instruction.getDisassembly())
        rcxId = getRegSymbolicID(IDREF.REG.RCX)
        convertExprToSymVar(rcxId, 8)

    bad  = list()
    regs = getRegs()

    for reg, data in regs.items():

        cvalue = data['concreteValue']
        seid   = data['symbolicExpr']

        if seid == IDREF.MISC.UNSET:
            continue

        if _debug == 1 and 'mov cl, 0x3' == instruction.getDisassembly():
            print getSymExpr(seid)
            print getSymExpr(seid).getAst()
            print getFullExpression(getSymExpr(seid).getAst())
            expr   = getFullExpression(getSymExpr(seid).getAst())
            print evaluateAST(expr)
            print "test print done"
        
        expr   = getFullExpression(getSymExpr(seid).getAst())
        svalue = evaluateAST(expr)

        if cvalue != svalue:
            bad.append({
                'reg': getRegName(reg),
                'svalue': svalue,
                'cvalue': cvalue,
                'expr': getSymExpr(seid).getAst()
            })

    if len(instruction.getSymbolicExpressions()) == 0:
        print "[%s??%s] %#x: %s" %(BLUE, ENDC, instruction.getAddress(), instruction.getDisassembly())
        return
    if not bad:
        print "[%sOK%s] %#x: %s" %(GREEN, ENDC, instruction.getAddress(), instruction.getDisassembly())
    else:
        print "[%sKO%s] %#x: %s (%s%d error%s)" %(RED, ENDC, instruction.getAddress(), instruction.getDisassembly(), RED, len(bad), ENDC)
        for w in bad:
            print "     Register       : %s" %(w['reg'])
            print "     Symbolic Value : %016x" %(w['svalue'])
            print "     Concrete Value : %016x" %(w['cvalue'])
            print "     Expression     : %s" %(w['expr'])
    return


if __name__ == '__main__':
    startAnalysisFromSymbol('main')
    addCallback(cafter, IDREF.CALLBACK.AFTER)
    addCallback(sbefore, IDREF.CALLBACK.BEFORE_SYMPROC)
    runProgram()



from triton import *
import  smt2lib

# Triton found several collisions. Example with the first collision:
# $ ./samples/crackmes/crackme_hash lrdxq
# Win
# $
#

expr = str()

def cafter(instruction):
    global expr
    # movzx esi,BYTE PTR [rax]
    # RAX points on the user password

    # cheese's modified.
    # 0x0000000000400559 <+44>: movzx  eax,BYTE PTR [rax]
    if instruction.address == 0x400559:
        print "Address 0x400559 progress"
        raxId = getRegSymbolicID(IDREF.REG.RAX)
        print convertExprToSymVar(raxId, 8) 

    # mov eax,DWORD PTR [rbp-0x4]
    # RAX must be equal to 0xad6d to win

    # cheese's modified.
    # 0x0000000000400561 <+52>: cmp    BYTE PTR [rbp-0x1],0x1
    if instruction.address == 0x400561:
        print '[+] Address <cmp (result_xor) 0x1>'
        raxId = getRegSymbolicID(IDREF.REG.RAX)
        raxExpr = getFullExpression(getSymExpr(raxId).getAst())
       
        #for se in instruction.symbolicExpressions:
                #print '\t -> #%d = %s %s' %(se.getId(), se.getAst(), (('; ' + se.getComment()) if se.getComment() is not None else '')) 

        zfId = getRegSymbolicID(IDREF.FLAG.ZF)
        zfExpr = getFullExpression(getSymExpr(zfId).getAst())
        cfId = getRegSymbolicID(IDREF.FLAG.CF)
        cfExpr = getFullExpression(getSymExpr(cfId).getAst())

        # ZF != true and CF != true
        expr =  smt2lib.compound([
                    smt2lib.smtAssert(smt2lib.equal(zfExpr, smt2lib.bvfalse()))
                    #smt2lib.smtAssert(smt2lib.equal(cfExpr, smt2lib.bvfalse()))
                ])
        # cheese's modified !
        # Get max 20 different models
        print expr
        models = getModels(expr, 20)
        print "2"
        for model in models:
            print {k: "0x%x, '%c'" % (v, v) for k, v in model.items()}



if __name__ == '__main__':

    startAnalysisFromSymbol('main')
    addCallback(cafter, IDREF.CALLBACK.AFTER)
    runProgram()


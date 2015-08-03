
from triton import *
import  smt2lib

"""
on test.

root@ubuntu:Triton# ./triton cheese/script/getModelcheck.range1.py cheese/example/getModelcheck.range1 a
nope!
"""

expr = str()
listExpr = list()

def cafter(instruction):
    global expr
    global listExpr

    if 0x400547 == instruction.getAddress():# == 0x400547:
        print "Address 0x400547 progress"
        raxId = getRegSymbolicID(IDREF.REG.RAX)
        print convertExprToSymVar(raxId, 8) #only 8bit


    #0x0000000000400553 <+38>:  cmp    BYTE PTR [rbp-0x1],0x59
    if instruction.getAddress() == 0x40054d:
        print '[+] Address <cmp argv[1][0] 0x59>'
        # WE DONT WANT JUMP, TOO.
        # 0x0000000000400557 <+42>:   jg     0x40056a <main+61>
        # jmp if greater. ZF = 0 and SF = OF
        # ZF = 1 or SF <> OF

        zfId = getRegSymbolicID(IDREF.FLAG.ZF)
        zfExpr = getFullExpression(getSymExpr(zfId).getAst())
        sfId = getRegSymbolicID(IDREF.FLAG.SF)
        sfExpr = getFullExpression(getSymExpr(sfId).getAst())
        ofId = getRegSymbolicID(IDREF.FLAG.OF)
        ofExpr = getFullExpression(getSymExpr(ofId).getAst())

        """
        #### [!!] expression test code.
        testexpr = smt2lib.equal(zfExpr, smt2lib.bvfalse())                          # ZF = 1
        testexpr2 = smt2lib.equal(sfExpr, ofExpr) # SF <> OF
        testexpr3 = smt2lib.bvand(testexpr, testexpr2)                               # ( ZF = 1 ) or ( SF <> OF ), ERROR. 
        #testexpr3 = smt2lib.bvor(zfExpr, ofExpr)
        testexpr4 = smt2lib.equal(testexpr3, smt2lib.bvfalse())
        testAssert = smt2lib.smtAssert(testexpr4)

        print testexpr3

        tests_models = getModels(testAssert, 40)
        print "1"
        for model in tests_models:
            print {k: "0x%x, '%c'" % (v, v) for k, v in model.items()}
        """
        
        #### [!!] expression test code.
        testexpr = smt2lib.equal(zfExpr, smt2lib.bvtrue())                          # ZF = 1
        testexpr2 = smt2lib.equal(smt2lib.bvxor(sfExpr, ofExpr), smt2lib.bvfalse()) # SF <> OF
        testexpr3 = smt2lib.bvor(testexpr, testexpr2)                               # ( ZF = 1 ) or ( SF <> OF ), ERROR. 
                                                                                    #(error "line 1 column 707: operator is applied to arguments of the wrong sort")
        testexpr4 = smt2lib.equal(testexpr3, smt2lib.bvtrue())
        testAssert = smt2lib.smtAssert(testexpr4)

        print testAssert

        tests_models = getModels(testAssert, 40)
        for model in tests_models:
            print {k: "0x%x, '%c'" % (v, v) for k, v in model.items()}
 
#def cfin(instruction):

if __name__ == '__main__':

    startAnalysisFromSymbol('main')
    addCallback(cafter, IDREF.CALLBACK.AFTER)
    runProgram()




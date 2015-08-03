
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

    # 0x0000000000400547 <+26>:   movzx  eax,BYTE PTR [rax]
    if 0x400547 == instruction.getAddress():# == 0x400547:
        print "Address 0x400547 progress"
        raxId = getRegSymbolicID(IDREF.REG.RAX)
        print convertExprToSymVar(raxId, 8) #only 8bit


    # 0x000000000040054d <+32>:  cmp    BYTE PTR [rbp-0x1],0x41 
    if instruction.getAddress() == 0x40054d:
        print '[+] Address <cmp argv[1][0] 0x41>'
    	# WE DONT WANT JUMP
        # 0x0000000000400551 <+36>: jle    0x40056a <main+61>
        # jump if less or equal . ZF = 1 or SF <> OF. 
        # ZF = 0 and SF == OF

        zfId = getRegSymbolicID(IDREF.FLAG.ZF)
        zfExpr = getFullExpression(getSymExpr(zfId).getAst())
        sfId = getRegSymbolicID(IDREF.FLAG.SF)
        sfExpr = getFullExpression(getSymExpr(sfId).getAst())
        ofId = getRegSymbolicID(IDREF.FLAG.OF)
        ofExpr = getFullExpression(getSymExpr(ofId).getAst())

        
        listExpr.append(smt2lib.smtAssert(smt2lib.equal(zfExpr, smt2lib.bvfalse())))
        listExpr.append(smt2lib.smtAssert(smt2lib.equal(sfExpr, ofExpr)))
        
        test = smt2lib.compound(listExpr)
        tests_models = getModels(test, 40)
        for model in tests_models:
            print {k: "0x%x, '%c'" % (v, v) for k, v in model.items()}
        raw_input()

    #0x0000000000400553 <+38>:  cmp    BYTE PTR [rbp-0x1],0x59
    if instruction.getAddress() == 0x400553:
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

        
        #### [!!] expression test code.
        testexpr = smt2lib.equal(zfExpr, smt2lib.bvtrue())                          # ZF = 1
        testexpr2 = smt2lib.equal(smt2lib.bvxor(sfExpr, ofExpr), smt2lib.bvfalse()) # SF <> OF
        testexpr3 = smt2lib.bvor(testexpr, testexpr2)                               # ( ZF = 1 ) or ( SF <> OF ), ERROR. 
                                                                                    #(error "line 1 column 707: operator is applied to arguments of the wrong sort")
        testexpr4 = smt2lib.equal(testexpr3, smt2lib.bvtrue())
        testAssert = smt2lib.smtAssert(testexpr4)
        tests_models = getModels(testAssert, 40)
        for model in tests_models:
            print {k: "0x%x, '%c'" % (v, v) for k, v in model.items()}
        raw_input()
 
#def cfin(instruction):

if __name__ == '__main__':

    startAnalysisFromSymbol('main')
    addCallback(cafter, IDREF.CALLBACK.AFTER)
    runProgram()





from triton import *
import  smt2lib

expr = str()
"""
root@ubuntu:Triton# ./triton cheese/script/getModelcheck.jz.py cheese/example/getModelcheck.jz a
Address 0x400547 progress

Address 0x400547 progress
SymVar_0
[+] Address <cmp argv[1][0] 0x54>
(assert (= (ite (= ((_ extract 7 0) (bvsub ((_ extract 7 0) ((_ extract 7 0) ((_ extract 7 0) SymVar_0))) (_ bv84 8))) (_ bv0 8)) (_ bv1 1) (_ bv0 1)) (_ bv1 1)))
2
{'SymVar_0': "0x54, 'T'"}

nope!
"""


def cafter(instruction):
    global expr

    # 0x0000000000400547 <+26>:   movzx  eax,BYTE PTR [rax]
    if 0x400547 == instruction.getAddress():# == 0x400547:
        print "Address 0x400547 progress"
        raxId = getRegSymbolicID(IDREF.REG.RAX)
        print convertExprToSymVar(raxId, 8) #only 8bit

    # 0x000000000040054d <+32>:  cmp    BYTE PTR [rbp-0x1],0x54
    if instruction.getAddress() == 0x40054d:
        print '[+] Address <cmp argv[1][0] 0x54>'
    	# WE WANT NOT JUMP
	# 0400551 <+36>:	jne    0x400564 <main+55>
        zfId = getRegSymbolicID(IDREF.FLAG.ZF)
        zfExpr = getFullExpression(getSymExpr(zfId).getAst())

        expr =  smt2lib.compound([
                    smt2lib.smtAssert(smt2lib.equal(zfExpr, smt2lib.bvtrue()))
                ])
        # Get max 20 different models
        print expr
        models = getModels(expr, 20)
        print "2"
        for model in models:
            print {k: "0x%x, '%c'" % (v, v) for k, v in model.items()}
	raw_input()

if __name__ == '__main__':

    startAnalysisFromSymbol('main')
    addCallback(cafter, IDREF.CALLBACK.AFTER)
    runProgram()


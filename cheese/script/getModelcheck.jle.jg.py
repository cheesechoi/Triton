from triton import *
import  smt2lib

"""
 root  ⋯  source  tools  Triton  ./triton cheese/script/getModelcheck.jle.jg.py cheese/example/getModelcheck.jle.jg b
Address 0x400547 progress
[+] Address <cmp argv[1][0] 0x41>
{'SymVar_0': "0x50, 'P'"}
{'SymVar_0': "0x60, '`'"}
{'SymVar_0': "0x5a, 'Z'"}
{'SymVar_0': "0x4a, 'J'"}
{'SymVar_0': "0x42, 'B'"}
{'SymVar_0': "0x62, 'b'"}
{'SymVar_0': "0x6a, 'j'"}
{'SymVar_0': "0x68, 'h'"}
{'SymVar_0': "0x69, 'i'"}
{'SymVar_0': "0x49, 'I'"}

[+] Address <cmp argv[1][0] 0x59>
{'SymVar_0': "0x50, 'P'"}
{'SymVar_0': "0x59, 'Y'"}
{'SymVar_0': "0x58, 'X'"}
{'SymVar_0': "0x48, 'H'"}
{'SymVar_0': "0x44, 'D'"}
{'SymVar_0': "0x4c, 'L'"}
{'SymVar_0': "0x54, 'T'"}
{'SymVar_0': "0x49, 'I'"}
{'SymVar_0': "0x4d, 'M'"}
{'SymVar_0': "0x4f, 'O'"}

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
        convertExprToSymVar(raxId, 8) #only 8bit


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
 
        exprComp = smt2lib.compound(listExpr)
        models = getModels(exprComp, 10)
        
        for model in models:
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

	exprJgNotJump = smt2lib.equal(smt2lib.bvor(smt2lib.bvxor(sfExpr,ofExpr), zfExpr), smt2lib.bvtrue())
	listExpr.append( smt2lib.smtAssert(exprJgNotJump) )
        
	exprComp = smt2lib.compound(listExpr)
	models = getModels(exprComp, 10)
        for model in models:
            print {k: "0x%x, '%c'" % (v, v) for k, v in model.items()}
        raw_input()
 
if __name__ == '__main__':

    startAnalysisFromSymbol('main')
    addCallback(cafter, IDREF.CALLBACK.AFTER)
    runProgram()




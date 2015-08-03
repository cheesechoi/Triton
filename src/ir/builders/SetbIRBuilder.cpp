/*
**  Copyright (C) - Triton
**
**  This program is under the terms of the LGPLv3 License.
*/

#include <iostream>
#include <sstream>
#include <stdexcept>

#include <SetbIRBuilder.h>
#include <Registers.h>
#include <SMT2Lib.h>
#include <SymbolicExpression.h>


SetbIRBuilder::SetbIRBuilder(uint64 address, const std::string &disassembly):
  BaseIRBuilder(address, disassembly) {
}


void SetbIRBuilder::imm(AnalysisProcessor &ap, Inst &inst) const {
  OneOperandTemplate::stop(this->disas);
}


void SetbIRBuilder::reg(AnalysisProcessor &ap, Inst &inst) const {
  SymbolicExpression *se;
  smt2lib::smtAstAbstractNode *expr, *cf;
  auto reg = this->operands[0].getReg().getTritonRegId();
  auto regSize = this->operands[0].getReg().getSize();

  /* Create the SMT semantic */
  cf = ap.buildSymbolicFlagOperand(ID_CF);

  /* Finale expr */
  expr = smt2lib::ite(
            smt2lib::equal(
              cf,
              smt2lib::bvtrue()),
            smt2lib::bv(1, BYTE_SIZE_BIT),
            smt2lib::bv(0, BYTE_SIZE_BIT));

  /* Create the symbolic expression */
  se = ap.createRegSE(inst, expr, reg, regSize);

  /* Apply the taint via the concretization */
  if (ap.getFlagValue(ID_CF) == 1)
    ap.assignmentSpreadTaintRegReg(se, reg, ID_CF);

}


void SetbIRBuilder::mem(AnalysisProcessor &ap, Inst &inst) const {
  SymbolicExpression *se;
  smt2lib::smtAstAbstractNode *expr, *cf;
  auto mem = this->operands[0].getMem().getAddress();
  auto memSize = this->operands[0].getMem().getSize();

  /* Create the SMT semantic */
  cf = ap.buildSymbolicFlagOperand(ID_CF);

  /* Finale expr */
  expr = smt2lib::ite(
            smt2lib::equal(
              cf,
              smt2lib::bvtrue()),
            smt2lib::bv(1, BYTE_SIZE_BIT),
            smt2lib::bv(0, BYTE_SIZE_BIT));

  /* Create the symbolic expression */
  se = ap.createMemSE(inst, expr, mem, memSize);

  /* Apply the taint via the concretization */
  if (ap.getFlagValue(ID_CF) == 1)
    ap.assignmentSpreadTaintMemReg(se, mem, ID_CF, memSize);

}


void SetbIRBuilder::none(AnalysisProcessor &ap, Inst &inst) const {
  OneOperandTemplate::stop(this->disas);
}


Inst *SetbIRBuilder::process(AnalysisProcessor &ap) const {
  this->checkSetup();

  Inst *inst = new Inst(ap.getThreadID(), this->address, this->disas);

  try {
    this->templateMethod(ap, *inst, this->operands, "SETB");
    ap.incNumberOfExpressions(inst->numberOfExpressions()); /* Used for statistics */
    ControlFlow::rip(*inst, ap, this->nextAddress);
  }
  catch (std::exception &e) {
    delete inst;
    throw;
  }

  return inst;
}


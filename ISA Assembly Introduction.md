ISA Assembly Introduction
==============================

# Data Movement

## LOAD_V
> LOAD_V {vreg} {reg_adr}
> > vreg : vector register to store data retrived from memory.\
> > reg_adr : scalar register that has memory address.
## LOAD_VS
> LOAD_V {vreg} {reg_adr} {stride}
> > vreg : vector register to store data retrived from memory.\
> > reg_adr : scalar register that has memory address.\
> > stride : immediate stride value.
## LOAD_S
> LOAD_S  {reg} {reg_adr}
> > reg : scalar register to store data retrived from memory.\
> > reg_adr : scalar register that has memory address.\
## STORE_V

## STORE_VS

## STORE_S

## MOV

# Data Processing

## ADD_VV

## ADD_VS

## ADD_SS

## SUB_VV

## SUB_VS

## SUB_SS

## MUL_VV

## MUL_VS

## MUL_SS

## RELU_V

## CMP_S

# Control

## JUMP

## JE

## JNE

# Debug Function

## __DEBUG_PASS

## __DEBUG_PRTREG

## __DEBUG_PRTVREG

## __DEBUG_MEMVIEW

## __DEBUG_PRT_MSG

## __DEBUG_MEM_2_FILE

## __DEBUG_FILE_2_MEM

## __DEBUG_EXIT

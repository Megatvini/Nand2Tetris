//push constant 17
@17
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 17
@17
D=A
@R0
A=M
M=D
@R0
M=M+1

//eq
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@EQUALS_0
D;JEQ

(NOT_EQUALS_0)
@R0
A=M
A=A-1
A=A-1
M=0

@END_0
0;JMP

(EQUALS_0)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_0)
@R0
M=M-1

//push constant 17
@17
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 16
@16
D=A
@R0
A=M
M=D
@R0
M=M+1

//eq
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@EQUALS_1
D;JEQ

(NOT_EQUALS_1)
@R0
A=M
A=A-1
A=A-1
M=0

@END_1
0;JMP

(EQUALS_1)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_1)
@R0
M=M-1

//push constant 16
@16
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 17
@17
D=A
@R0
A=M
M=D
@R0
M=M+1

//eq
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@EQUALS_2
D;JEQ

(NOT_EQUALS_2)
@R0
A=M
A=A-1
A=A-1
M=0

@END_2
0;JMP

(EQUALS_2)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_2)
@R0
M=M-1

//push constant 892
@892
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 891
@891
D=A
@R0
A=M
M=D
@R0
M=M+1

//lt
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@LESS_3
D;JLT

(NOT_LESS_3)
@R0
A=M
A=A-1
A=A-1
M=0

@END_3
0;JMP

(LESS_3)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_3)
@R0
M=M-1

//push constant 891
@891
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 892
@892
D=A
@R0
A=M
M=D
@R0
M=M+1

//lt
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@LESS_4
D;JLT

(NOT_LESS_4)
@R0
A=M
A=A-1
A=A-1
M=0

@END_4
0;JMP

(LESS_4)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_4)
@R0
M=M-1

//push constant 891
@891
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 891
@891
D=A
@R0
A=M
M=D
@R0
M=M+1

//lt
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@LESS_5
D;JLT

(NOT_LESS_5)
@R0
A=M
A=A-1
A=A-1
M=0

@END_5
0;JMP

(LESS_5)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_5)
@R0
M=M-1

//push constant 32767
@32767
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 32766
@32766
D=A
@R0
A=M
M=D
@R0
M=M+1

//gt
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@GREATER_6
D;JGT

(NOT_GREATER_6)
@R0
A=M
A=A-1
A=A-1
M=0

@END_6
0;JMP

(GREATER_6)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_6)
@R0
M=M-1

//push constant 32766
@32766
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 32767
@32767
D=A
@R0
A=M
M=D
@R0
M=M+1

//gt
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@GREATER_7
D;JGT

(NOT_GREATER_7)
@R0
A=M
A=A-1
A=A-1
M=0

@END_7
0;JMP

(GREATER_7)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_7)
@R0
M=M-1

//push constant 32766
@32766
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 32766
@32766
D=A
@R0
A=M
M=D
@R0
M=M+1

//gt
@R0
A=M

A=A-1
D=M

A=A-1
D=M-D

@GREATER_8
D;JGT

(NOT_GREATER_8)
@R0
A=M
A=A-1
A=A-1
M=0

@END_8
0;JMP

(GREATER_8)
@R0
A=M
A=A-1
A=A-1
M=-1

(END_8)
@R0
M=M-1

//push constant 57
@57
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 31
@31
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 53
@53
D=A
@R0
A=M
M=D
@R0
M=M+1

//add
@R0
A=M
A=A-1
D=M
A=A-1
M=M+D
@R0
M=M-1

//push constant 112
@112
D=A
@R0
A=M
M=D
@R0
M=M+1

//sub
@R0
A=M
A=A-1
D=M
A=A-1
M=M-D
@R0
M=M-1

//neg
@R0
A=M
A=A-1
M=-M

//and
@R0
A=M
A=A-1
D=M
A=A-1
M=M&D
@R0
M=M-1

//push constant 82
@82
D=A
@R0
A=M
M=D
@R0
M=M+1

//or
@R0
A=M
A=A-1
D=M
A=A-1
M=M|D
@R0
M=M-1

//not
@R0
A=M
A=A-1
M=!M


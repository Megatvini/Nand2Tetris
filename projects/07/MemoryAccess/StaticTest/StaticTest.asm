//push constant 111
@111
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 333
@333
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 888
@888
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop static 8
@R0
A=M
A=A-1
D=M

@R13
M=D

@8
D=A
@16
A=M
A=A+D

D=A
@R14
M=D

@R13
D=M

@R14
A=M

M=D
@R0
M=M-1

//pop static 3
@R0
A=M
A=A-1
D=M

@R13
M=D

@3
D=A
@16
A=M
A=A+D

D=A
@R14
M=D

@R13
D=M

@R14
A=M

M=D
@R0
M=M-1

//pop static 1
@R0
A=M
A=A-1
D=M

@R13
M=D

@1
D=A
@16
A=M
A=A+D

D=A
@R14
M=D

@R13
D=M

@R14
A=M

M=D
@R0
M=M-1

//push static 3
@3
D=A
@16
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1

//push static 1
@1
D=A
@16
A=M+D
D=M
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

//push static 8
@8
D=A
@16
A=M+D
D=M
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


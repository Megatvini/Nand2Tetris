//push constant 3030
@3030
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop pointer 0
@R0
A=M
A=A-1

D=M
@3
M=D
@R0
M=M-1

//push constant 3040
@3040
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop pointer 1
@R0
A=M
A=A-1

D=M
@4
M=D
@R0
M=M-1

//push constant 32
@32
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop this 2
@R0
A=M
A=A-1
D=M

@R13
M=D

@2
D=A
@3
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

//push constant 46
@46
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop that 6
@R0
A=M
A=A-1
D=M

@R13
M=D

@6
D=A
@4
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

//push pointer 0
@3
D=M
@R0
A=M
M=D
@R0
M=M+1

//push pointer 1
@4
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

//push this 2
@2
D=A
@3
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

//push that 6
@6
D=A
@4
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


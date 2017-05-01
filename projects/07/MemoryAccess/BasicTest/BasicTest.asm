//push constant 10
@10
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop local 0
@R0
A=M
A=A-1
D=M

@R13
M=D

@0
D=A
@1
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

//push constant 21
@21
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 22
@22
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop argument 2
@R0
A=M
A=A-1
D=M

@R13
M=D

@2
D=A
@2
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

//pop argument 1
@R0
A=M
A=A-1
D=M

@R13
M=D

@1
D=A
@2
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

//push constant 36
@36
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop this 6
@R0
A=M
A=A-1
D=M

@R13
M=D

@6
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

//push constant 42
@42
D=A
@R0
A=M
M=D
@R0
M=M+1

//push constant 45
@45
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop that 5
@R0
A=M
A=A-1
D=M

@R13
M=D

@5
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

//pop that 2
@R0
A=M
A=A-1
D=M

@R13
M=D

@2
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

//push constant 510
@510
D=A
@R0
A=M
M=D
@R0
M=M+1

//pop temp 6
@R0
A=M
A=A-1

D=M
@11
M=D
@R0
M=M-1

//push local 0
@0
D=A
@1
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1

//push that 5
@5
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

//push argument 1
@1
D=A
@2
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

//push this 6
@6
D=A
@3
A=M+D
D=M
@R0
A=M
M=D
@R0
M=M+1

//push this 6
@6
D=A
@3
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

//sub
@R0
A=M
A=A-1
D=M
A=A-1
M=M-D
@R0
M=M-1

//push temp 6
@11
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


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
@300
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
@402
M=D
@R0
M=M-1

//pop argument 1
@R0
A=M
A=A-1
D=M
@401
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
@3006
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
@3015
M=D
@R0
M=M-1

//pop that 2
@R0
A=M
A=A-1
D=M
@3012
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
@300
D=M
@R0
A=M
M=D
@R0
M=M+1

//push that 5
@3015
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
@401
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
@3006
D=M
@R0
A=M
M=D
@R0
M=M+1

//push this 6
@3006
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


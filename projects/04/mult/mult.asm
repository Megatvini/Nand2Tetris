// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@res 	// multiplication result
	M=0  	// res = 0

	@i
	M=0 	//i = 0

(LOOP)
	@i
	D=M 	//D = i
	
	@R0
	D=D-M	//D = i - R0
	
	@END
	D;JGE // if (i - R0) >= 0 jump to END
	
	@R1
	D=M 	//D = R1
	
	@res
	M=M+D 	//res += R1
	
	@i
	M=M+1	//i++
	
	@LOOP
	0; JMP  //goto LOOP

(END)
	@res
	D=M     //D = res
	
	@R2
	M=D    //R2 = res
	

(INFINITE)
	@INFINITE
	0;JMP 	//Infinite LOOP

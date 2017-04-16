// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
	@pixel
	M=0		//make pixel value 0
	
	@KBD
	D=M     //D = keyboard input
	
	@NOINPUT
	D;JEQ   //if input is zero do nothing
	
	@pixel
	M=-1	//input is not zero so make pixel black
	
	(NOINPUT)
	
	@i
	M=0     //i = 0
	
	(FOR_I)
		@i
		D=M
		
		@8192
		D=D-A //D = i-8192
	
		@END_FOR_I
		D;JGE    //if (i - 8192) >= 0 end END_FOR_I
		
		@j
		M=0  //j = 0
		
		(FOR_J)
			@j
			D=M
			
			@32
			D=D-A  //D = j - 32
			
			@END_FOR_J
			D;JGE  // if (j - 32 >= 0) goto END_FOR_J
			
			@i
			D=M    //D = i
			
			@j
			D=D+M  //D = i + j
			
			@SCREEN
			D=D+A  //D = SCREEN + i + j
			
			@R0
			M=D    //R0 = D
			
			@pixel
			D=M   //D = pixel
			
			@R0
			A=M   //A = R0
			
			M=D   //SCREEN[R0] = D
			
			@j
			M=M+1 //j++
			
		@FOR_J
		0;JMP	//goto second for loop
		
		(END_FOR_J)
		
		@i
		D=M
		@32
		D=D+A	
		@i
		M=D //i = i + 32
		
	@FOR_I
	0;JMP	//goto first for loop
	
	(END_FOR_I)
	
@LOOP	//start loop again
0;JMP
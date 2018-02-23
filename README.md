# Random-walk

This is a simple implementation for random walk. 


The program reads files containing English paragraphs, one paragraph per line. The files are in a directory. 
The directory and two positive integers P, specifying the desired prefix length, and N, specifying the desired 
number of randomly generated paragraph, will be entered in the command line.

Input:
shellprompt> executable_name input_directory_name P N <enter>

Once the files have been read, the program will generate N English paragraph in the style of the input text
documents. The paragraphs are sufficiently random, including their starting phrases. They are not necessarily
grammtically right though.  

A cutoff length is chosen (100 words) so that the randomly generated paragraphs do not run out of control. 
Once N paragraphs are printed, the program reports the number of unique prefix phrases in the input text. 

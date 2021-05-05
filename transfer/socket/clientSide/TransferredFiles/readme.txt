Tested on Windows 10 

To run via CLI, either use the command line via arguments : 
g++ B18CSE020 -o exec
./exec <Value of N> <Mean value (between 0 to 1 ) > <Scheduling Technique [1,2,3,4,5] >   [eg ./exec 10 0.5 3]

To run without argumnents : 
g++ B18CSE020 -o exec
./exec

To plot, run 
python run.py
The plots would be saved with names in the folder itself

To run via shell script for cpp [For Linux]:
bash scriptCPP.sh

To run via shell script for Python [For Linux]:
bash scriptPython.sh

The table genertated would be saved as a text file separately with name "partA_generated_table.txt"
The ready queue and the current CPUs process will be printed directly upon running B18CSE020.cpp 
The queue would not be visibile upon running run.py as it would be too cumbersome, so I redirected it to STDIN for python file

I have given my best in this assignment and have tried to stress over the details, kindly let me know if there are to be any further clarifications.
# Notes from the textbook

Foundations of Coding: Compression, Encryption, Error Correction, First Edition. 
Jean-Guillaume Dumas, Jean-Louis Roch, Éric Tannier and Sébastien Varrette.

- Final error rate after corrections should be less than 10^(-15)
- Perfect Hamming codes have codewords of length 2^r-1 and encodes words of length 2^r-r-1
	- The common 7, 4 Hamming code corresponds to r=3

# MatLab

- Matlab has a hammgen function for generating hamming matrices.
- Usage: [h,g,n,k] = hammgen(3)
- https://uk.mathworks.com/help/comm/ref/hammgen.html
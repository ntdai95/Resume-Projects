// Decode prompts the user for the name of a binary (encoded) input file and
// the name to use for the output file.  It reproduces the original file.  It
// assumes that Encode was run to produce the binary file.

import java.io.*;
import java.util.*;

public class Decode {
    public static final int CHAR_MAX = 256;  // max char value to be encoded

    public static void main(String[] args) throws IOException {
        String inFile = "../" + args[0] + ".code";
        String outputFile = "../" + args[0];
        
        // open encoded file, open output, build tree, decode
        BitInputStream input = new BitInputStream(inFile);
        PrintStream output = new PrintStream(outputFile);
        HuffmanTree t = new HuffmanTree(input);
        t.decode(input, output, CHAR_MAX);
        output.close();
    }
}

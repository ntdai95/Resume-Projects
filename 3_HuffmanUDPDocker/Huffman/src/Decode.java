// Decode prompts the user for the name of a binary (encoded) input file and a
// code file name and produces as output a text file containing the original
// file.  Assumes that the binary input file was creaed by Encode.

import java.io.*;
import java.util.*;

public class Decode {
    public static final int CHAR_MAX = 256;  // max char value to be encoded

    public static void main(String[] args) throws IOException {
        System.out.println("This program decodes a file with a Huffman code.");
        System.out.println();

        Scanner console = new Scanner(System.in);
        System.out.print("encoded file name? ");
        String inFile = console.nextLine();
        System.out.print("code file name? ");
        String codeFile = console.nextLine();
        System.out.print("output file name? ");
        String outputFile = console.nextLine();
        
        // open code file and construct tree
        Scanner codeInput = new Scanner(new File(codeFile));
        HuffmanTree t = new HuffmanTree(codeInput);
            
        // open encoded file, open output, decode
        BitInputStream input = new BitInputStream(inFile);
        PrintStream output = new PrintStream(outputFile);
        t.decode(input, output, CHAR_MAX);
        output.close();
    }
}

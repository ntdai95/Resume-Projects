// This is a starter file that includes the read9/write9 methods described in
// the bonus assignment writeup.

import java.io.PrintStream;
import java.util.PriorityQueue;
import java.util.Queue;

public class HuffmanTree {
    private final HuffmanNode currentTree;

    public HuffmanTree (int[] count) {
        Queue<HuffmanNode> pQueue = new PriorityQueue<>();
        for (int i = 0; i < count.length; i++) {
            if (count[i] > 0) {
                pQueue.add(new HuffmanNode(count[i], i));
            }
        }

        // Adding eof
        pQueue.add(new HuffmanNode(1, count.length));

        while (pQueue.size() > 1) {
            HuffmanNode firstNode = pQueue.remove();
            HuffmanNode secondNode = pQueue.remove();
            // charIntVal = 0 or -1
            pQueue.add(new HuffmanNode(firstNode.getCount() + secondNode.getCount(),
                    -1, firstNode, secondNode));
        }

        this.currentTree = pQueue.remove();
    }

    public HuffmanTree (BitInputStream input) {
        this.currentTree = buildTree(input);
    }

    private HuffmanNode buildTree (BitInputStream input) {
        if (input.readBit() == 1) {
            int characterValue = read9(input);
            return new HuffmanNode(1, characterValue);
        } else {
            // for branch, there no data to store, so we put -1 as character integer value
            return new HuffmanNode(1, -1, buildTree(input), buildTree(input));
        }
    }

    public void assign (String[] codes) {
        assign(codes, this.currentTree, "");
    }

    private void assign (String[] codes, HuffmanNode currentTree, String code) {
        if (currentTree.getCharacter() != (char) -1) {
            codes[currentTree.getCharacter()] = code;
        } else{
            assign(codes, currentTree.getLeft(), code + "0");
            assign(codes, currentTree.getRight(), code + "1");
        }
    }

    public void writeHeader (BitOutputStream output) {
        writeHeader(output, this.currentTree);
    }

    private void writeHeader (BitOutputStream output, HuffmanNode currentTree) {
        if (currentTree.getCharacter() == (char) -1) {
            output.writeBit(0);
            writeHeader(output, currentTree.getLeft());
            writeHeader(output, currentTree.getRight());
        } else {
            output.writeBit(1);
            write9(output, currentTree.getCharacter());
        }
    }

    public void decode (BitInputStream input, PrintStream output, int eof) {
        int characterIntegerValue = readNextCharacterIntegerValue(input);

        while (characterIntegerValue != eof ) {
            output.write(characterIntegerValue);
            characterIntegerValue = readNextCharacterIntegerValue(input);
        }
    }

    private int readNextCharacterIntegerValue(BitInputStream input) {
        HuffmanNode currentTree = this.currentTree;
        while (currentTree.getCharacter() == (char) -1) {
            if (input.readBit() == 0) {
                currentTree = currentTree.getLeft();
            } else {
                currentTree = currentTree.getRight();
            }
        }

        return currentTree.getCharacter();
    }

    // pre : an integer n has been encoded using write9 or its equivalent
    // post: reads 9 bits to reconstruct the original integer
    private int read9 (BitInputStream input) {
        int multiplier = 1;
        int sum = 0;
        for (int i = 0; i < 9; i++) {
            sum += multiplier * input.readBit();
            multiplier = multiplier * 2;
        }
        return sum;
    }

    // pre : 0 <= n < 512
    // post: writes a 9-bit representation of n to the given output stream
    private void write9 (BitOutputStream output, int n) {
        for (int i = 0; i < 9; i++) {
            output.writeBit(n % 2);
            n = n / 2;
        }
    }


    ////////////////// Huffman Node blueprint for the Huffman tree ///////////////////

    private static class HuffmanNode implements Comparable<HuffmanNode> {
        private final int count;
        private final char character;
        private final HuffmanNode left;
        private final HuffmanNode right;

        public HuffmanNode(int count, int characterIntegerValue) {
            this(count, characterIntegerValue, null, null);
        }

        public HuffmanNode(int count, int characterIntegerValue, HuffmanNode left, HuffmanNode right) {
            this.count = count;
            this.character = (char) characterIntegerValue;
            this.left = left;
            this.right = right;
        }

        public int compareTo(HuffmanNode other) {
            return this.count - other.count;
        }

        public int getCount() {
            return count;
        }

        public char getCharacter() {
            return character;
        }

        public HuffmanNode getLeft() {
            return left;
        }

        public HuffmanNode getRight() {
            return right;
        }
    }
}

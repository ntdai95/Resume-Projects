import java.io.PrintStream;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Scanner;

public class HuffmanTree {
    private HuffmanNode currentTree;

    public HuffmanTree(int[] count) {
        Queue<HuffmanNode> pQueue = new PriorityQueue<>();
        for (int i = 0; i < count.length; i++) {
            if (count[i] > 0) {
                HuffmanNode characterLeafNode = new HuffmanNode(count[i], i);
                pQueue.add(characterLeafNode);
            }
        }

        // Adding eof
        pQueue.add(new HuffmanNode(-1, count.length));

        while (pQueue.size() > 1) {
            HuffmanNode firstNode = pQueue.remove();
            HuffmanNode secondNode = pQueue.remove();
            pQueue.add(new HuffmanNode(firstNode.getCount() + secondNode.getCount(),
                    0, firstNode, secondNode));
        }

        this.currentTree = pQueue.remove();
    }

    public HuffmanTree(Scanner input) {
        while (input.hasNextLine()) {
            int characterIntegerValue = Integer.parseInt(input.nextLine());
            String characterCode = input.nextLine();
            this.currentTree = read(this.currentTree, characterIntegerValue, characterCode);
        }
    }

    private HuffmanNode read(HuffmanNode currentTree, int characterIntegerValue, String characterCode) {
        if (characterCode.isEmpty()) {
            return new HuffmanNode(-1, characterIntegerValue);
        } else {
            if (currentTree == null) {
                currentTree = new HuffmanNode(-1, 0);
            }

            if (characterCode.charAt(0) == '0') {
                currentTree.setLeft(read(currentTree.getLeft(),
                        characterIntegerValue, characterCode.substring(1)));
            } else if (characterCode.charAt(0) == '1') {
                currentTree.setRight(read(currentTree.getRight(),
                        characterIntegerValue, characterCode.substring(1)));
            }

            return currentTree;
        }
    }

    public void write(PrintStream output) {
        this.write(output, this.currentTree, "");
    }

    private void write(PrintStream output, HuffmanNode currentTree, String characterCode) {
        if (currentTree != null) {
            if (currentTree.getLeft() == null && currentTree.getRight() == null) {
                output.println((int) currentTree.getCharacter());
                output.println(characterCode);
            }

            this.write(output, currentTree.getLeft(), characterCode + 0);
            this.write(output, currentTree.getRight(), characterCode + 1);
        }
    }

    public void decode(BitInputStream input, PrintStream output, int eof) {
        HuffmanNode currentTree = this.currentTree;
        while (true) {
            int nextBit = input.readBit();
            if (nextBit == 0) {
                currentTree = currentTree.getLeft();
            } else {
                currentTree = currentTree.getRight();
            }

            if (currentTree.getLeft() == null && currentTree.getRight() == null) {
                if (currentTree.getCharacter() == (char) eof) {
                    break;
                }
                output.write(currentTree.getCharacter());
                currentTree = this.currentTree;
            }
        }
    }
}

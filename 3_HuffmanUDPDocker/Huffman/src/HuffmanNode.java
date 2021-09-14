public class HuffmanNode implements Comparable<HuffmanNode> {
    private int count;
    private char character;
    private HuffmanNode left;
    private HuffmanNode right;

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

    public void setLeft(HuffmanNode left) {
        this.left = left;
    }

    public HuffmanNode getRight() {
        return right;
    }

    public void setRight(HuffmanNode right) {
        this.right = right;
    }
}

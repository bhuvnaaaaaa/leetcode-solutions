class Solution {
    public String reverseWords(String s) {
        String [] words = s.trim().split("\\s+");
        String [] temp = new String[words.length];


        int j = 0;
        for(int i = words.length - 1; i >= 0; i--)
        {
            temp[j] = words[i];
            j++;
        }
        return String.join(" ", temp);
    }
}

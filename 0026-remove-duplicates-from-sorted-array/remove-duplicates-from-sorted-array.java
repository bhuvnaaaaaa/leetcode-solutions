class Solution {
    public int removeDuplicates(int[] nums) {
        int j = 0;
        int k = j + 1;
        for(int i = 1; i < nums.length; i++)
        {
            if(nums[j] != nums[i])
            {
                j++;
                k++;
                nums[j] = nums[i];
            }
        }
        return k;
    }
}

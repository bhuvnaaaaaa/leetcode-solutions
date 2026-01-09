class Solution {
    public int subarraySum(int[] nums, int k) {
        Map <Integer, Integer> prefixSum = new HashMap<>();
        int res = 0;
        int currSum = 0;

        for(int i = 0; i < nums.length; i++)
        {
            currSum += nums[i];

            if(currSum == k)
            {
                res++;
            }

            if(prefixSum.containsKey(currSum - k))
            {
                res += prefixSum.get(currSum - k);
            }

            prefixSum.put(currSum, prefixSum.getOrDefault(currSum, 0) + 1);
        }
        return res;
        
    }
}

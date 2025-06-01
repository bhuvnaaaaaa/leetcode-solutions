class Solution {
    public int maxProfit(int[] prices) {
        int buy = 0;
        int sell = 1;
        int max = 0;
        while(sell < prices.length)
        {
            if(prices[buy] > prices[sell])
            {
                buy = sell;
            }
            else
            {
                max = Math.max(max, (prices[sell] - prices[buy]));
            }
            sell++;
        }
        return max;
}
}

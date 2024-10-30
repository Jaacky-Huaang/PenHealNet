def knapsack_with_items(values, weights, capacity):
    """
    Solve the 0/1 knapsack problem using dynamic programming and also return the items included in the knapsack.

    :param values: List of values of the items.
    :param weights: List of weights of the items.
    :param capacity: Maximum weight capacity of the knapsack.
    :return: Tuple (maximum value that can be carried in the knapsack, list of items included)
    """
    n = len(values)
    
    # Create a DP array where dp[i][w] is the maximum value with capacity w using the first i items.
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Build the DP table in bottom-up manner
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                # Check if including the item gives a better value
                if dp[i-1][w] < dp[i-1][w-weights[i-1]] + values[i-1]:
                    dp[i][w] = dp[i-1][w-weights[i-1]] + values[i-1]
                else:
                    dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = dp[i-1][w]
    
    # Now reconstruct the solution to find out which items to include
    items_included = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:  # Means this item is included
            items_included.append(i-1)  # Include this item (indexing starts from 0)
            w -= weights[i-1]  # Reduce the capacity by the weight of this item
    
    items_included.reverse()  # To display in the order of the input items
    
    return dp[n][capacity], items_included

# Example usage
# values = [60, 100, 120]
# weights = [10, 20, 30]
# capacity = 50
# max_value, included_items = knapsack_with_items(values, weights, capacity)
# print("Maximum value:", max_value)
# print("Items included:", included_items)



def parse_security_advice(text):
    # Split the text into sections based on the delimiter '$'
    sections = text.split('$')
    
    solutions = []
    costs = []
    values = []
    
    # Process each section
    for section in sections:
        # Trim whitespace
        section = section.strip()
        if not section:
            continue
        
        # Find the cost line and value line
        cost_line = next((line for line in section.split('\n') if 'Cost:' in line), None)
        value_line = next((line for line in section.split('\n') if 'Value:' in line), None)
        
        # Extract cost and value if lines are found
        if cost_line and value_line:
            try:
                # Extract numbers from the lines
                cost = int(cost_line.split('Cost:')[1].strip())
                value = int(value_line.split('Value:')[1].strip())
                
                # Extract the solution description
                solution = section.split('Cost:')[0].strip()
                
                # Append to lists
                solutions.append(solution)
                costs.append(cost)
                values.append(value)
            except ValueError:
                # Handle cases where conversion to int fails
                print("Error parsing numbers from:", cost_line, "or", value_line)
    
    return solutions, costs, values

with open('logs/advice.txt', 'r') as file:
    text = file.read()

solutions, costs, values = parse_security_advice(text)
# print("Solutions:", solutions)
print("Costs:", costs)
print("Values:", values)

capacity = 100
max_value, included_items = knapsack_with_items(values, costs, capacity)
print("Maximum value:", max_value)
for i in included_items:
    print("Solution:", solutions[i])
    print("Cost:", costs[i])
    print("Value:", values[i])
    print()




def group_knapsack_with_tracking(groups, capacity):
    # Initialize a list to store the maximum value at each weight capacity
    dp = [0] * (capacity + 1)
    # Initialize a list to store the chosen items for each capacity
    item_tracker = [[] for _ in range(capacity + 1)]

    # Process each group one by one
    for group in groups:
        # Temporary tracker to update during this group processing
        new_tracker = [list(items) for items in item_tracker]
        # Traverse dp array from right to left
        for j in range(capacity, -1, -1):
            max_val = dp[j]  # start with the current value at capacity j, no items taken from new group
            chosen_items = item_tracker[j]  # current items list without new group
            # Try taking each item in the current group if it fits
            for item, weight, value in group:
                if j >= weight:
                    # Calculate new value if this item is taken
                    new_val = dp[j - weight] + value
                    if new_val > max_val:
                        max_val = new_val
                        # Update the list of items chosen to achieve this max value
                        chosen_items = item_tracker[j - weight] + [item]
            # Update dp and tracker
            dp[j] = max_val
            new_tracker[j] = chosen_items
        # Update the main item tracker with the updated list from this group
        item_tracker = new_tracker

    # The maximum value and the corresponding items chosen
    return dp[capacity], item_tracker[capacity]

# Example of usage
# Define groups as tuples of (item, weight, value)
groups = [
    [("A1", 1, 100), ("A2", 3, 300), ("A3", 4, 350)],
    [("B1", 2, 200), ("B2", 3, 250)],
    [("C1", 2, 150), ("C2", 5, 750)]
]

capacity = 10
max_value, items_chosen = group_knapsack_with_tracking(groups, capacity)
print("Maximum value achievable:", max_value)
print("Items chosen:", items_chosen)


import random
import time
class Item:
    def __init__(self, value, size_sampler, label=None):
        self.value = value
        self.size_sampler = size_sampler
        self.label = label if label else f"Item({value})"
        # Estimate expected size via simulation (for ranking)
        num_samples = 10000
        self.expected_size = sum(size_sampler() for _ in range(num_samples)) / num_samples


def greedy_non_adaptive(items, capacity=1.0):
    # Sort by v / E[size], descending
    items_sorted = sorted(items, key=lambda x: x.value / x.expected_size, reverse=True)
    total_value = 0.0
    used = 0.0
    for item in items_sorted:
        s = item.size_sampler()
        if used + s <= capacity:
            used += s
            total_value += item.value
            print(f"-> Added {item.label}: size={s:.3f}, total used={used:.3f}, total value={total_value:.3f}")
        else:
            print(f"-> Tried {item.label}: size={s:.3f} → STOP (would exceed)")
            break
    return total_value


if __name__ == "__main__":
    random.seed(123)

    # Define items with distributions
    items = [
        Item(10, lambda: random.uniform(0.1, 0.3), label="A"),
        Item(8, lambda: random.betavariate(2, 5), label="B"),  # Beta ~ (0,1)
        Item(6, lambda: random.expovariate(2), label="C")  # Exponential
    ]

    print("Expected sizes (approx):")
    for it in items:
        print(f" - {it.label}: value={it.value}, E[size]={it.expected_size:.3f}, ratio={it.value / it.expected_size:.3f}")

    print("\nSimulating greedy non-adaptive packing:")
    total = greedy_non_adaptive(items, capacity=1.0)
    print(f"\nTotal value from greedy policy: {total:.3f}")

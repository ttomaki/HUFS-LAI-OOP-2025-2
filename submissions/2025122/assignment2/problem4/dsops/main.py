if __name__ == "__main__":
    from dsops import train_test_split, label_distribution

    # Demo train/test split
    tr, te = train_test_split([1, 2, 3, 4, 5], 0.4, seed=42)
    print("Train:", tr)
    print("Test:", te)

    # Demo label distribution
    labels = ["cat", "dog", "cat"]
    dist = label_distribution(labels)
    print("Label distribution:", dist)
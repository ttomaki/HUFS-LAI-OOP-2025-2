if __name__ == "__main__":
    from . import Cache, print_version_info
    print_version_info()
    c = Cache(); c.put("a", 1)
    print(len(c), c.get("a"))
    c.clear(); print(len(c))
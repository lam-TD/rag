some_list = ["a", "b", "c", "b", "d", "m", "n", "n"]

print(some_list)

my_set = set([x for x in some_list if some_list.count(x) > 1])

print(iter(my_set))


text = "test_build_messages_for_rag_with_empty_hits_max_chars"

hits = [
    {
        "text": "test_build_messages_for_rag_with_empty_hits_max_chars",
        "similarity": 0.8,
    },
    {
        "text": "test_build_messages_for_rag_with_empty_hits_max_chars",
        "similarity": 0.8,
    },
]

seen = set()

for h in hits:
    key = h.get("text")[:200]
    if key in seen:
        print(f"{key} is dupplicate")
        continue
    seen.add(key)

print(seen)

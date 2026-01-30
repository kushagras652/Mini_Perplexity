from graph.pipeline import pipeline

query = input("Enter research query: ")

state = {"query": query}
result = pipeline.invoke(state)

print("\n===== FINAL ANSWER =====\n")
print(result["answer"])

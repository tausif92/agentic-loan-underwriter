from agents.underwriting_agent import graph

# Generate mermaid text
mermaid_text = graph.get_graph().draw_mermaid()

# Save to file
with open("docs/underwriting_workflow.mmd", "w") as f:
    f.write(mermaid_text)

print("Mermaid file generated at docs/underwriting_workflow.mmd")

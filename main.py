from manufacturingagents.graph.trading_graph import TradingAgentsGraph
from manufacturingagents.default_config import DEFAULT_CONFIG

# Create a custom config for manufacturing use case
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "google"  # Use a different model
config["backend_url"] = "https://generativelanguage.googleapis.com/v1"  # Use a different backend
config["deep_think_llm"] = "gemini-2.0-flash"  # Use a different model
config["quick_think_llm"] = "gemini-2.0-flash"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds
config["online_tools"] = True  # Enable online tools

# Initialize manufacturing decision system
ma = TradingAgentsGraph(debug=True, config=config)

# Example: Analyze replenishment decision for a manufacturing product
# In actual implementation, this would be adapted for manufacturing data
_, decision = ma.propagate("PRODUCT_001", "2024-05-10")
print("Manufacturing Decision:", decision)

# Reflect and optimize decision process
# ma.reflect_and_remember(1000) # parameter is the performance metrics

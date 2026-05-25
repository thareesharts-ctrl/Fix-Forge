from services.deepseek_service import ask_deepseek

# Maintain backward compatibility for all modules referencing ask_qwen
ask_qwen = ask_deepseek
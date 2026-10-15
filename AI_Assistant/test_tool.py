from tool import get_current_date_time, get_roll_dice, get_generate_password
from tool_manager import execute_tool_function

print("Current Date and Time:", execute_tool_function("get_current_date_time"))
print("Roll of the dice:", execute_tool_function("get_roll_dice"))
print("Generated Password:", execute_tool_function("get_generate_password"))
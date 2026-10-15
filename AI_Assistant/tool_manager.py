from tool import get_current_date_time, get_roll_dice, get_generate_password

def execute_tool_function(user_input):
    """
    Executes a tool function based on the provided tool name and arguments.
    
    Parameters:
        tool_name (str): The name of the tool function to execute.
        *args: Arguments to pass to the tool function.
    """
    text = user_input.strip().lower() 

    if "time" in text or "date" in text or "current" in text or "now" in text or "what is the time" in text:
        return get_current_date_time()
    elif "roll" in text and "dice" in text:
        return get_roll_dice()
    elif "generate" in text and "password" in text:
        return get_generate_password(12)
    else:
        return None
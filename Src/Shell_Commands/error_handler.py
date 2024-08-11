import time 
import random 

"""Honey on Honey"""


def Error(): 
    """Just Error"""
    error_messages = [
            f"SyntaxError!",
            f"Error: Invalid command "
        ]
    return random.choice(error_messages) + "\n"

def Permission_Denied(filename):
    """You are not allowed here!"""
    
    return f"-sh: {filename}: Permission denied\n"

def Wget_error(url):
    """No no, can't download here!"""
    errors = [
        f"wget: error getting file: {random.choice(['Connection timed out', 'Could not resolve host', 'Protocol error'])}",
        f"wget: error getting file: {random.choice(['File size exceeds limit', 'Invalid URL'])}",
        f"wget: {random.choice(['Cannot open', 'No such file'])}: {url}",
    ]
    return random.choice(errors) + "\n"

def Python_Interactive_Error():
        """Yeah your script is problem!!!"""
        fake_messages = [
            f"Traceback (most recent call last):\r\n  File \"<stdin>\", line {random.randint(1,10)}, in <module>\r\n",
            f"  File \"<stdin>\", line {random.randint(1,10)} \r\n    ^\r\nSyntaxError: invalid syntax",
            f"TypeError: unsupported operand type(s)\r\n"
        ]
        return random.choice(fake_messages)

def Delay(self):
    """It's Delay time"""
    message = "Required to reset host for applying changes. Reload in 10 seconds...\r\n"
    for char in message:
        self.write_output(char,end='',flush=True)
        time.sleep(0.05)
        
    for _ in range(7):
        for dots in ["." * i for i in range(1, 4)]:
            self.write_output(f"\r{dots}", end="", flush=True)
            time.sleep(0.5)
        self.write_output("\r\033[K", end="", flush=True)
        time.sleep(0.3)
        
    self.write_output("\rDone...")


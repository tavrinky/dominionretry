import string 
import random 
def random_string(n): 
    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
    
class Triggered: 
    def __init__(self): 
        self.triggered = False 

    def trigger(self): 
        self.triggered = True 
import time
from typing import Optional


def animate_text(empty, text: str, 
                 time_per_letter: Optional[float] = None, 
                 time_per_sentence: Optional[float] = None) -> None:
    if time_per_letter and time_per_sentence:
        raise Exception("Either time_per_letter or time_per_sentence has to be define.")
    
    if time_per_letter:
        sleep_time = time_per_letter
    elif time_per_sentence:
        sleep_time = time_per_sentence / len(text)
    else:
        raise Exception("Either time_per_letter or time_per_sentence has to be define.")
    
    empty.empty()
    with empty:
        for i in range(len(text)):
            time.sleep(sleep_time)
            empty.write(text[:i+1])

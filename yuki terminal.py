import pygame
import subprocess
import os
import getpass
import re
from pygame.locals import *

ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')

def main():
    pygame.init()

    # Window setup
    window_width = 900
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("yuki terminal (still working on it)")

    # font
    try:
        font = pygame.font.Font("/usr/share/fonts/J//home/polar/Downloads/JetBrains Mono Bold Italic Nerd Font Complete Mono.ttf", 30)  # Path to monospaced font
    except:
        font = pygame.font.SysFont("/home/polar/Downloads/JetBrains Mono Bold Italic Nerd Font Complete Mono.ttf", 30)

    text_color = (255, 255, 255) 
    background_color = (0, 0, 0)  

    user_name = getpass.getuser()
    host_name = os.uname()[1]
    prompt = f"{user_name}@{host_name}:~$ "

    input_text = ""
    output_text = []
    scroll_offset = 0
    scroll_speed = 25

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                
                    command = input_text.strip()

                    if command.lower() == "clear":
                        
                        output_text = []
                    elif command.lower() == "exit":
                       
                        running = False
                    elif command:
                        
                        output_text.append(prompt + command)  
                        execute_and_display_command(command, output_text)  

                    input_text = ""  
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]  
                elif event.key == K_ESCAPE:
                    running = False  
                elif event.key == K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
                elif event.key == K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, len(output_text) * scroll_speed)
                else:
                    input_text += event.unicode  
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == 1:  # scroll up
                    scroll_offset = max(scroll_offset - scroll_speed, 0)
                elif event.y == -1:  # scroll down
                    scroll_offset = min(scroll_offset + scroll_speed, len(output_text) * scroll_speed)

        
        window.fill(background_color)

        
        input_surface = font.render(prompt + input_text, True, text_color)
        input_y_pos = window_height - 40  
        window.blit(input_surface, (10, input_y_pos))

       
        y_offset = input_y_pos - 25 - scroll_offset
        for line in reversed(output_text):
            if y_offset + 25 > 0:
                text_surface = font.render(line, True, text_color)
                window.blit(text_surface, (10, y_offset))
            y_offset -= 25

        pygame.display.flip()  

    pygame.quit()

def execute_and_display_command(command, output_text):
    try:
       
        result = subprocess.run(f"bash -c '{command}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout + result.stderr

       
        clean_output = ansi_escape.sub('', output)

        # Add the command output to the output text buffer
        output_lines = clean_output.splitlines()
        output_text.extend(output_lines)
    except Exception as e:
        output_text.append(f"Error: {e}")

if __name__ == "__main__":
    main()

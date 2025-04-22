#  nuitka_build.py
#  Copyright (c) TotallyNotSeth 2025
#  All rights reserved.

# Builtin imports
import sys
import os
from pathlib import Path

# Package imports
import pygame
from pygame.locals import QUIT
from loguru import logger

# Local imports
from ttwhy.util import ensure_iverilog
from ttwhy.character import BLINK
from ttwhy.terminal import Terminal
from ttwhy.color import *


# TERM_WIDTH = 100
# TERM_HEIGHT = 32
FPS = 165
BLINK_EVENT = pygame.event.custom_type()


def main():
    logger.add(Path(os.getenv('LOCALAPPDATA')) / "TotallyNotSeth" / "HDLGame" / "hdlgame_{time}.log",
               level="DEBUG", retention="7 days", backtrace=True, diagnose=True)

    logger.info("HDLGame")
    logger.info("Copyright (c) TotallyNotSeth 2025\n")

    # logger.debug("Ensuring Icarus Verilog is installed")
    # try:
    #     ensure_iverilog.ensure_iverilog()
    # except ensure_iverilog.InstallError:
    #     logger.exception("Failed to install Icarus Verilog")
    #     sys.exit(1)

    logger.debug("Pygame v{version} Init", version=pygame.ver)
    pygame.init()
    pygame.font.init()
    pygame.key.set_repeat(500, 50)
    clock = pygame.time.Clock()

    logger.debug("Pygame Display Init")
    screen = pygame.display.set_mode()
    pygame.mouse.set_visible(False)

    logger.debug("Terminal Init")
    font = pygame.font.Font(Path(__file__).parent / "MxPlus_IBM_VGA_8x16.ttf", 32)
    term_width = screen.get_width() // font.size(" ")[0]
    term_height = screen.get_height() // font.size(" ")[1]
    terminal = Terminal(screen, term_width, term_height, font)
    terminal.print("ChipperOS")
    # terminal.grid[1][2].style = BLINK
    terminal.print("Type \"help\" for a list of commands")
    terminal.print("")
    terminal.print("> █")

    logger.debug("Blink Event ID: {id}", id=BLINK_EVENT)

    last_mouse_pos: tuple[int, int] = (0, 0)
    current_mouse_pos: tuple[int, int]
    show_fps: bool = False
    frame_count: int = 0

    # Game Loop
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                logger.info("Exiting HDLGame (OS request)...")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    logger.info("Exiting HDLGame (ESC key pressed)...")
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F2:
                    show_fps = not show_fps
                else:
                    terminal.process_input_key(event)

        # Update
        terminal.clear()
        # terminal.draw_str(" Hello, World! ", (1, 1), WHITE, RED)
        # terminal.draw_box((25, 5), 30, 10, CYAN, BLACK, DoubleBoxDrawingCharacters)
        terminal.draw_text_buffer()
        if show_fps:
            counter = f" FPS: {clock.get_fps():.2f} "
            terminal.draw_str(counter, (term_width - len(counter), 0), WHITE, BLUE)
            # terminal.print(counter)

        current_mouse_pos = terminal.surface_pos_to_char_pos(pygame.mouse.get_pos())
        terminal.set_color_at_char(last_mouse_pos, BLACK, BLACK)
        terminal.set_color_at_char(current_mouse_pos, BLACK, WHITE)
        last_mouse_pos = current_mouse_pos

        # Draw
        terminal.render(frame_count)
        frame_count += 1
        if frame_count >= FPS:
            frame_count = 0

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

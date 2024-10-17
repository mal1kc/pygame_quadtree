import asyncio
import pygame
from quadtree import create_quadtree_from_QuadtreeFlag, get_example_quadtreeflag

_ = pygame.init()

pygame.display.set_caption("quadtree")
scr_size = (1200, 900)
screen = pygame.display.set_mode(scr_size)


async def main():
    example_quad_tree = create_quadtree_from_QuadtreeFlag(
        screen, get_example_quadtreeflag(), pygame.Vector2(0, 0)
    )

    running = True
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        _ = screen.fill((0, 0, 0))

        # Draw the quadtree
        example_quad_tree.draw(pygame.Color(0, 100, 255), screen)

        # Update the display
        pygame.display.update()

        await asyncio.sleep(0)

        # running = False # check draw result  of single frame
        # Control the frame rate
        _ = clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()


asyncio.run(main())

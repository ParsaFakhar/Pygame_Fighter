import pygame


def load_frames(sheet: pygame.Surface, size: int, scale: int, frames_per: list[int]) -> list[list[pygame.Surface]]:
    """
    Generic tilesheet loader: for each row (i.e. an animation),
    grab `frames_per[row]` frames of size `size` and scale them up.
    Returns a list of frame-lists.
    """
    animation: list[list[pygame.Surface]] = []
    for row, count in enumerate(frames_per):
        row_frames: list[pygame.Surface] = []
        for i in range(count):
            sub = sheet.subsurface(pygame.Rect(i * size, row * size, size, size))
            row_frames.append(pygame.transform.scale(sub, (size * scale, size * scale)))
        animation.append(row_frames)
    return animation

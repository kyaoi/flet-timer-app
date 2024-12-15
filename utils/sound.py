import pygame


class Sound:
    def __init__(self):
        pygame.mixer.init()

    def play_alarm_sound(self) -> None:
        pygame.mixer.music.load("sound.wav")
        pygame.mixer.music.play(-1)

    def stop_alarm_sound(self) -> None:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

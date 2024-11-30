import pygame


class Sound:
    def __init__(self):
        pygame.mixer.init()

    def play_alarm_sound(self):
        pygame.mixer.music.load("sound.wav")
        print("Playing alarm sound...")
        pygame.mixer.music.play(-1)

    def stop_alarm_sound(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print("Alarm sound stopped.")

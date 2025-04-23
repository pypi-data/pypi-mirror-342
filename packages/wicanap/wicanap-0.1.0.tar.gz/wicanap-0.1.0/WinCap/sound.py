import os
import winsound
import threading

class SoundManager:
    def play(self, file, volume=100, repeat=0):
        if not os.path.isfile(file):
            print(f"Файл {file} не найден.")
            return

        def _play():
            if repeat is True:
                while True:
                    winsound.PlaySound(file, winsound.SND_FILENAME)
            else:
                for _ in range(repeat + 1):
                    winsound.PlaySound(file, winsound.SND_FILENAME)

        threading.Thread(target=_play, daemon=True).start()

sound = SoundManager()

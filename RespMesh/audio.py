from AudioRec import Recorder
import time
import os

class AudioHendler:
	def record(self):
                        os.remove('./media/test.mp3')
                        os.remove('./media/test.wav')
                        rec = Recorder(chunk=512, channels=1, rate=5500)
                        rec.start()
                        time.sleep(5)
                        rec.stop()
                        rec.save("./media/test.wav")
                        os.system("ffmpeg -i \"./media/test.wav\" \"./media/test.mp3\"")


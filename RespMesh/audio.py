from AudioRec import Recorder
import time
import os

class AudioHendler:
	def record(self):
                        os.remove('/home/dor/Desktop/ArmsMesh/RespMesh/media/test.mp3')
                        os.remove('/home/dor/Desktop/ArmsMesh/RespMesh/media/test.wav')
                        rec = Recorder(chunk=512, channels=1, rate=5500)
                        rec.start()
                        time.sleep(5)
                        rec.stop()
                        rec.save("/home/dor/Desktop/ArmsMesh/RespMesh/media/test.wav")
                        os.system("ffmpeg -i \"/home/dor/Desktop/ArmsMesh/RespMesh/media/test.wav\" \"/home/dor/Desktop/ArmsMesh/RespMesh/media/test.mp3\"")


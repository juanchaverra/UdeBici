import androidhelper as android
from datetime import datetime

app = android.Android()
app.cameraInteractiveCapturePicture('/home/PycharmProjects/{}.jpeg'.format(str(datetime.now())))

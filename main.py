from kivy.lang import Builder
from kivymd.app import MDApp

from jnius import autoclass, cast

from PIL import Image

from android import activity, mActivity
from android.permissions import request_permissions, Permission
from android.storage import primary_external_storage_path
request_permissions([Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE])

from kivy.logger import Logger
from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'log_dir', 'logs')
Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')
Config.set('kivy', 'log_enable', 1)
Config.write()
Logger.debug("DEBUG: primary_external_storage_path")
Logger.debug("DEBUG: %s", primary_external_storage_path())

Intent = autoclass('android.content.Intent')
MediaStore = autoclass('android.provider.MediaStore')
Environment = autoclass('android.os.Environment')
Context = autoclass("android.content.Context")
FileProvider = autoclass('android.support.v4.content.FileProvider')
PythonActivity = autoclass("org.kivy.android.PythonActivity").mActivity

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file('scanneRx.kv')
    
    def take_picture(self):
        def create_img_file():
            File = autoclass('java.io.File')
            storageDir = Context.getExternalFilesDir(Environment.DIRECTORY_PICTURES)

            imageFile = File(
                storageDir,
                "temp.jpg"
            )
            imageFile.createNewFile()
            return imageFile

        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)

        photoFile = create_img_file()
        photoUri = FileProvider.getUriForFile(
            Context.getApplicationContext(),
            "org.test.takepicture.fileprovider",
            photoFile
        )

        parcelable = cast('android.os.Parcelable', photoUri)

        intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)
        mActivity.startActivityForResult(intent, 0x123)

    def on_pause(self):
        return True

MainApp().run()

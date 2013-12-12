from mediacrush.processing.processor import Processor

copy = "cp {0} {1}.{extension}"

class VideoProcessor(Processor):
    time = 300
    outputs = ['mp4', 'webm', 'ogv']
    extras = ['png']

    def sync(self):
        self._execute(copy)
        self._execute("ffmpeg -i {0} -vframes 1 -map 0:v:0 {1}.png")
        self._execute("ffmpeg -i {0} -vcodec libx264 -pix_fmt yuv420p -vf scale=trunc(in_w/2)*2:trunc(in_h/2)*2 -map 0:a:0 -map 0:v:0 {1}.mp4")
        self._execute("ffmpeg -i {0} -c:v libvpx -c:a libvorbis -pix_fmt yuv420p -quality good -b:v 2M -crf 5 -map 0:a:0 -map 0:v:0 {1}.webm")

    def async(self):
        self._execute("ffmpeg -i {0} -q 5 -pix_fmt yuv420p -acodec libvorbis -vcodec libtheora -map 0:a:0 -map 0:v:0 {1}.ogv")

class AudioProcessor(Processor):
    time = 300
    outputs = ['mp3', 'ogg']

    def sync(self):
        self._execute(copy)
        self._execute("ffmpeg -i {0} {1}.mp3")

    def async(self):
        self._execute("ffmpeg -i {0} -acodec libvorbis {1}.ogg")

class ImageProcessor(Processor):
    time = 60
    outputs = ['png']

    def sync(self):
        self._execute(copy)
        self._execute("convert {0} {1}.png")

# We have some special optimizations for specific filetypes
# These customized processors follow

class PNGProcessor(Processor):
    time = 120
    outputs = ['png']

    def sync(self):
        self._execute(copy)

    def async(self):
        self._execute("optipng -o5 {1}")

class JPEGProcessor(Processor):
    time = 5
    outputs = []

    def sync(self):
        self._execute("jhead -purejpg {0}")
        self._execute(copy)

class SVGProcessor(Processor):
    time = 5
    outputs = []

    def sync(self):
        self._execute("tidy -asxml -xml --hide-comments 1 --wrap 0 --quiet --write-back 1 {0}")
        self._execute(copy)

class DefaultProcessor(Processor):
    time = 5

    def sync(self):
        self._execute(copy)

processor_table = {
    'video': VideoProcessor,
    'audio': AudioProcessor,
    'image': ImageProcessor,
    'image/jpeg': JPEGProcessor,
    'image/svg+xml': SVGProcessor,
    'default': DefaultProcessor,
}

def get_processor(processor):
    return processor_table.get(processor, DefaultProcessor)

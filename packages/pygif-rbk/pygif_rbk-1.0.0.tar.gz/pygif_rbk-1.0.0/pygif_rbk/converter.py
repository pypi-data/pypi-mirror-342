import glob
from PIL import Image


class GifConverter:
    def __init__(self, path_in=None, path_out=None, resize=(320, 240)):
        """
        path_in: original image source location (ex: images/*.png)
        path_out: result image location (ex: output/filename.gif)
        resize: (width, height)
        """
        self.path_in = path_in or './*.png'
        self.path_out = path_out or './output.gif'
        self.resize = resize
        
    def convert_gif(self):
        """
        GIF image converter
        """
        print(self.path_in, self.path_out, self.resize)
        
        img, *images = \
            [Image.open(f).resize(self.resize, Image.Resampling.LANCZOS) for f in sorted(glob.glob(self.path_in))]
            
        try:            
            img.save(
                fp=self.path_out,
                format='GIF',
                append_images=images,
                save_all=True,
                duration=500,
                loop=0,
                disposal=2
            )
        except IOError:
            print("Cannot convert!", img)



if __name__ == "__main__":
    # Class
    c = GifConverter('./project/images/*.png', './project/image_out/result1.gif', (320, 240))
    
    # Convert
    c.convert_gif()
import cairo
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 100, 100)
surface.write_to_png("test.png")
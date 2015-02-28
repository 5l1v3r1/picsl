import sys
import colorsys
from PIL import Image

BLOCKLEN = 1
COLORS = {}
COLORS["red"] = 0
COLORS["green"] = 1
COLORS["blue"] = 2

def color_average(pixels, block):
    """ 
    Gets the color average of the given block coordinates in an image.

    Returns a tuple (r, g, b) representing the average color
    """

    x1, y1, _, _ = block
    p = [pixels[x+x1,y+y1] for x in xrange(BLOCKLEN) for y in xrange(BLOCKLEN)]

    rgb_sum = lambda a, b: (a[0] + b[0], a[1] + b[1], a[2] + b[2])
    rgb_total = reduce(rgb_sum, p)

    div = lambda x: (x / (BLOCKLEN ** 2))
    rgb = map(div, rgb_total)

    return tuple(rgb)

def chunk(l, n):
    """ 
    Returns a list of n-sized slices of l 
    """

    result = []
    app = result.append

    for i in xrange(0, len(l), n):
        app(l[i:i+n])

    return result

def get_blockmap(xblock, yblock):
    """
    Constructs a list of blocks from the number of block segments for x and y.

    Returns a list of blocks where a block is (x1, y1, x2, y2) for 
    top right and bottom left corners, respectively.
    """
    return [(xb*BLOCKLEN, yb*BLOCKLEN, (xb+1)*BLOCKLEN, (yb+1)*BLOCKLEN)
            for xb in xrange(xblock) for yb in xrange(yblock)]      

def get_block_colors(blockmap, pixels):
    """
    Gets the color average for each block in the given blockmap.

    Returns a list of the averages as RGB tuples.
    """
    c_avg = lambda b: color_average(pixels, b)
    return map(c_avg, blockmap)

def sort_by(p, color):
    """ 
    Sorts
    """
    return sorted(p, key=lambda t: t[0][COLORS[color]])

def main(argv):

    filename = argv[0]
    img = Image.open(filename)
    width, height = img.size

    xblock = width / BLOCKLEN
    yblock = height / BLOCKLEN

    print "Building blockmap"
    blockmap = get_blockmap(xblock, yblock)

    print "Loading pixels"
    pixels = img.load()

    print "Color averaging"
    rgb_vals = get_block_colors(blockmap, pixels)

    # pair with blockmap indices
    pairs = zip(rgb_vals, range(len(blockmap)))

    pairs = sort_by(pairs, "red")
    chunks = chunk(pairs, yblock)

    sort_all_by_blue = lambda x: sort_by(x, "green")

    chunks = map(sort_all_by_blue, chunks)
    sorted_blockmap = [blockmap[item[1]] for c in chunks for item in c]

    # form result
    result = Image.new(img.mode, (width, height))

    for box, sbox in zip(blockmap, sorted_blockmap):
        c = img.crop(sbox)
        result.paste(c, box)

    print "saving"
    result.save(argv[1])

if __name__ == "__main__":
    main(sys.argv[1:])
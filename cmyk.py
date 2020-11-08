import os
from PIL import Image, ImageCms

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
ICC_PATH = os.path.join(THIS_FOLDER, 'icc')

def Extract( folder, client_id, ext):

    fp = folder + '/' + client_id
    img = Image.open( fp + "_s" + ext)

    # Available via https://www.adobe.com/support/downloads/iccprofiles/iccprofiles_win.html
    rgb_icc = os.path.join(ICC_PATH, 'AppleRGB.icc')
    cmyk_icc = os.path.join(ICC_PATH, 'USWebCoatedSWOP.icc')

    im = ImageCms.profileToProfile(img, rgb_icc, cmyk_icc, renderingIntent=0, outputMode='CMYK')
    source = im.split()

    print("Extracting")
    # create blank image and split the layers
    blank = Image.new("CMYK", im.size, (0,0,0,0))
    b_split = blank.split()

    # add the separate layers to the k layer
    c_out = Image.merge("CMYK",(b_split[0], b_split[1], b_split[2], source[0]))
    m_out = Image.merge("CMYK",(b_split[0], b_split[1], b_split[2], source[1]))
    y_out = Image.merge("CMYK",(b_split[0], b_split[1], b_split[2], source[2]))
    k_out = Image.merge("CMYK",(b_split[0], b_split[1], b_split[2], source[3]))

    out = Image.merge("CMYK",(source[0],  source[1], source[2], source[3]))

    # Colour versions
    c_out_rgb = ImageCms.profileToProfile(c_out, cmyk_icc, rgb_icc, renderingIntent=0, outputMode='RGB')
    c_out_rgb.save(fp + '_c.jpg','PNG',optimize=False)

    m_out_rgb = ImageCms.profileToProfile(m_out, cmyk_icc, rgb_icc, renderingIntent=0, outputMode='RGB')
    m_out_rgb.save(fp + '_m.jpg','PNG',optimize=False)

    y_out_rgb = ImageCms.profileToProfile(y_out, cmyk_icc, rgb_icc, renderingIntent=0, outputMode='RGB')
    y_out_rgb.save(fp + '_y.jpg','PNG',optimize=False)

    k_out_rgb = ImageCms.profileToProfile(k_out, cmyk_icc, rgb_icc, renderingIntent=0, outputMode='RGB')
    k_out_rgb.save(fp + '_k.jpg','PNG',optimize=False)

if (__name__ == '__main__'):
    print("This was the one thing we didn't want to happen")


from PIL import Image, ImageCms

def Extract( folder, client_id, ext):
    
    fp = folder + '/' + client_id
    img = Image.open( fp + "_s" + ext)

    # Available via https://www.adobe.com/support/downloads/iccprofiles/iccprofiles_win.html
    rgb_icc = "icc/AppleRGB.icc"
    cmyk_icc = "icc/USWebCoatedSWOP.icc"

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
    c_out.save(fp + '_c.jpg')
    m_out.save(fp + '_m.jpg')
    y_out.save(fp + '_y.jpg')
    k_out.save(fp + '_k.jpg')


if (__name__ == '__main__'):
    print("This was the one thing we didn't want to happen")


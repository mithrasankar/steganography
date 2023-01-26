from bakery import assert_equal
#from tkinter import filedialog
#from tkinter import *
from PIL import Image
import string
#Mithra Sankar -- Honors CISC108 Final Project
#############################################################
"""
NOTA BENE: Do not change the names, parameters, or return types of these functions.
They must stay the same to pass our tests.
NOTA BENE SECUNDUS: You have already written variations of these functions. Use 
your work!
"""
"""
TO USE:
Call encode(msg, image) on a secret message file and an image filename
The new image (a .png file) has the secret message hidden inside (steganography!).
Call decode(image) to see the secret message again. 
Encoding preserves A-Z and '\n. ,?'
"""
"""
TO START:
Identify low-level functions that can be written and tested without calling other 
functions. Write and test these first (comment out the other tests). Then look for 
reciprocal functions that you can write and test against each other (see tests 
provided). As you write tests and gain understanding about a function, feel free to
add to its comments!
"""
"""
REQUIRED:
For each function, write at least THREE additional good tests. Your tests should 
not rely on external files -- create files in code when needed (see tests 
provided). Look for boundary conditions not already being tested. Use the best 
coding style we have learned in class, it will be graded.
"""
#############################################################
TEST = True
"""Please don't alter the next three lines"""
char_codes_strip = {'\n':91,'.':92,' ':93,',':94,'?':96} #strip out underscore
charCodesEncode = { **char_codes_strip, '_':95} #allow underscore for encoding, decoding
inverseCharCodes = {value:key for key,value in charCodesEncode.items() } #use when decoding
"""
Read image
Get pixel array
Get message (from file or input)
Strip message
Prepare message x
Walk pixels, inserting chars
Save image as .png
___
Get filename
Open image
Get pixels
Walk pixels and get message
 message
return message
"""
def decode(image_file_name):
    """
    Open image, get chars from image 
    Call select_msg_output to allow user to choose what to do with message
    Also calls , get_msg_from_image.  No automated tests for this function.
    """
    image1 = Image.open(image_file_name)
    message = restore_msg(get_message_from_image(image1))
    choice = select_msg_output(message)
    return choice

#
def select_msg_output(msg):
    """
    Ask user whether to print (p), save (s), or return (default) message, then 
perform. Should be able to handle input with leading or trailing whitespace. No 
automated tests for this function.
    """
    user_input = input("Select whether to print (type 'p'), save ('s'), or return ('default')")
    if user_input.strip() == 'p':
        print(msg)
    if user_input.strip() == 's':
        file = open('decoded.txt','w')
        file.write(msg)
        file.close()
    else:
        return (msg)
#    
def restore_msg(str):
    """
    Replace underscores with spaces; trim trailing characters off the end.
    """
    str = str.strip()
    for character in str:
        if character == "_":
            str = str.replace(character," ")
    return str

#        
#
def get_msg_from_image(image1):
    """
    Go through pixels in the image and extract chars until the message
    is finished. Calls get_char_from_color.  Only process pixels until
    the end of the message. If message is not properly terminated, print an error 
message.
    """
    im = image1.copy()
    pixels = im.load()
    height = im.height
    width = im.width
    message = ""
    underscore = 0
    for y in range(height):
        for x in range(width):
            char = get_char_from_color(pixels[x,y])
            if char == "_":
                underscore = underscore + 1
                if underscore == 3:
                    return(message)
            else:
                underscore = 0
            message = message + char
    return("Error: improper msg")
#
def encode(message_file_name, image_file_name):
    """
    Gets the message and prepares it for encoding #get_message_from_file
    Gets the image information and opens it, copies it #compare
    Checks that image is big enough to hold message, prints error message if not
    Put every char from message into image #put_all_chars_in_image
    Save resulting image with new name (get_new_file_name())
    return new image
    """
    message = prepare_message(strip_message(get_message_from_file(message_file_name)))
    image1 = Image.open(image_file_name)
    image_size = image1.size[0] * image1.size[1]
    if len(message) > image_size:
        print("Error: the message is too long!")
    image1 = image1.copy()
    image1 = put_all_chars_in_image(image1,message)
    image1.save(get_new_file_name(image_file_name))
    return image1
#
def get_new_file_name(old):
    """
    Change the old file name to end with '.encoded.png'
    e.g. 'spam.png' -> 'spam.encoded.png' OR 'spam.jpeg' -> 'spam.encoded.png'
    """
    for index, value in enumerate(old):
        if value == ".":
            old = old.replace(old[index:],".encoded.png")
    return old
    assert_equal(get_new_file_name("spam.png"), "spam.encoded.png")
    assert_equal(get_new_file_name("spam.jpeg"), "spam.encoded.png")
    assert_equal(get_new_file_name("spamjpeg"), "spamjpeg")
    assert_equal(get_new_file_name(""), "")
    assert_equal(get_new_file_name("mithra.png"), "mithra.encoded.png")

def put_all_chars_in_image(image1, msg):
    """
    Takes an opened image and a fully processed message
    Encodes the message into the image, one char to each pixel 
(put_one_char_in_colors())
    Returns the image
    """
    input_img = image1.copy()
    pixels = input_img.load()
    height = input_img.height
    width = input_img.width
    index = 0
    for y in range (height):
        for x in range(width):
            if index < len(msg):
                color = put_one_char_in_colors(pixels[x,y],msg[index])
            elif index < len(msg) + 3:
                color = put_one_char_in_colors(pixels[x,y],"_")
            else:
                color = pixels[x,y]
            index = index + 1
            pixels[x,y] = color
    return input_img
   
def get_message_from_file(message_file_name):
    msg = None
    with open(message_file_name, 'r') as infile:
        msg = infile.read()
    return msg


def strip_message(strIn):
    """
    Returns a string with all unacceptable chars removed. 
    May only look at each char in the input string once. USE THE STRIP DICTIONARY 
PROVIDED AT TOP.
    Acceptable characters: AZaz\n. ,?
    """
    new = strIn
    for character in strIn:
        if character not in string.ascii_lowercase:
            if character not in string.ascii_uppercase:
                if character not in char_codes_strip:
                    new = new.replace(character,"")
    return new

def prepare_message(input_string):
    """
    Convert parameter string to upper case and replace any spaces with underscores.
Any occurrence of consecutive spaces should be replaced with a single underscore 
(CALL THE FUNCTION YOU WROTE). Add a sequence of three underscores to the end of 
the message '___'.
    https://docs.python.org/3/library/stdtypes.html#textseq
    """
    single_space = input_string.replace("  ", " ")
    while single_space != input_string:
        input_string = single_space
        single_space = input_string.replace("  ", " ")
    input_string = input_string.replace(" ", "_")
    input_string += "___"
    return input_string.upper()

def put_one_char_in_colors(color, char):
    """
    Get ASCII value of uppercase character (for special characters use 
charCodesEncode), change to A=0 base. Then convert 2 digit base 10 to base 6. Put 
first digit of into last digit of G, and second into last digit of B.  
assert_equal( put_one_char_in_colors(color1, 'Z'), (255, 254, 251))
    color  -- RGB triple
    char   -- ASCII char
    return -- color 3-tuple with char hidden inside
    """
    char_codes_strip = {'\n':91,'.':92,' ':93,',':94,'?':96} #strip out underscore
    charCodesEncode = { **char_codes_strip, '_':95} #allow underscore for encoding, decoding
    green = color[1]
    blue = color[2]
    if char in charCodesEncode:
        num = charCodesEncode[char]-65
    else:
        num = ord(char)-65
    green = 10*(green//10) + num // 6 
    blue = 10*(blue//10) + num % 6
    return (color[0], green, blue)

def get_char_from_color(color):
    """
    Get two digits from color 3-tuple, translate to base 10, add 65, convert to char. 
    Use inverseCharCodes.
    """
    green = color[1]
    blue = color[2]
    first_num = (green % 10)* 6
    second_num = blue % 10
    number = second_num + first_num + 65
    if number > 90:
        return(inverseCharCodes.get(number))
    else:
        return(chr(number))
    for i in range(0,256,5):
        color = (i,i,i)
        for c in charCodesEncode:
            color = put_one_char_in_colors(color, c)
            assert_equal(get_char_from_color(color), c)
        for c in 'AZ':
            color = put_one_char_in_colors(color, c)
            assert_equal(get_char_from_color(color), c)
getchar = (122,81,44)
getchar2 = (255, 254, 251)
getchar3 = (255, 255, 250)
assert_equal(get_char_from_color(getchar), "K")
assert_equal(get_char_from_color(getchar2), "Z")
assert_equal(get_char_from_color(getchar3), "_")

if TEST:
    assert_equal(strip_message('AaZz\n. ,?'),'AaZz\n. ,?')
    assert_equal(strip_message('2190!@#$-=+<>;":_'),'')
    assert_equal(prepare_message("I once had a dog"),"I_ONCE_HAD_A_DOG___")
    assert_equal(prepare_message("I  once    had   a       dog"),"I_ONCE_HAD_A_DOG___")
    assert_equal(prepare_message("I  once    had\n   a       dog"),"I_ONCE_HAD\n_A_DOG___")
    #Jackson
    assert_equal(prepare_message('This should be line 1\n this should be line 2'),'THIS_SHOULD_BE_LINE_1\n_THIS_SHOULD_BE_LINE_2___')
    assert_equal(prepare_message("She  was  a   dog."),"SHE_WAS_A_DOG.___")
    assert_equal(prepare_message(" "),"____")
    assert_equal(prepare_message("Mithra does NOT haVe a dog."),"MITHRA_DOES_NOT_HAVE_A_DOG.___")
    

    color1 = (255,255,255)
    assert_equal(put_one_char_in_colors(color1, 'A'), (255, 250, 250))
    assert_equal(put_one_char_in_colors(color1, '?'), (255, 255, 251) )
    assert_equal(put_one_char_in_colors(color1, 'Z'), (255, 254, 251))
    assert_equal(put_one_char_in_colors(color1, '_'), (255, 255, 250))
    assert_equal(put_one_char_in_colors(color1, ':'), (255, 248, 255))
    assert_equal(put_one_char_in_colors(color1, '%'), (255, 245, 252))
    assert_equal(put_one_char_in_colors(color1, ')'), (255, 246, 250))

    for  i in range(0,256,5):
        color = (i,i,i)
        for c in charCodesEncode:
            color = put_one_char_in_colors(color, c)
            assert_equal(get_char_from_color(color), c)
        
        for c in 'AZ':
            color = put_one_char_in_colors(color, c)
            assert_equal(get_char_from_color(color), c)
        
    assert_equal(strip_message("Hey!"),"Hey")
    assert_equal(strip_message("Test: 'quote?'"),"Test quote?")
    assert_equal(strip_message("This should all work."),"This should all work.")
    assert_equal(strip_message("Un@ccept@ble Str!ng"),"Uncceptble Strng")
    assert_equal(strip_message(""),"")
    assert_equal(strip_message("Mithra"),"Mithra")
    assert_equal(strip_message("l\n#"),"l\n")
    assert_equal(strip_message("TEST\n!"),"TEST\n")
    
    def compare(im1, im2):
        if im1.size != im2.size:
            return False
        else:
            p1 = im1.load()
            p2 = im2.load()
            for r in range(im1.size[1]):
                for c in range(im1.size[0]):
                    if p1[c,r] != p2[c,r]:
                        return False
        return True
    
    image0 = Image.new('RGB', (2,1), (0,0,0))
    image0 = put_all_chars_in_image(image0, "AZ")
    pixels0 = image0.load()
    assert_equal(pixels0[0,0], (0,0,0))
    assert_equal(pixels0[1,0], (0,4,1))
    
    image0 = Image.new('RGB', (3,2), (0,0,0))
    image1 = image0.copy()
    image1 = put_all_chars_in_image(image1, "AZ?___")
    pixels0 = image0.load()
    pixels0[0,0] = (0,0,0)
    pixels0[1,0] = (0,4,1)
    pixels0[2,0] = (0,5,1)
    pixels0[0,1] = (0,5,0)
    pixels0[1,1] = (0,5,0)
    pixels0[2,1] = (0,5,0)
    assert_equal(compare(image0, image1), True)
    
    image0 = Image.new('RGB', (3,2), (0,0,0))
    image0.save('temp.png')
    with open('msg.txt', 'w') as ofile:
        ofile.write("AZ?___")
    new_im1 = encode('msg.txt', 'temp.png')
    pixels0 = image0.load()
    pixels0[0,0] = (0,0,0)
    pixels0[1,0] = (0,4,1)
    pixels0[2,0] = (0,5,1)
    pixels0[0,1] = (0,5,0)
    pixels0[1,1] = (0,5,0)
    pixels0[2,1] = (0,5,0)
    assert_equal(compare(image0, new_im1), True)
    
    image0 = Image.new('RGB', (6,1), (0,0,0))
    image0.save('temp.png')
    with open('msg.txt', 'w') as ofile:
        ofile.write("AZ?___")
    new_im2 = encode('msg.txt', 'temp.png')
    pixels0 = image0.load()
    pixels0[0,0] = (0,0,0)
    pixels0[1,0] = (0,4,1)
    pixels0[2,0] = (0,5,1)
    pixels0[3,0] = (0,5,0)
    pixels0[4,0] = (0,5,0)
    pixels0[5,0] = (0,5,0)
    assert_equal(compare(image0, new_im2), True)
    assert_equal(restore_msg(get_msg_from_image(new_im2)), 'AZ?')
    assert_equal(restore_msg(get_msg_from_image(new_im1)), 'AZ?')
    assert_equal(restore_msg("Hello_World   "), "Hello World")
    assert_equal(restore_msg("1_2_3_4_5"), "1 2 3 4 5")
    assert_equal(restore_msg(""), "")
    assert_equal(restore_msg("Computer_Science_Lecture"), "Computer Science Lecture")
    
    image0 = Image.new('RGB', (500,500), (0,0,0))
    image0.save('temp4.png')
    with open('msg4.txt', 'w') as ofile:
        ofile.write("A" * (500 * 500 -3))
        ofile.write('___')
    new_im4 = encode('msg4.txt', 'temp4.png')
    assert_equal(restore_msg(get_msg_from_image( new_im4)), 'A' * (250000 - 3))
encode("jane.txt","fourSquid.png")
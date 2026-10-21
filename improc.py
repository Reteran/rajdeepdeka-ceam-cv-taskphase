import copy

image = []
# setting image
with open("grayscale.txt") as f:
    for line in f:
        image.append([int(n) for n in line.split(',')])

# PGM filereader
pgmimage = []
width = 0
height = 0
max = 0
filename = "casablanca"
with open(f'pgm-files/{filename}.pgm') as f:
    c = 0
    single_list = []
    for line in f:
        if c == 1:
            width = int(line.split(' ')[0])
            height = int(line.split(' ')[1])
        if c == 2:
            max = int(line.split(' ')[0])
        if c >= 3:
            for x in [int(n.strip()) for n in line.split(' ') if n.strip()]: # remember: if n.strip() checks if n.strip() is truthy, as '' (empty char) is considered equivalent to false when evaluated with if
                single_list.append(x)
            # pgmimage.append([int(n) for n in line.split(' ') if n != ''])
        if '\n' in line:
            c+=1
    
    wcount = 0
    row = []
    for x in single_list:
        wcount+=1
        row.append(x)
        if wcount == width:
            pgmimage.append(row)
            row = []
            wcount = 0

# for x in pgmimage:
#     for y in x: print(y, end=' ')
#     print()

# print(width)
# print(height)
# print(max)

def writepgm(img, filename):
    with open(f'{filename}.pgm', "w") as f:
        f.write(f'P2\n')
        f.write(f'{width} {height}\n')
        f.write(f'{max}\n')
        for x in img:
            f.write(" ".join([f'{int(round(c)) }' for c in x]) + "\n")

def change_brightness(img, option):
    if option == 2:
        for row in img:
            for n in range(len(row)):
                row[n] += 5
                if row[n] > 255: row[n] = 255
        
        # print("image with increased brightness:")
        # for row in image:
            # for px in row: print(px, end="\t")
            # print()
    elif option == 1:
        for row in img:
            for n in range(len(row)):
                row[n] -= 5
                if row[n] < 0: row[n] = 0
        
        # print("image with decreased brightness:")
        # for row in image:
            # for px in row: print(px, end="\t")
            # print()
    else:
        print("invalid option, enter either 0 or 1")

def threshold(img, tvalue):
    for row in img:
        for n in range(len(row)):
            row[n] = 255 if row[n] >= tvalue else 0

def invert():
    for row in img:
        for n in range(len(row)):
            row[n] = 255-row[n]

def flip(img, option):
    l = len(img)
    match option:
        case 'H' | 'h':
            for r in img:
                lr = len(r)
                for p in range(int(lr/2)):
                    temp = r[p]
                    r[p] = r[lr-p-1]
                    r[lr-p-1] = temp
        case 'V' | 'v':
            for n in range(int(len(img)/2)):
                temp = img[n]
                img[n] = img[l-n-1]
                img[l-n-1] = temp
        case _:
            print("invalid choice for flip")

def rotate(img):
    print("0 for counter-clockwise\n1 for clockwise")
    c = int(input())
    # transpose the matrix first
    for r in range(len(img)):
        for n in range(r, len(img[r])):
            temp = img[r][n]
            img[r][n] = img[n][r]
            img[n][r] = temp
    match c:
        case 0:
            flip(img, 'v')
        case 1:
            flip(img, 'h')
        case _:
            print("invalid choice for rotate")

    return img

def apply_pad(img, n):
    pad = int((n-1)/2)
    pad_img = []

    for i in range(pad):
        row = []
        for j in range(2*pad + len(img[0])):
            row.append(0)
        pad_img.append(row)

    for i in range(len(img)):
        row = []
        for j in range(pad):
            row.append(0)

        for j in img[i]:
            row.append(j)
        
        for j in range(pad):
            row.append(0)

        pad_img.append(row)

    for i in range(pad):
        row = []
        for j in range(2*pad + len(img[0])):
            row.append(0)
        pad_img.append(row)

    return pad_img


def blur(img, n):
    if(n%2==0):
        print("\n\n!! Enter an odd number for the kernel size !!")
        return -1

    kernel = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(1/(n*n))
        kernel.append(row)

    pad_img = apply_pad(img, n)

    print("\n")
    blurred = []
    for r in range(len(pad_img) - n + 1):
        row = []
        for p in range(len(pad_img[r]) - n + 1):
            sum = 0
            for y in range(n):
                for x in range(n):
                    sum += kernel[y][x] * pad_img[r+y][p+x]
                    #print(sum)
            row.append(sum)
        blurred.append(row)

    writepgm(blurred, "blur_output")
    return blurred

def edge(img, n):
    kernel =   [[-1/4, 2/4, 1/4],
                [-2/4, 0, 2/4],
                [-1/4, -2/4, 1/4]]

    pad_img = apply_pad(img, n)
    edges = []
    for r in range(len(pad_img) - n + 1):
        row = []
        for p in range(len(pad_img[r]) - n + 1):
            sum = 0
            for y in range(n):
                for x in range(n):
                    sum += kernel[y][x] * pad_img[r+y][p+x]
                    #print(sum)
            row.append(sum)
        edges.append(row)

    with open("edge_output.pgm", "w") as f:
        f.write(f'P2\n')
        f.write(f'{width} {height}\n')
        f.write(f'{max}\n')
        for x in edges:
            f.write(" ".join([f'{abs(int(round(c)))}' for c in x]) + "\n")

    return edges


ogimage = copy.deepcopy(image)
while True:
    # debugging
    # print("original image:")
    # for row in ogimage:
    #     for px in row: print(px, end="\t")
    #     print()  

    
    print("Current Image:")
    for row in image:
        for px in row: print(px, end="\t")
        print()

    print("Enter:")
    print("0\tReset to original image")
    print("1\tDecrease Brightness")
    print("2\tIncrease Brightness")
    print("3\tThreshold image")
    print("4\tFlip image")
    print("5\tRotate image")
    print("6\tBlur image")
    print("7\tDetect Edges")
    choice = int(input())
    
    match choice:
        case -1:
            break
        case 0:
            image = copy.deepcopy(ogimage)
        case 1 | 2:
            change_brightness(image, choice)
        case 3:
            print("Enter the threshold value:", end=' ')
            value = int(input())
            threshold(image, value)
        case 4:
            print("\nH for horizontal flip\nV for vertical flip")
            c = input()
            flip(image, c)
        case 5:
            rotate(image)
        case 6:
            print("Enter the kernel size (odd numbers only):")
            c = int(input())
            blur(pgmimage, c)
        case 7:
            edge(pgmimage, 3)
        case _:
            print("invalid choice")
    
    print("\n\n\n")
    
# resources:
# 
# https://docs.python.org/3/library/copy.html
# https://www.cs.rhodes.edu/~kirlinp/courses/cs1/f19/projects/proj8/
# https://www.w3schools.com/python/python_match.asp
# https://towardsdatascience.com/computer-vision-convolution-basics-2d0ae3b79346/
# https://youtu.be/KuXjwB4LzSA (3b1b convolutions video)
# https://cse19-iiith.vlabs.ac.in/exp/neighbourhood-operations/theory.html
# https://people.sc.fsu.edu/~jburkardt/data/pgma/pgma.html
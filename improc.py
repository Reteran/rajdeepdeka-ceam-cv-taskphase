import copy

image = []
# setting image
with open("grayscale.txt") as f:
    for line in f:
        image.append([int(n) for n in line.split(',')])
        
pgmimage = []
with open("feep.pgm") as f:
    c = 0
    for line in f:
        if c >= 3:
            pgmimage.append([int(n) for n in line.split(' ') if n != ''])
        if '\n' in line:
            c+=1
for x in pgmimage:
    print(x)

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

def threshold(tvalue):
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

def rotate():
    print("0 for counter-clockwise\n1 for clockwise")
    c = int(input())
    # transpose the matrix first
    for r in range(len(image)):
        for n in range(r, len(image[r])):
            temp = image[r][n]
            image[r][n] = image[n][r]
            image[n][r] = temp
    match c:
        case 0:
            flip('v')
        case 1:
            flip('h')
        case _:
            print("invalid choice for rotate")

def blur(img, n):
    if(n%2==0):
        print("Enter an odd number for the kernel size")
        return _

    kernel = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(1/(n*n))
        kernel.append(row)

    pad = int((n-1)/2)
    pad_image = []

    for i in range(pad):
        row = []
        for j in range(2*pad + len(img[0])):
            row.append(0)
        pad_image.append(row)

    for i in range(len(img)):
        row = []
        for j in range(pad):
            row.append(0)

        for n in img[i]:
            row.append(n)
        
        for j in range(pad):
            row.append(0)

        pad_image.append(row)

    for i in range(pad):
        row = []
        for j in range(2*pad + len(img[0])):
            row.append(0)
        pad_image.append(row)

    for x in pad_image:
        for y in x: print(y, end=' ')
        print()

    print("\n")
    blurred = []
    for r in range(len(pad_image) - n):
        row = []
        for p in range(len(pad_image[r]) - n):
            sum = 0
            for y in range(n):
                for x in range(n):
                    sum += kernel[y][x] * pad_image[p+y][r+x]
            row.append(sum)
        blurred.append(row)

    for x in blurred:
        for y in x: print(y, end=' ')
        print()
        



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
            threshold(value)
        case 4:
            print("\nH for horizontal flip\nV for vertical flip")
            c = input()
            flip(image, c)
        case 5:
            rotate()
        case 6:
            print("Enter the kernel size (odd numbers only):")
            c = int(input())
            blur(pgmimage, c)
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
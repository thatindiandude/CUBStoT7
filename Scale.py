''' Estimates bounding boxes of bird parts
    given coordinates. Python prototype.
    To be placed at same level as parts/.
    Note: bird parts are described in parts/parts.txt.
    Use:
        python BirdBox.py 0 test0.bb
    to write bounding boxes for image 0 into `test0.bb`
'''

def intersect(*boxes):
    return tuple(m(b[2*i+axis] for b in boxes) for i,m in enumerate((max,min)) for axis in range(2))
def join(*boxes):
    return tuple(m(b[2*i+axis] for b in boxes) for i,m in enumerate((min,max)) for axis in range(2))

from math import sqrt
distance = lambda a,b: sqrt(sum((aa-bb)**2 for aa,bb in zip(a,b)))
def makebox(center, height, width):
    x,y = center
    return (x-width/2,y-height/2,x+width/2,y+height/2)
def guess_bounding_boxes(bounding_box, keypoints, scale=0.3):
    ''' Estimates bounding boxes of bird parts
        given coordinates. Inputs:
           `keypoints`, a length-15 list of (y,x) tuples each
           representing the hand-keyed center of a bird part.
           `bounding_box`, a (min_y, min_x, max_y, max_x) tuple
           representing a hand-keyed bounding box for the whole bird.
    '''
    x,y,X,Y = bounding_box
    height, width = (Y-y)*scale, (X-x)*scale
    return [makebox(p, height, width) if sum(p) else (0,0,0,0) for p in keypoints]

import sys
tocoor = lambda line: tuple(float(w) for w in line if w)
tostring = lambda box: ' '.join(str(c) for c in box)
if __name__=='__main__':
    imageid=int(sys.argv[1]); bounding_boxes_name=sys.argv[2]
    with open('bounding_boxes.txt') as f:
        x,y,w,h = tocoor(f.read().split('\n')[imageid].split()[1:])
        bounding_box = y,x,y+h,x+w
    with open('parts/part_locs.txt') as f:
        keypoints = [tocoor(line.split()[2:4])[::-1] for line in f.read().split('\n')[15*imageid:15*(imageid+1)]]
    bounding_boxes = guess_bounding_boxes(bounding_box, keypoints)
    with open(bounding_boxes_name,'w') as f:
        f.write('\n'.join(tostring(box) for box in bounding_boxes))

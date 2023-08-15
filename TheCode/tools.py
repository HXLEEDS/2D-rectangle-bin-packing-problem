
from matplotlib.pyplot import axis
import numpy as np

def Horizontal_Lines_Intersect(line1,line2):
    #In the first case, line1 is completely to the left of line2
    if line1[2]<=line2[0]:
        flag=0
        HD=line1[1]-line2[1]
    #In the second case, line1 is to the left of line2
    elif (line1[2]>line2[0]) and (line1[2]<=line2[0]):
        flag=1
        HD=line1[1]-line2[1]
    #In the third case, line1 is to the right of line2
    elif (line1[0]>=line2[0]) and (line1[0]<line2[2]):
        flag=1
        HD=line1[1]-line2[1]
    #In the fourth case, line1 is completely to the right of line2
    elif line1[0]>=line2[2]:
        flag=0
        HD=line1[1]-line2[1]
    #In the fifth case, line1 completely contains line2
    else:
        flag=1
        HD=line1[1]-line2[1]
    return flag,HD

######################################

def Point_Horizontal_Line(item,RPXY):
    RBPXY=[RPXY[0],RPXY[1]-item[1]]#  Coordinates of the vertex in the lower right corner of the item
    LBPXY=[RPXY[0]-item[0],RPXY[1]-item[1]]  #Coordinates of the vertex in the lower left corner of the item
    bottomLine=[]
    bottomLine.extend(LBPXY)
    bottomLine.extend(RBPXY)
    return bottomLine


def downHAtPoint(item,AllItem,itemRP,RPNXY):
    bottomLine=Point_Horizontal_Line(item,itemRP)  #Coordinates of the left and right ends of the horizontal line segment at the lower end of the object[leftx,lefty,rightx,righty]
    RP_NUM=len(RPNXY) #Number of items in the bin
    if RP_NUM!=0:
        sRPNXY=np.array(sorted(list(RPNXY), key=lambda x:x[2],reverse=True))#Sort RPNXY in descending order by Y-coordinate.
        sRBPNXY=sRPNXY.copy()
        sRBPNXY[:,1]=sRPNXY[:,1]-AllItem[sRPNXY[:,0],0]  #The coordinates of the top-left vertex of RPNXY in descending order of the Y-coordinates.
        
        topLine=np.concatenate((sRBPNXY[:,1:3],sRPNXY[:,1:3]),axis=1)  #Coordinates of the left and right ends of the horizontal line segment at the top of the item [leftx,lefty,rightx,righty] after the items are sorted in descending order according to the Y-coordinate.
        # Iterate through the items in sRPNXY one by one
        alldownH=[]  # Store all descending distances that satisfy the intersection condition
        for i in range(RP_NUM):
            
            flag,HD=Horizontal_Lines_Intersect(bottomLine,topLine[i,:])
            if (flag==1) and (HD>=0):
                alldownH.append(HD)
        # If there are no items that satisfy the intersection condition
        if len(alldownH)==0:
            downH=itemRP[1]-item[1]
        else:  # If there are items that satisfy the intersection condition
            downH=min(alldownH)
    else:
        downH=itemRP[1]-item[1]  
    return downH

def Vertical_Lines_Intersect(line1,line2):
    # In the first case, line1 is completely above line2
    if line1[3]>=line2[1]:
        flag=0
        HD=line1[0]-line2[0]
    # In the second case, line1 is above line2
    elif (line1[3]<line2[1])and (line1[3]>=line2[3]):
        flag=1
        HD=line1[0]-line2[0]
    # In the third case, line1 is below line2
    elif (line1[1]<=line2[1]) and (line1[1]>line2[3]):
        flag=1
        HD=line1[0]-line2[0]
    # In the fourth case, line1 is completely below line2
    elif line1[1]<=line2[3]:
        flag=0
        HD=line1[0]-line2[0]
    else:
        flag=1
        HD=line1[0]-line2[0]
    return flag,HD


def Point_Vertical_Line(item,RPXY):
    LUPXY=[RPXY[0]-item[0],RPXY[1]]  #Coordinates of the top-left vertex of the item
    LBPXY=[RPXY[0]-item[0],RPXY[1]-item[1]] #Coordinates of the vertex in the lower left corner of the item
    leftLine=[]
    leftLine.extend(LUPXY)
    leftLine.extend(LBPXY)
    return leftLine


def leftWAtPoint(item,Item,itemRP,RPNXY):
    leftLine=Point_Vertical_Line(item,itemRP)  #Coordinates of the top and bottom of the vertical segment at the left end of the object
    RP_NUM=len(RPNXY)
    if RP_NUM!=0:
        sRPNXY=np.array(sorted(list(RPNXY), key=lambda x:x[0]))  # Sort RPNXY in descending order by X-coordinate
        sRBPNXY=sRPNXY.copy()
        sRBPNXY[:,2]=sRPNXY[:,2]-Item[sRPNXY[:,0],1] #The coordinates of the lower right vertex of RPNXY after sorting it in descending order by the X coordinate.
        rightLine=np.concatenate((sRPNXY[:,1:3],sRBPNXY[:,1:3]),axis=1)#The coordinates of the top and bottom of the right-hand end of the line segment after the items have been sorted in descending order by X-coordinate
        
        allLeftW=[]  #Store all left shift distances that satisfy the intersection condition
        for i in range(RP_NUM):
            flag,HD=Vertical_Lines_Intersect(leftLine,rightLine[i,:])
            if (flag==1) and (HD>=0):
                allLeftW.append(HD)
        if len(allLeftW)==0:
            leftW=itemRP[0]-item[0]
        else:
            leftW=min(allLeftW)
    else:
        leftW=itemRP[0]-item[0]
    return leftW


def Update_itemRP(itemRP,downH,leftW):
    h=itemRP[1]-downH  #y coordinates
    w=itemRP[0]-leftW   #x coordinates
    return [w,h]

class Rectangle:
    def __init__(self, x, y,w,h):
      self.x = x
      self.y = y
      self.width = w
      self.height = h

def finalPos(item,Item,itemRP,RPNXY):
    while 1:
        downH=downHAtPoint(item,Item,itemRP,RPNXY) #Calculate the maximum height that the item item can fall at the itemRP position inside the box.
        leftW=0
        itemRP=Update_itemRP(itemRP,downH,leftW) #Update the coordinates of the top-right corner of the item item's current position.
        downH=0
        leftW=leftWAtPoint(item,Item,itemRP,RPNXY) #Calculate the maximum distance the item can be moved to the left at the itemRP position inside the box.
        itemRP=Update_itemRP(itemRP,downH,leftW) #Update the coordinates of the top-right corner of the item item's current position.
        if (downH==0)and (leftW==0):
            finalRP=itemRP
            break
    return finalRP


def overlap(item,Item,itemRP,RPNXY):
    flagOL=0  
    itemLBP=[itemRP[0]-item[0],itemRP[1]-item[1]] #Coordinates of the vertex in the lower left corner
    A = Rectangle(itemLBP[0],itemLBP[1],item[0],item[1])
    num=len(RPNXY)
    if num>0:
        for i in range(num):
            width=Item[RPNXY[i][0],0]  #Item(RPNXY(i,1),:)width
            height=Item[RPNXY[i][0],1]  #Item(RPNXY(i,1),:) Height
            LBPXY=[RPNXY[i][1]-width,RPNXY[i][2]-height]  #Coordinates of the lower-left corner vertex of the current rectangular Item(RPNXY(i,1),:) in the bin
            B = Rectangle(LBPXY[0],LBPXY[1],width,height)
            area=rectint(A,B)#Calculate the intersection area
            #If AB intersects, the following relationship is satisfied
            if area>0:
                flagOL=1
                break
    return flagOL

def rectint(rect1, rect2):
    xl1, yb1, xr1, yt1 = rect1.x,rect1.y,rect1.x+rect1.width,rect1.y+rect1.height # (xl1, yb1) are the coordinates of the lower left corner of the rectangle and (xr1, yt1) are the coordinates of the upper right corner.
    xl2, yb2, xr2, yt2 = rect2.x,rect2.y,rect2.x+rect2.width,rect2.y+rect2.height 
    xmin = max(xl1, xl2)
    ymin = max(yb1, yb2)
    xmax = min(xr1, xr2)
    ymax = min(yt1, yt2)
    width = xmax - xmin
    height = ymax - ymin
    if width <= 0 or height <= 0:
        return 0
    cross_square = width * height
    return cross_square
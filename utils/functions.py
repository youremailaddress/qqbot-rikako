import os

def EditDist(a,b):
    m,n = len(a)+1,len(b)+1
    d = [[0]*n for i in range(m)]
    d[0][0]=0
    for i in range(1,m):
        d[i][0] = d[i-1][0] + 1
    for j in range(1,n):
        d[0][j] = d[0][j-1]+1
    temp = 0
    for i in range(1,m):
        for j in range(1,n):
            if a[i-1]==b[j-1]:
                temp = 0
            else:
                temp = 1
            d[i][j]=min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+temp)
    return d[m-1][n-1]

def baseDir():
    return os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0],os.path.pardir))

def getDir(path):
    return os.path.abspath(os.path.join(baseDir(),path))
#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import random
import pygame
import maze
# 
pygame.init()  # 初始化pygame
size = width, height = 800, 600  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
# 颜色
diamond_color_size = 12
COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_BLACK, COLOR_FLAXEN, COLOR_GOLD, COLOR_GRAY, COLOR_PINK, COLOR_ORANGE, COLOR_WHEAT, COLOR_CYAN = list(range(
    diamond_color_size))
COLOR = {
    COLOR_RED: (255, 0, 0), # 红
    COLOR_BLUE: (0, 0, 255), # 蓝
    COLOR_GREEN: (0, 255, 0), # 绿
    COLOR_YELLOW: (255, 255, 0), # 黄
    COLOR_BLACK: (0, 0, 0), # 黑
    COLOR_FLAXEN: (250, 240, 230), # 亚麻
    COLOR_GOLD : (255,215,0), # 金
    COLOR_GRAY: (128,128,128), # 灰
    COLOR_PINK:(255,192,203), # 粉
    COLOR_ORANGE: (255,165,0),# 橙
    COLOR_WHEAT: (245,222,179),# 小麦
    COLOR_CYAN : (0,255,255), # 青
}
# 格子大小
DIAMOND_LEN = 20
DIAMOND_SIZE = (DIAMOND_LEN, DIAMOND_LEN)
# 各色的格子
DIAMONDS=[]
for x in range(diamond_color_size):
    diamoand=pygame.surface.Surface(DIAMOND_SIZE).convert()
    diamoand.fill(COLOR[x])
    DIAMONDS.append(diamoand)

DIAMONDS=[]
for x in range(diamond_color_size):
    diamoand=pygame.surface.Surface(DIAMOND_SIZE).convert()
    diamoand.fill(COLOR[x])
    DIAMONDS.append(diamoand)


# 字体
use_font = pygame.font.Font("simsunb.TTF", 16)
use_font12 = pygame.font.Font("simsunb.TTF", 12)
# 背景
background=pygame.surface.Surface(size).convert()
background.fill(COLOR[COLOR_BLACK])
# 文字
score_surface = use_font.render("找到终点", True, COLOR[COLOR_BLACK], COLOR[COLOR_FLAXEN])
# 时间
clock = pygame.time.Clock()
#标记 
NOWALL=maze.NOWALL # 无墙
WALL=maze.WALL  # 有墙
WALL2=maze.WALL2  # 有墙
VISIT=maze.VISIT # 到访过
NOVISIT=maze.NOVISIT # 没到过
VERTICAL = maze.VERTICAL # 垂直的
HORIZONTAL = maze.HORIZONTAL# 水平的
INFINITE = maze.INFINITE # 无穷远

def DrawCircle(screen,  position, color, pure=False, radius=6, width=6):
    if pure:
        pygame.draw.circle(screen, color, position, radius, width)
    else:
        pygame.draw.circle(screen, color, position, radius-3, 3)
        pygame.draw.circle(screen, COLOR[COLOR_RED], position, radius-2, 1)
        pygame.draw.circle(screen, COLOR[COLOR_GREEN], position, radius-1, 1)
        pygame.draw.circle(screen, COLOR[COLOR_BLUE], position, radius, 1)
    #pygame.draw.circle(screen, color, position, radius, 1)
    #pygame.draw.circle(screen, color, position, radius, 1)
    #pygame.draw.circle(screen, color, position, radius, 1)

# 下一圈
def FindNextCircle(startList, walls, grids, rows, cols):
    startNextList = [] # 下一步
    for node in startList:
        r, c = node
        l = grids[r][c]
        # 可以到达的位置
        if r>0 and NOWALL == walls[r][c][1] and INFINITE == grids[r-1][c]:
            # move = 'u'
            nr=r-1
            nc=c
            if (nr,nc) not in startNextList:
                startNextList.append((nr,nc))
                grids[nr][nc] = l+1
        if c>0 and NOWALL == walls[r][c][0] and INFINITE == grids[r][c-1]:
            # move = 'l'
            nr=r
            nc=c-1
            if (nr,nc) not in startNextList:
                startNextList.append((nr,nc))
                grids[nr][nc] = l+1
        if c<cols-1 and NOWALL == walls[r][c+1][0] and INFINITE == grids[r][c+1] :
            # move='r'
            nr=r
            nc=c+1
            if (nr,nc) not in startNextList:
                startNextList.append((nr,nc))
                grids[nr][nc] = l+1
        if r<rows-1 and NOWALL == walls[r+1][c][1] and INFINITE == grids[r+1][c] :
            # move='d'
            nr=r+1
            nc=c
            if (nr,nc) not in startNextList:
                startNextList.append((nr,nc))
                grids[nr][nc] = l+1
    # 下一圈
    startList.clear()
    startList.extend(startNextList)
    return startList

def sample_findmainpath_step(r, c, mainList, walls, grids, rows, cols):
    # 演示生成最短路径过程
    findMainPath = False
    mainList.append((r,c))
    l = grids[r][c]
    nl=l-1
    # 最近的
    if r>0 and NOWALL == walls[r][c][1] and nl == grids[r-1][c]:
        # move = 'u'
        nr=r-1
        nc=c
    elif c>0 and NOWALL == walls[r][c][0] and nl == grids[r][c-1]:
        # move = 'l'
        nr=r
        nc=c-1
    elif c<cols-1 and NOWALL == walls[r][c+1][0] and nl == grids[r][c+1] :
        # move='r'
        nr=r
        nc=c+1
    elif r<rows-1 and NOWALL == walls[r+1][c][1] and nl == grids[r+1][c] :
        # move='d'
        nr=r+1
        nc=c
    # 找到起点
    if 0 == nl:
        mainList.append((nr,nc))
        findMainPath = True
    r,c=nr,nc
    return r,c, findMainPath

def sample_findpathing_step(startList, walls, grids, rows, cols, treasures):
    # 演示寻路过程
    # 初始化未访问
    findPath = False
    startNextList = [] # 下一步
    for node in startList:
        r, c = node
        l = grids[r][c]
        ln=l+1
        if node in treasures:
            findPath = True
            startList.clear()
            break
        # 可以到达的位置
        if r>0 and NOWALL == walls[r][c][1] and INFINITE == grids[r-1][c]:
            # move = 'u'
            nr=r-1
            nc=c
            if (nr,nc) not in startNextList:
                startNextList.append((nr,nc))
                grids[nr][nc] = ln
        if c>0 and NOWALL == walls[r][c][0] and INFINITE == grids[r][c-1]:
            # move = 'l'
            nr=r
            nc=c-1
            if (nr,nc) not in startNextList:
                startNextList.append((nr,nc))
                grids[nr][nc] = ln
        if c<cols-1 and NOWALL == walls[r][c+1][0] and INFINITE == grids[r][c+1] :
            # move='r'
            nr=r
            nc=c+1
            if (nr,nc) not in startNextList:
                startNextList.append((nr,nc))
                grids[nr][nc] = ln
        if r<rows-1 and NOWALL == walls[r+1][c][1] and INFINITE == grids[r+1][c] :
            # move='d'
            nr=r+1
            nc=c
            if (nr,nc) not in startNextList:
                startNextList.append((nr,nc))
                grids[nr][nc] = ln
    # 下一圈
    startList.clear()
    startList.extend(startNextList)
    return findPath, r, c

# 画方块
def draw_diamond(r, c, screen, diamod):
    px,py= 1 + (c) * DIAMOND_SIZE[0], 1 + (r) * DIAMOND_SIZE[1]
    screen.blit(diamod, (px, py))
    return 


# 画方块和字符串string
def draw_diamond_and_str(r, c, screen, diamod, use_font, string, color, color_back):
    px,py= 1 + (c) * DIAMOND_SIZE[0], 1 + (r) * DIAMOND_SIZE[1]
    screen.blit(diamod, (px, py))
    distance_surface = use_font.render(string, True, color, color_back)
    screen.blit(distance_surface, (px, py))
    return 


# Sample algorithm
def multipath_maze_demo(rows, cols):
    maze_h = rows * DIAMOND_SIZE[0] + 1
    maze_w = cols * DIAMOND_SIZE[0] + 1
    size = (maze_w, maze_h)
    # 迷宫图层
    maze_surface=pygame.surface.Surface(size).convert()
    #walls = maze.aldous_broder_maze(rows, cols)
    #walls = maze.depth_maze(rows, cols)
    #walls = maze.kruskal_maze(rows, cols)
    #walls = maze.prim_maze(rows, cols)
    #walls = maze.wilson_maze(rows, cols)
    walls = maze.wilson_maze(rows, cols)
    # 画
    posion_xy=(40, 40)
    # 初始化未访问
    grids=[[ INFINITE for i in range(cols)]for j in range(rows)]
    # 起点
    # 标记迷宫
    r=0
    c=0
    startPoint=(r,c)  # 起点
    endPoint=(rows-1,cols-1)  # 终点
    # 拆出多条路
    def down_wall_maze(walls, rows, cols, startPoint, endPoint):
        maze.down_wall_maze(walls, rows, cols, startPoint, endPoint)
        maze.down_wall_maze(walls, rows, cols, startPoint, endPoint)
    # 随机N个宝箱
    n=6
    treasures=[]   
    tmpTreasures=[] 
    while n > 0:
        r = random.randint(0, rows-1)
        c = random.randint(0, cols-1)
        if (r,c) not in treasures and (r,c) != startPoint and (r,c) != endPoint:
            treasures.append((r,c))
            tmpTreasures.append((r,c))
            n -=1
    # 
    mainList=[] # 主路径
    # 标记
    findEndPoint=False
    findPath=False
    findTreasures=None
    findMainPath=None
    # 
    startList=[startPoint]
    grids[startPoint[0]][startPoint[1]]=0 # 标记已经到过格子距离   
    startMap=[]
    startMap += startList
    # 
    parts = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if not findPath:
            # 寻路过程
            if tmpTreasures:  # 找宝箱
                findPath, r, c = sample_findpathing_step(startList, walls, grids, rows, cols, tmpTreasures)
                # treasures.remove((r, c))
                treasurePoint=(r,c)
            else:  # 找终点
                findPath, r, c = sample_findpathing_step(startList, walls, grids, rows, cols, [endPoint])
        elif not findMainPath:
            # 回溯路径
            r, c, findMainPath = sample_findmainpath_step(r, c, mainList, walls, grids, rows, cols)
            # 
            if findMainPath:
                # 宝箱已经找全部找到
                if not tmpTreasures:
                    findEndPoint = True
        else:
            if not findEndPoint:
                grids=[[ INFINITE for i in range(cols)]for j in range(rows)]
                startMap=[]
                if tmpTreasures:
                    tmpTreasures.remove(treasurePoint)
                    findPath = False
                    findMainPath = False
                    startList=[treasurePoint]
                    grids[treasurePoint[0]][treasurePoint[1]]=0 # 标记已经到过格子距离   
                    startMap += startList
        # 背景
        screen.blit(background, (0, 0))
        # maze_surface
        # 格子
        for cx in range(cols):
            for ry in range(rows):
                # 标记访问过的格子
                if maze.INFINITE == grids[ry][cx]:
                    draw_diamond(ry, cx, maze_surface, DIAMONDS[COLOR_GRAY])
                else:
                    s = "{}".format(grids[ry][cx])
                    draw_diamond_and_str(ry, cx, maze_surface, DIAMONDS[COLOR_WHEAT], use_font12, s, COLOR[COLOR_BLACK], COLOR[COLOR_WHEAT]) 
        # 圈地
        for pos in startMap:
            s = "{}".format(grids[pos[0]][pos[1]])
            draw_diamond_and_str(pos[0], pos[1], maze_surface, DIAMONDS[COLOR_WHEAT], use_font12, s, COLOR[COLOR_BLACK], COLOR[COLOR_WHEAT])
        # 循环外圈
        if startList and not mainList:
            for pos in startList:
                s = "{}".format(grids[pos[0]][pos[1]])
                draw_diamond_and_str(pos[0], pos[1], maze_surface, DIAMONDS[COLOR_RED], use_font12, s, COLOR[COLOR_BLACK], COLOR[COLOR_RED])
        # 路径
        if mainList:
            for pos in mainList:
                s = "{}".format(grids[pos[0]][pos[1]])
                draw_diamond_and_str(pos[0], pos[1], maze_surface, DIAMONDS[COLOR_YELLOW], use_font12, s, COLOR[COLOR_BLACK], COLOR[COLOR_YELLOW])
            # r,c
            s = "{}".format(grids[pos[0]][pos[1]])
            draw_diamond_and_str(r, c, maze_surface, DIAMONDS[COLOR_GREEN], use_font12, s, COLOR[COLOR_BLACK], COLOR[COLOR_GREEN])
        # 画外墙
        pygame.draw.rect(maze_surface, COLOR[COLOR_RED], (0, 0, DIAMOND_LEN*cols+1, DIAMOND_LEN*rows+1), 2)
        # 画没打通的墙
        DrawWalls(maze_surface, DIAMOND_SIZE, walls, rows, cols)
        # 
        if parts:
            DrawWallList(maze_surface, COLOR[COLOR_RED], DIAMOND_SIZE, parts, rows, cols)
        # 
        if startPoint:
            pos = (startPoint[1]*DIAMOND_LEN + 10, startPoint[0]*DIAMOND_LEN + 10)
            DrawCircle(maze_surface, pos, COLOR[COLOR_RED])
        if endPoint:
            pos = (endPoint[1]*DIAMOND_LEN + 10, endPoint[0]*DIAMOND_LEN + 10)
            DrawCircle(maze_surface, pos, COLOR[COLOR_RED])
        # 
        if treasures:
            for p in treasures:
                pos = (p[1]*DIAMOND_LEN + 10, p[0]*DIAMOND_LEN + 10)
                DrawCircle(maze_surface, pos, COLOR[COLOR_GOLD])

        # 贴maze
        screen.blit(maze_surface, posion_xy)

        # 打印文字提示
        if findEndPoint:
            screen.blit(score_surface, (100, 20+rows*22))
        # 帧率
        clock.tick(25)

        pygame.display.update()
    return 

# 
def DrawWalls(screen, DIAMOND_SIZE, walls, rows, cols):
    for cx in range( cols):
        for ry in range(rows):
            px,py = 1 + (cx) * DIAMOND_SIZE[0], 1 + (ry) * DIAMOND_SIZE[1]
            color = COLOR[COLOR_BLACK]
            if maze.WALL == walls[ry][cx][0]:
                pygame.draw.line(screen, color, (px, py), (px, py+DIAMOND_LEN), 2)
            if maze.WALL == walls[ry][cx][1]:
                pygame.draw.line(screen, color, (px, py), (px+DIAMOND_LEN, py), 2)
    return 

# 
def DrawWallList(screen, color, DIAMOND_SIZE, wlist, rows, cols):
    for r,c,d in wlist:
        px,py = 1 + (c) * DIAMOND_SIZE[0], 1 + (r) * DIAMOND_SIZE[1]
        if d == 0:
            pygame.draw.line(screen, color, (px, py), (px, py+DIAMOND_LEN), 2)
        if d == 1:
            pygame.draw.line(screen, color, (px, py), (px+DIAMOND_LEN, py), 2)
    return 



# main
if __name__ == "__main__":
    '''main'''
    multipath_maze_demo(20, 30)

import pygame,sys
from pygame.locals import *
import random
import time

def gameAgain():    # 开始游戏
    '''
    第二页面的调用函数，为游戏主体部分。第一次载入和我方死亡或成功击杀对方后选择继续游戏时调用
    '''
    # 首先创建一个窗口 用来显示内容
    screen = pygame.display.set_mode((1080, 675))
    # 设置一个背景图片
    background = pygame.image.load('assert/image/background.png') # 加载图片作为背景
    # 此处无需指明窗口标题，主函数中设置一次title可一直沿用
    # 背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load('assert/music/background.mp3')
    pygame.mixer.music.set_volume(0.5)  # 设置背景音乐音量
    pygame.mixer.music.play(-1)  # 参数为循环次数 -1表示无限循环

    # 创建一个玩家飞机对象
    player = PlayerPlane(screen)
    # 创建一个敌机对象
    enemy = EnemyPlane(screen)

    # 设置要显示的内容
    while True:
        screen.blit(background, (0, 0))  # .blit() 显示加载的图片

        player.display()  # 显示玩家的飞机
        enemy.display()

        enemy.move()  # 敌机移动
        enemy.enemyfirebullet()  # 敌机随机发射子弹

        player.isHitted(enemy,130, 88)  # 是否击中hero
        enemy.isHitted(player,114,88)   # 是否击中enemy

        key_control(player)  # 调用键盘检测函数

        pygame.display.update()         # 更新显示内容
        pass
    pass

def end():  # 主游戏界面结束后的显示内容
    '''
    第三页面的调用函数，在我方死亡或成功击杀对方后提供选择界面，选择是否重新游戏或者退出
    '''
    screen = pygame.display.set_mode((1080, 675))  # 游戏窗口
    # 窗口title无需重新命名，可以与上一界面同用
    start_ck = pygame.Surface(screen.get_size())  # 充当开始界面的画布
    start_ck = pygame.image.load('assert/image/background.png')  # 加载背景图片

    start_ck2 = pygame.Surface(screen.get_size())  # 充当第一关的画布界面暂时占位（可以理解为游戏开始了）
    start_ck2 = pygame.image.load('assert/image/background.png')  # 加载背景图片

    start_button = pygame.image.load('assert/image/start1.png')
    start_button = pygame.transform.smoothscale(start_button, (256, 71))
    start_button.convert()

    press_start_button = pygame.image.load('assert/image/start2.png')
    press_start_button = pygame.transform.smoothscale(press_start_button, (256, 71))
    press_start_button.convert()

    end_button = pygame.image.load('assert/image/finish1.png')
    end_button = pygame.transform.smoothscale(end_button, (256, 71))
    end_button.convert()

    press_end_button = pygame.image.load('assert/image/finish2.png')
    press_end_button = pygame.transform.smoothscale(press_end_button, (256, 71))
    press_end_button.convert()

    tip_img = pygame.image.load('assert/image/end1.jfif')
    tip_img = pygame.transform.smoothscale(tip_img, (500, 380))
    tip_img.convert()

    #  以下为选择结束界面鼠标检测结构。
    n1 = True
    while n1:
        screen.blit(start_ck, (0, 0))
        buttons = pygame.mouse.get_pressed()    # 检测鼠标是否按下
        x1, y1 = pygame.mouse.get_pos()         # 检测鼠标位置
        if x1 >= 412 and x1 <= 668 and y1 >= 450 and y1 <= 521:
            start_ck.blit(press_start_button, (412, 450))
            if buttons[0]:
                print('开始游戏……')
                gameAgain()
                pass
            pass
        elif x1 >= 412 and x1 <= 668 and y1 >= 550 and y1 <= 621:
            start_ck.blit(press_end_button, (412, 550))
            if buttons[0]:  # 点击结束游戏退出窗口
                print('游戏退出……')
                pygame.quit()
                sys.exit()
                pass
            pass
        else:
            start_ck.blit(start_button, (412, 450))
            start_ck.blit(end_button, (412, 550))
            start_ck.blit(tip_img, (290, 30))
            pass
        pygame.display.update()

        # 下面是监听退出动作
        # 监听事件
        for event in pygame.event.get():
            # 判断事件类型是否是退出事件
            if event.type == pygame.QUIT:
                print("游戏退出...")
                # quit 卸载所有的模块
                pygame.quit()
                # exit() 直接终止当前正在执行的程序
                sys.exit()
                pass
            pass
    pygame.display.update()
    pass

class Base(object):
    '''
    基类（父类） 具有对象通性，但目前只应用于飞机类的继承
    '''
    def __init__(self, screen_temp, x, y, image_name, picture_num):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)
        # 爆炸效果用的如下属性
        self.hit = False                        # 表示是否要爆炸
        self.bomb_picture_list = []             # 用来存储爆炸时需要的图片
        self.bomb_picture_num = picture_num     # 飞机爆炸效果的图片数量
        self.image_num = 0      # 用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0    # 用来记录当前要显示的爆炸效果的图片的序号
        pass
    pass

class BasePlane(Base):
    '''
    飞机的基类
    '''
    def __init__(self,screen,x,y,imagePath,picture_num):
        '''
        初始化飞机基类
        :param screen:  主窗体
        :param imageName:   加载的图片
        '''
        Base.__init__(self,screen, x, y, imagePath, picture_num)
        self.screen = screen
        self.image = pygame.image.load(imagePath)
        self.bulletlist = []    # 存储所有的子弹
        pass
    def display(self):
        '''
        如果被击中,就显示爆炸效果,否则显示普通的飞机效果
        :return:
        '''
        if self.hit == True:
            self.screen.blit(self.bomb_picture_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7:  # 每７次循环换一张图片
                self.image_num = 0
                self.image_index += 1
            if self.image_index > self.bomb_picture_num - 1:       # 如果击中目标
                print('击中')
                # 播放爆炸音效
                pygame.mixer.init()
                fire = pygame.mixer.Sound('assert/music/boom.mp3')
                fire.set_volume(0.4)  # 设置音量
                fire.play()

                time.sleep(3)   # 击杀后页面停留三秒
                end()   # 切换到第三界面
                pass
            pass
        else:
            self.screen.blit(self.image,(self.x,self.y))
            pass

        # 完善子弹的展示逻辑
        needDelItemList = []

        for i in self.bulletlist:
            if i.judge():
                needDelItemList.append(i)
                pass
            pass

        # 重新遍历一下
        for i in needDelItemList:
            self.bulletlist.remove(i)
            pass

        for bullet in self.bulletlist:
            bullet.display()    # 显示子弹的位置
            bullet.move()   # 让这个子弹进行移动，下次显示的时候就会看到子弹在修改之后的位置
            pass
        pass
    pass
    def crate_images(self, bomb_picture_name):
        '''
        显示爆炸效果
        :param bomb_picture_name: 爆炸特效图片的文件名
        :return:
        '''
        for i in range(0, self.bomb_picture_num + 1):
            self.bomb_picture_list.append(pygame.image.load('./assert/boom/' +bomb_picture_name +str(i) + '.png'))
            pass
        pass
    def isHitted(self, plane, width, height):
        '''
        判断是否被击中
        :param plane: 飞机类型
        :param width: 飞机图片的宽
        :param height: 飞机图片的高
        :return:
        '''
        if plane.bulletlist is not None:
            for bullet in plane.bulletlist:
                if bullet.x > self.x and bullet.x < self.x + width and bullet.y > self.y and bullet.y < self.y + height:
                    plane.bulletlist.remove(bullet)
                    self.hit = True
                    pass
                pass
            pass
        pass

class BaseBullet(object):
    '''
    公共的子弹类
    '''
    def __init__(self,x,y,screen,bullettype):
        '''
        初始化子弹基类
        :param x: 子弹发出位置
        :param y: 子弹发出位置
        :param screen: 显示子弹
        :param bullettype: 传入子弹类型（敌机或玩家）
        '''
        self.type = bullettype
        self.screen =screen
        self.speed = 1
        if self.type == 'playerplane':
            self.x = x + 45
            self.y = y - 40
            self.imagePath = './assert/image/playerbullet.png'
            self.speed = 5      # 子弹移动速度
            pass
        elif self.type == 'enemyplane':
            self.x = x + 45
            self.y = y + 50
            self.imagePath = './assert/image/enemybullet.png'
            self.speed = 0.5
            pass
        self.image = pygame.image.load(self.imagePath)
        pass

    def move(self):
        '''
        让子弹动起来
        :return:
        '''
        if self.type == 'playerplane':
            self.y -= self.speed
            pass
        elif self.type == 'enemyplane':
            self.y += self.speed
        pass

    def display(self):
        '''
        显示子弹
        :return:
        '''
        self.screen.blit(self.image,(self.x,self.y))
        pass

    def judge(self):
        '''
        判断子弹是否越界
        :return:
        '''
        if self.y > 675 or self.y < 0:
            return True
        else:
            return False
        pass
    pass

class PlayerPlane(BasePlane):
    '''
    实现飞机的显示，控制飞机的移动
    '''
    def __init__(self,screen):
        '''
        初始化函数
        :param screen:主窗体对象
        '''
        BasePlane.__init__(self,screen,114,88,'./assert/image/playerplane2.png',8) # 调用父类的构造方法

        BasePlane.crate_images(self,'bomb')
        # 飞机的初始位置
        self.x = (1080 - 114)/2
        self.y = 675 - 88
        self.speed = 1.5    # 使战机移动画面比较连续，提升视觉效果。但是不可以调节过小。会导致敌机反应受我方控制
        pass
    def moveleft(self):
        '''
        向左移动
        :return:
        '''
        if self.x > 0:
            self.x -= self.speed
        pass
    def moveright(self):
        '''
        向右移动
        :return:
        '''
        if self.x < 1080 - 114:
            self.x += self.speed
        pass
    def moveup(self):
        '''
        向上移动
        :return:
        '''
        if self.y > 0:
            self.y -= self.speed
        pass
    def movedown(self):
        '''
        向下移动
        :return:
        '''
        if self.y < 675 - 88:
            self.y += self.speed
        pass
    def playerfireBullet(self):
        '''
        玩家发射子弹
        :return:
        '''
        # 射击音效
        file = pygame.mixer.Sound('assert/music/firebullet.mp3')
        file.set_volume(0.2)  # 设置音量
        file.play() # 播放射击音效

        newBullet = BaseBullet(self.x,self.y,self.screen,'playerplane')
        self.bulletlist.append(newBullet)
        pass
    pass

class EnemyPlane(BasePlane):
    '''
    创建敌机
    '''
    def __init__(self,screen):
        '''
        初始化敌机
        :param screen: 显示敌机
        '''
        BasePlane.__init__(self,screen,130, 88,'./assert/image/enemyplane.png',8)
        BasePlane.crate_images(self,'bomb')
        # 默认设置一个方向
        self.direction = 'right'
        # 飞机的初始位置
        self.x = random.randint(1,1080)
        self.y = 0
        self.image = pygame.transform.smoothscale(self.image, (130, 88))  # 原图196,133
        pass
    def enemyfirebullet(self):
        '''
        敌机随机发射子弹
        :return:
        '''
        num = random.randint(1,500)
        if num == 70 or num == 8:
            newBullet = BaseBullet(self.x,self.y,self.screen,'enemyplane')
            self.bulletlist.append(newBullet)
            pass
        pass
    def move(self):
        '''
        敌机随机移动
        :return:
        '''
        if self.direction == 'right':
            self.x += random.uniform(0.5,1)     # 向右移动时速度随机
            pass
        elif self.direction == 'left':
            self.x -= random.uniform(0.5,1)      # 向左移动时速度随机
            pass
        if self.x > 1080 - 130:
            self.direction = 'left'
            pass
        elif self.x < 0:
            self.direction = 'right'
            pass
        pass
    pass

def key_control(PlayerPlaneOBJ):    # 传入对象
    '''
    键盘控制检测函数。支持修改按键长按时的作用延迟修改：飞机移动的视觉效果对应的按键延迟以及发射子弹的按键延迟
    '''

    # 获取键盘事件
    delay = 3  # 按键3ms延迟响应 不能调节太高
    for event in pygame.event.get():
        if event.type == QUIT:
            print('游戏退出……')
            sys.exit()
            pass
        elif event.type == KEYDOWN:
            pygame.key.set_repeat(delay)  # 控制重复响应持续按下按键。
            if event.key == K_a or event.key == K_LEFT :
                print('left')
                PlayerPlaneOBJ.moveleft()   # 调用函数实现左移动
                pass
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                PlayerPlaneOBJ.moveright()  # 调用函数实现右移动
                pass
            elif event.key == K_w or event.key == K_UP:
                print('up')
                PlayerPlaneOBJ.moveup()
                pass
            elif event.key == K_s or event.key == K_DOWN:
                print('down')
                PlayerPlaneOBJ.movedown()
                pass
            elif event.key == K_SPACE:
                pygame.key.set_repeat(120)  # 发射子弹速度不会太快
                print('space')
                PlayerPlaneOBJ.playerfireBullet()
                pass
            pass
        pass
    pass

def main():
    '''
    第一界面的调用函数，提供进入游戏与结束游戏的入口界面
    '''
    screen = pygame.display.set_mode((1080, 675))  # 游戏窗口
    pygame.display.set_caption("飞机大战1.0 Coded by Xu For Jianjian")  # 给窗口取个名

    start_ck = pygame.Surface(screen.get_size())  # 充当开始界面的画布
    start_ck = pygame.image.load('assert/image/background.png')  # 加载背景图片

    start_ck2 = pygame.Surface(screen.get_size())  # 充当第一关的画布界面暂时占位（可以理解为游戏开始了）
    start_ck2 = pygame.image.load('assert/image/background.png')  # 加载背景图片

    start_button = pygame.image.load('assert/image/start1.png')
    start_button = pygame.transform.smoothscale(start_button,(256,71))
    start_button.convert()

    press_start_button = pygame.image.load('assert/image/start2.png')
    press_start_button = pygame.transform.smoothscale(press_start_button,(256,71))
    press_start_button.convert()

    end_button = pygame.image.load('assert/image/finish1.png')
    end_button = pygame.transform.smoothscale(end_button,(256,71))
    end_button.convert()

    press_end_button = pygame.image.load('assert/image/finish2.png')
    press_end_button = pygame.transform.smoothscale(press_end_button, (256, 71))
    press_end_button.convert()

    tip_img = pygame.image.load('assert/image/cover.png')
    tip_img = pygame.transform.smoothscale(tip_img, (355, 355))
    tip_img.convert()

    #  以下为选择开始界面鼠标检测结构。
    n1 = True
    while n1:
        screen.blit(start_ck, (0, 0))
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        if x1 >= 412 and x1 <= 668 and y1 >= 400 and y1 <= 471:
            start_ck.blit(press_start_button, (412, 400))
            if buttons[0]:
                print('开始游戏……')
                gameAgain()
                pass
            pass
        elif x1 >= 412 and x1 <= 668 and y1 >= 500 and y1 <= 571:
            start_ck.blit(press_end_button, (412, 500))
            if buttons[0]:  # 点击结束游戏退出窗口
                print('游戏退出……')
                pygame.quit()
                sys.exit()
                pass
            pass
        else:
            start_ck.blit(start_button, (412, 400))
            start_ck.blit(end_button, (412, 500))
            start_ck.blit(tip_img, (362.5, 30))
            pass

        pygame.display.update()

        # 下面是监听退出动作
        # 监听事件
        for event in pygame.event.get():
            # 判断事件类型是否是退出事件
            if event.type == pygame.QUIT:
                print("游戏退出...")
                # quit 卸载所有的模块
                pygame.quit()
                # exit() 直接终止当前正在执行的程序
                sys.exit()
                pass
            pass
        pass
    pygame.display.update()
    pass

if __name__ == '__main__':
    main()
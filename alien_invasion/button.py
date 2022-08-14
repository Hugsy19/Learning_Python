import pygame.font


class Button:
    """显示按钮的类"""

    def __init__(self, ai_game, msg):
        """初始化各种属性
        :param ai_game: AlienInvasion对象
        :prep msg: 需渲染的字符串
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50  # 大小
        self.button_color = (0, 0, 225)  # 颜色
        self.text_color = (255, 255, 255)  # 文字颜色
        self.font = pygame.font.SysFont(None, 48)  # 字体

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center  # 居中

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将字符串渲染为图像
        :prep msg: 需渲染的字符串
        """
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)  # 渲染为图像
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center  # 居中显示

    def draw_button(self):
        """绘制按钮"""
        self.screen.fill(self.button_color, self.rect)  # 填充颜色
        self.screen.blit(self.msg_image, self.msg_image_rect)  # 绘制文字

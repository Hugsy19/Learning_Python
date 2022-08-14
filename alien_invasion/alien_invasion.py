import sys
import pygame
import time

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from score_borad import ScoreBoard


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化并创建游戏资源"""
        pygame.init()  # 初始化背景设置
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # 窗口大小
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")  # 标题

        self.stats = GameStats(self)  # 统计
        self.ship = Ship(self)  # 飞船
        self.bullets = pygame.sprite.Group()  # 子弹组
        self.aliens = pygame.sprite.Group()  # 外星人组

        self._create_fleet()  # 创建外星人组
        self.play_button = Button(self, "Play")  # 显示Play按钮
        self.score_board = ScoreBoard(self)

    def run_game(self):
        """游戏主循环"""
        while True:
            self._check_event()  # 检查键鼠事件
            if self.stats.game_active:  # 检查游戏是否结束
                self.ship.update()  # 更新飞船位置
                self._update_bullets()  # 更新子弹
                self._update_aliens()  # 更新外星人
            self._update_screen()  # 更新屏幕

    def _check_event(self):
        """响应键鼠事件"""
        for event in pygame.event.get():  # 获取键鼠事件
            if event.type == pygame.QUIT:  # 单击关闭按钮
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 按键按下
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # 按键松开
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_screen(self):
        """更新屏幕图像"""
        self.screen.fill(self.settings.bg_color)  # 设置背景颜色
        self.ship.blitme()  # 绘制飞船
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # 绘制子弹
        self.aliens.draw(self.screen)  # 绘制外星人
        self.score_board.show_score()

        if not self.stats.game_active:  # 游戏为启动下
            self.play_button.draw_button()  # 显示Play按钮
        pygame.display.flip()  # 刷新屏幕

    def _update_bullets(self):
        """更新、管理子弹"""
        self.bullets.update()  # 更新子弹位置
        for bullet in self.bullets.copy():  # 循环时列表的长度不可变
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)  # 删除越界的子弹
        self._check_bullet_alien_collisions()  # 是否和外星人碰撞

    def _update_aliens(self):
        """更新、管理外星人"""
        self._check_fleet_edges()  # 检查边界
        self.aliens.update()  # 更新位置
        if pygame.sprite.spritecollide(self.ship, self.aliens, False):  # 是否和火箭发生碰撞
            self._ship_hit()

        self._check_aliens_bottom()  # 检查是否碰到底端

    def _check_keydown_events(self, event):
        """响应按键按下
        :param event: 键鼠事件
        """
        if event.key == pygame.K_RIGHT:  # 右移
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # 左移
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # 退出
            sys.exit()
        elif event.key == pygame.K_SPACE:  # 发射子弹
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应按键松开
        :param event: 键鼠事件
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_fleet_edges(self):
        """检查外星人是否到达边缘"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()  # 改变方向
                break

    def _check_aliens_bottom(self):
        """检查外星人是否到达底端"""
        screen_rect = self.screen.get_rect()  # 屏幕数据
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:  # 到达底端
                self._ship_hit()  # 按碰撞处理
                break

    def _change_fleet_direction(self):
        """改变外星人方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed  # 下落
        self.settings.fleet_direction *= -1  # 反方向

    def _check_bullet_alien_collisions(self):
        """检查子弹和外星人碰撞"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)  # 比较两个编组中各元素的rect，如发生重叠即销毁相应元素并返回为字典
        if collisions:
            for aliens in collisions.values():  # 按值遍历字典
                self.stats.score += self.settings.alien_points  # 计分
            self.score_board.prep_score()  # 渲染得分
            self.score_board.check_high_score()  # 检查最高得分
        if not self.aliens:  # 外星人都消灭了
            self.bullets.empty()
            self._create_fleet()  # 重新创建一群
            self.settings.increase_speed()  # 加快节奏

            self.stats.level += 1  # 提高等级
            self.score_board.prep_level()

    def _check_play_button(self, mouse_pos):
        """检查鼠标是否单击play按钮"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()  # 重置统计信息
            self._reset_game()  # 清屏重置
            self.settings.initialize_dynamic_settings()  # 重置设置
            self.stats.game_active = True  # 启动游戏
            self.score_board.prep_score()  # 重新渲染得分
            self.score_board.prep_score()  # 重新渲染等级
            self.score_board.prep_ships()  # 重新渲染剩余飞船
            pygame.mouse.set_visible(False)  # 隐藏鼠标

    def _fire_bullet(self):
        """创建子弹并加入子弹组"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        """处理飞船与外星人发生碰撞"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1  # 飞船数减1
            self.score_board.prep_ships()  # 更新剩余飞船数
            self._reset_game()
            time.sleep(1)  # 暂停1s
        else:
            self.stats.game_active = False  # 结束游戏
            pygame.mouse.set_visible(True)  # 显示鼠标

    def _reset_game(self):
        """清屏并重置游戏"""
        self.aliens.empty()  # 清屏
        self.bullets.empty()

        self._create_fleet()  # 重建外星人
        self.ship.center_ship()  # 居中

    def _create_fleet(self):
        """创建一群外星人"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaliable_space_x = self.settings.screen_width - 2 * alien_width  # 屏幕两边留一个外星人宽度
        # 外星人之间隔一个外星人宽度
        number_aliens_x = avaliable_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        avaliable_space_y = self.settings.screen_height - \
            3 * alien_height - ship_height  # 飞船上方留三个外星人高度
        number_rows = avaliable_space_y // (2 * alien_height)  # 外星人之间隔一个外星人高度

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):  # 一行外星人
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建单个外星人"""
        alien = Alien(self)
        alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
        alien.rect.x = alien.x  # 放置的位置
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)  # 加入外星人组


if __name__ == '__main__':
    """创建实例并运行游戏"""
    ai = AlienInvasion()
    ai.run_game()

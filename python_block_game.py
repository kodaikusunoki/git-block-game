import pygame
import sys
import time

# 初期化
pygame.init()

# ウィンドウのサイズ
width = 1500
height = 1000

# ウィンドウの作成
screen = pygame.display.set_mode((width, height))

# ウィンドウのタイトル
pygame.display.set_caption("ブロック崩し")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# フォントの設定
font = pygame.font.Font(None, 36)

# パドルの設定
paddle_width = 100
paddle_height = 15
paddle_speed = 15
paddle_x = (width - paddle_width) // 2
paddle_y = height - 30
paddle_acceleration = 5
left_passed_time = 0
right_passed_time = 0
paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

# ボールの設定
ball_radius = 10
ball_speed_x = 8
ball_speed_y = 8
ball_speed_increase = 0.005
ball = pygame.Rect(width // 2, height // 2, ball_radius * 2, ball_radius * 2)

# ブロックの設定
block_width = 60
block_height = 20
block_color = GREEN
brock_rows = 5
brock_cols = 20

blocks = []
for row in range(brock_rows):
    block_row = []
    for col in range(brock_cols):
        # ブロックの位置を設定
        block_x = col * (block_width + 10) + 35
        block_y = row * (block_height + 10) + 35
        block = pygame.Rect(block_x, block_y, block_width, block_height)
        # ブロックをリストに追加
        block_row.append(block)
    blocks.append(block_row)

# カウントダウンの表示
count_down_font = pygame.font.Font(None, 100)
for i in range(3, 0, -1):
    screen.fill(BLACK)
    count_down_text = count_down_font.render(f"{i}", True, WHITE)
    screen.blit(count_down_text, (width // 2 - count_down_text.get_width() // 2, height // 2 - count_down_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

# スコアの設定
score = 0
# ゲームのメインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # パドルの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        left_passed_time += 1
        right_passed_time = 0
        paddle_speed = (10 + paddle_acceleration * left_passed_time) # パドルの加速度を計算
        if paddle.left > 0:
            paddle.left -= paddle_speed
    elif keys[pygame.K_RIGHT]:
        right_passed_time += 1
        left_passed_time = 0
        paddle_speed = (10 + paddle_acceleration * right_passed_time) # パドルの加速度を計算
        if paddle.right < width:
            paddle.right += paddle_speed
    else:
        left_passed_time = 0
        right_passed_time = 0
        paddle_speed = 10 # ボタンが押されていない時はパドルの速度を10に戻す

    # ボールの移動
    ball.left += ball_speed_x
    ball.top += ball_speed_y
    
    # ボールと壁の衝突
    if ball.left <= 0 or ball.right >= width:
        ball_speed_y *= (1+ball_speed_increase) # 衝突によってボールの速度を上げる
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball.bottom >= height:
        running = False

    # ボールとブロックの衝突
    for row in blocks:
        for block in row:
            if ball.colliderect(block):
                ball_speed_y *= (1+ball_speed_increase) # 衝突によってボールの速度を上げる
                ball_speed_y = -ball_speed_y
                row.remove(block)
                score += 100
    
    # ボールとパドルの衝突
    if ball.colliderect(paddle):
        ball_speed_y *= (1+ball_speed_increase) # 衝突によってボールの速度を上げる
        ball_speed_y = -ball_speed_y
   
    # 画面の描画
    screen.fill(BLACK)
    # パドルの描画
    pygame.draw.rect(screen, BLUE, paddle)
    # ボールの描画
    pygame.draw.ellipse(screen, WHITE, ball)
    # ブロックの描画
    for row in blocks:
        for block in row:
            pygame.draw.rect(screen, block_color, block)

    # スコアの表示
    score_text = font.render(f"Score: {score}", True, WHITE) # スコアをテキストに変換
    screen.blit(score_text, (10, 10)) # スクリーンにスコアを表示

    time.sleep(0.02)
    pygame.display.flip()
    
# ゲーム終了後のスコアを表示
screen.fill(BLACK)
final_score_text = font.render(f"Game Over! Your score is {score}", True, WHITE)
exit_text = font.render("Press 'Enter to Exit", True, WHITE)
screen.blit(final_score_text, (width // 2 - final_score_text.get_width() // 2, height // 2 - final_score_text.get_height() // 2 - 20))
screen.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 - exit_text.get_height() // 2 + 20))
pygame.display.flip() # 画面を更新

waiting_for_exit = True
while waiting_for_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()     
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pygame.quit()
            sys.exit()   

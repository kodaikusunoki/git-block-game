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
paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

# ボールの設定
ball_radius = 10
ball_speed_x = 7
ball_speed_y = 7
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
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < width:
        paddle.right += paddle_speed

    # ボールの移動
    ball.left += ball_speed_x
    ball.top += ball_speed_y
    
    # ボールと壁の衝突
    if ball.left <= 0 or ball.right >= width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball.bottom >= height:
        running = False

    # ボールとブロックの衝突
    for row in blocks:
        for block in row:
            if ball.colliderect(block):
                ball_speed_y = -ball_speed_y
                row.remove(block)
                score += 100
    
    # ボールとパドルの衝突
    if ball.colliderect(paddle):
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
    
    
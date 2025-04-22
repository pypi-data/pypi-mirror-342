
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 配置
const gridSize = 20;  // 单元格像素
const tileCount = canvas.width / gridSize;

// 游戏状态
let snake;
let direction;
let food;
let score;
let gameLoop;

function initGame() {
    snake = [{x: 10, y: 10}];
    direction = {x: 0, y: 0};
    placeFood();
    score = 0;
    document.getElementById('score').textContent = '分数: ' + score;
    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(gameTick, 100);
}

function placeFood() {
    food = {
        x: Math.floor(Math.random() * tileCount),
        y: Math.floor(Math.random() * tileCount)
    };
    // 防止食物生成在蛇身上
    while (snake.some(s => s.x === food.x && s.y === food.y)) {
        food.x = Math.floor(Math.random() * tileCount);
        food.y = Math.floor(Math.random() * tileCount);
    }
}

function gameTick() {
    // 移动蛇
    const head = {x: snake[0].x + direction.x, y: snake[0].y + direction.y};

    // 边界、身体碰撞检测
    if (
        head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount ||
        snake.some(s => s.x === head.x && s.y === head.y)
    ) {
        clearInterval(gameLoop);
        ctx.fillStyle = "rgba(0,0,0,0.6)";
        ctx.fillRect(0,0,canvas.width,canvas.height);
        ctx.fillStyle = "#fff";
        ctx.font = "32px Arial";
        ctx.fillText('游戏结束', canvas.width / 2 - 70, canvas.height / 2);
        return;
    }

    snake.unshift(head);

    // 吃到食物
    if (head.x === food.x && head.y === food.y) {
        score++;
        document.getElementById('score').textContent = '分数: ' + score;
        placeFood();
    } else {
        snake.pop();
    }

    draw();
}

function draw() {
    ctx.fillStyle = '#eee';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 绘制食物
    ctx.fillStyle = '#f00';
    ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize-2, gridSize-2);

    // 绘制蛇
    ctx.fillStyle = '#080';
    snake.forEach((s, i) => {
        ctx.fillRect(s.x * gridSize, s.y * gridSize, gridSize-2, gridSize-2);
    });
}

// 控制
window.addEventListener('keydown', e => {
    switch(e.key) {
        case 'ArrowLeft':
        case 'a':
            if (direction.x !== 1) direction = {x: -1, y: 0};
            break;
        case 'ArrowUp':
        case 'w':
            if (direction.y !== 1) direction = {x: 0, y: -1};
            break;
        case 'ArrowRight':
        case 'd':
            if (direction.x !== -1) direction = {x: 1, y: 0};
            break;
        case 'ArrowDown':
        case 's':
            if (direction.y !== -1) direction = {x: 0, y: 1};
            break;
    }
});

// 重新开始按钮
function restartGame() {
    initGame();
}

// 自动初始化
initGame();

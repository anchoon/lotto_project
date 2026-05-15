const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = 400; canvas.height = 400;
let balls = [], drawCount = 0;

class Ball {
    constructor(num) {
        this.num = num; this.x = Math.random() * 350 + 25; this.y = Math.random() * 350 + 25;
        this.vx = (Math.random() - 0.5) * 8; this.vy = (Math.random() - 0.5) * 8;
    }
    move() {
        this.x += this.vx; this.y += this.vy;
        if (this.x < 20 || this.x > 380) this.vx *= -1;
        if (this.y < 20 || this.y > 380) this.vy *= -1;
    }
    draw() {
        ctx.beginPath(); ctx.arc(this.x, this.y, 16, 0, Math.PI * 2);
        ctx.fillStyle = getColor(this.num); ctx.fill(); 
        ctx.strokeStyle = "#fff"; ctx.stroke();
        ctx.fillStyle = "#000"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(this.num, this.x, this.y);
    }
}

function init() { balls = []; for (let i = 1; i <= 45; i++) balls.push(new Ball(i)); }
function animate() { ctx.clearRect(0,0,400,400); balls.forEach(b => { b.move(); b.draw(); }); requestAnimationFrame(animate); }

// 번호 생성 로직
function getLottoNumbers() {
    let picked = [];
    while(picked.length < 6) {
        let n = Math.floor(Math.random() * 45) + 1;
        if(!picked.includes(n)) picked.push(n);
    }
    return picked.sort((a,b) => a-b);
}

// 1줄 추첨 (애니메이션 포함)
function startDraw() {
    if (drawCount >= 5) return alert("최대 5줄입니다.");
    const line = document.createElement("div"); line.className = "line";
    line.innerHTML = `<strong>${++drawCount}줄</strong>`;
    document.getElementById("result").appendChild(line);
    
    let nums = getLottoNumbers();
    nums.forEach((n, i) => {
        setTimeout(() => {
            animateBall(n);
            setTimeout(() => {
                const b = document.createElement("div");
                b.className = "ball " + getColorClass(n); b.innerText = n;
                line.appendChild(b);
            }, 1200);
        }, i * 1400);
    });
}

// 빠른 추첨 (애니메이션 건너뜀)
function fastFive() {
    resetDraw(); // 기존 결과 삭제
    for (let i = 1; i <= 5; i++) {
        const line = document.createElement("div"); line.className = "line";
        line.innerHTML = `<strong>${i}줄</strong>`;
        let nums = getLottoNumbers();
        nums.forEach(n => {
            const b = document.createElement("div");
            b.className = "ball " + getColorClass(n); b.innerText = n;
            line.appendChild(b);
        });
        document.getElementById("result").appendChild(line);
    }
    drawCount = 5;
}

function animateBall(n) {
    const tube = document.getElementById("tube");
    const ball = document.createElement("div");
    ball.className = "ball-moving " + getColorClass(n);
    ball.innerText = n;
    tube.appendChild(ball);
    setTimeout(() => ball.remove(), 1200);
}

function resetDraw() { document.getElementById("result").innerHTML = ""; drawCount = 0; init(); }
function getColor(n) { 
    if(n<=10) return "#ffcc00"; if(n<=20) return "#007bff"; 
    if(n<=30) return "#28a745"; if(n<=40) return "#a333c8"; return "#555"; 
}
function getColorClass(n) { 
    if(n<=10) return "c1"; if(n<=20) return "c2"; 
    if(n<=30) return "c3"; if(n<=40) return "c4"; return "c5"; 
}

init(); animate();

setInterval(() => {
    location.reload()
}, 60000)
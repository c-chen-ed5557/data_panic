var resources = 0;

function setup() {
    createCanvas(800, 800);
}

function draw() {
    background(51);
    resources = document.getElementById('user_resources').innerHTML;
    draw_resources(resources);
}

function draw_resources(number) {
    for(let i=0;i<resources;i++){
        ellipse(40*(i+1), 40, 40, 40);
    }
}
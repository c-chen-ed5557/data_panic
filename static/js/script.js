var resources = 0;

function setup() {
    createCanvas(300, 60);
}

function draw() {
    background(17);
    resources = document.getElementById('user_resources').innerHTML;
    draw_resources(resources);
}

function draw_resources(number) {
    stroke(255);

    // fill(255);
    for(let i=0;i<resources;i++){
        noFill();
        strokeWeight(2);
        arc(40*(i+1), 28, 40, 40, -PI/6 * 5, -PI/6);
        arc(40*(i+1), 32, 36, 36, -PI/5 * 4, -PI/5);
        arc(40*(i+1), 36, 32, 32, -PI/4 * 3, -PI/4);
        arc(40*(i+1), 40, 30, 30, -PI/3 * 2, -PI/3);
        fill(255);
        ellipse(40*(i+1), 32, 5, 5);
    }
}
let capture;
let gui;

// let b;
let s1;
let s2;
let s3;
let s4;



let sliderWidth;
let sliderPad;
let sliderXInitial;
let sliderY;



function setup() {

// createCanvas(windowWidth/1.5, windowHeight*0.9);
//createCanvas(1200, 900);
myCanvas = createCanvas(850, 600);
myCanvas.parent("area");

sliderWidth = width * 0.2;
sliderPad = width * (1/40);
sliderXInitial = sliderPad;
sliderY = 515;

frameRate(60);
capture = createCapture(VIDEO); //Webcam
capture.size(windowWidth/1.5, windowHeight/1.5);
capture.hide();
// background(0);
    gui = createGui();
    s1 = createSlider("Slider1", sliderXInitial, sliderY, sliderWidth, 32, -50, 50);
    s2 = createSlider("Slider2", sliderXInitial+sliderWidth*1+sliderPad*2, sliderY, sliderWidth, 32, -50, 50);
    s3 = createSlider("Slider3", sliderXInitial+sliderWidth*2+sliderPad*4, sliderY, sliderWidth, 32, -50, 50);
    s4 = createSlider("Slider4", sliderXInitial+sliderWidth*3+sliderPad*6, sliderY, sliderWidth, 32, 100, 300);
    s1.setStyle("fillBg", color(49,183,123));
    s2.setStyle("fillBg", color(49,183,123));
    s3.setStyle("fillBg", color(49,183,123));
    s4.setStyle("fillBg", color(49,183,123));
    s1.val = 0;
    s2.val = 0;
    s3.val = 0;
    s4.val = 120;

}
function draw() {

//キャプチャーした画像を描画してピクセル情報の読み込み
capture.loadPixels();
let widthRatio = capture.width / width;
let heightRatio = capture.height / height;
for (let i = 0; i < 100; i++) {

let x = int(random(width)); //色を取得する位置をランダムに決定
let y = int(random(height));
let col = capture.get(x * widthRatio, y *heightRatio); //指定した場所の色を取得
noStroke();
let diameter = map(saturation(col), 0,255, 1, 120); //色の彩度を円の直径に反映させる
fill(red(col)+s1.val, green(col)+s2.val, blue(col)+s3.val,128); //色に透明度を加える
if (y < 490) {
    ellipse(x, y, diameter); //円を描画
}


drawGui();
}

}
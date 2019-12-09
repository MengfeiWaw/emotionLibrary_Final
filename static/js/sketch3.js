var img;
var AR= 0
var objSize=6;
var objDis=24;
var capture;

let gui;

let s1;
let s2;
let s3;
let s4;

function setup() {
  //createCanvas(1200, 900);
  myCanvas = createCanvas(850, 600);
  myCanvas.parent("area");
  gui = createGui();
  sliderWidth = width * 0.2;
  sliderPad = width * (1/40);
  sliderXInitial = sliderPad;
  sliderY = 515;

  s1 = createSlider("Slider1", sliderXInitial, sliderY, sliderWidth, 32, -30, 100);
  s2 = createSlider("Slider2", sliderXInitial+sliderWidth*1+sliderPad*2, sliderY, sliderWidth, 32, -30, 100);
  s3 = createSlider("Slider3", sliderXInitial+sliderWidth*2+sliderPad*4, sliderY, sliderWidth, 32, -30, 100);
  s4 = createSlider("Slider4", sliderXInitial+sliderWidth*3+sliderPad*6, sliderY, sliderWidth, 32, 1, 70);
  s1.setStyle("fillBg", color(49,183,123));
  s2.setStyle("fillBg", color(49,183,123));
  s3.setStyle("fillBg", color(49,183,123));
  s4.setStyle("fillBg", color(49,183,123));
  s1.val = 0;
  s2.val = 0;
  s3.val = 0;
  s4.val = 16;

  frameRate(60);
  capture = createCapture(VIDEO);
  capture.size(windowWidth/1.5, windowHeight/1.5);
  capture.hide();
}

function draw() {
  capture.loadPixels();

  for(var y=0; y<windowHeight/1.5; y+=objDis){//yposition of my pattern
    for(var x=0; x<windowWidth/1.5; x+=objDis) {//xposition of my pattern
      var i =y*capture.width+x;
      fill(capture.pixels[i*4]+s1.val,capture.pixels[i*4+1]+s2.val,capture.pixels[i*4+2]+s3.val);
      noStroke();
      if (y <= 490)
      {
        ellipse(x,y,random(objSize,objSize+s4.val));
      }
    }
  }
  drawGui();
}
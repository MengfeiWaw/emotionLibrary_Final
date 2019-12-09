var capture;
var captureMax = 500 ;

let gui;

let s1;
let s2;
let s3;
let s4;

let sliderWidth;
let sliderPad;
let sliderXInitial;
let sliderY



function preload () {
  capture = createCapture(VIDEO);
  capture.size(windowWidth/1.5, windowHeight/1.5);
 	capture.hide();
}

function setup() {
	//createCanvas(1200, 900);
  myCanvas = createCanvas(850, 600);
  myCanvas.parent("area");

	sliderWidth = width * 0.2;
	sliderPad = width * (1/40);
	sliderXInitial = sliderPad;
	sliderY = 515;

  stroke(200, 0, 5, 0.3);
	frameRate(30);

    gui = createGui();
    s1 = createSlider("Slider1", sliderXInitial, sliderY, sliderWidth, 32, -50, 100);
    s2 = createSlider("Slider2", sliderXInitial+sliderWidth*1+sliderPad*2, sliderY, sliderWidth, 32, -50, 100);
    s3 = createSlider("Slider3", sliderXInitial+sliderWidth*2+sliderPad*4, sliderY, sliderWidth, 32, -50, 100);
    s4 = createSlider("Slider4", sliderXInitial+sliderWidth*3+sliderPad*6, sliderY, sliderWidth, 32, 0, 10);
    s1.setStyle("fillBg", color(49,183,123));
    s2.setStyle("fillBg", color(49,183,123));
    s3.setStyle("fillBg", color(49,183,123));
    s4.setStyle("fillBg", color(49,183,123));
    s1.val = 0;
    s2.val = 0;
    s3.val = 0;
    s4.val = 0;
}

function draw() {
	capture.loadPixels();
  drawGui();
  //blendMode (HARD_LIGHT) ;
  colorMode ( RGB, 100, 100, 50);
	if (capture.length > captureMax) {
            capture.shift();
				 }

	for (var i=0; i<1000; ++i) {

        var x = int(random(capture.width));
        var y = int(random(capture.height));
        var pix = (x + y*capture.width) * 4;
        var col = capture.pixels.slice( pix, pix+6 );

		fill( col[0] + s1.val,col[1]+s2.val,col[2]+s3.val)
 		stroke( col[0], col[1], col[2]);
        if (y < 490) {
		rect( x , y ,20,3+s4.val, random (30,60) ) ;

		}
	}
}
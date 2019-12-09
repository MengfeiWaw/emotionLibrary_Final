let img;
let gui;

// let b;
let s1;
let s2;
let s3;
let s4;
let myDiv = document.getElementById("myDiv");
myDiv.style.zIndex = "1";

function setup() {
    // createCanvas(windowWidth/1.5, windowHeight);
    //createCanvas(1200, 900);
    myCanvas = createCanvas(850, 600);
    myCanvas.parent("area");
    // myCanvas.style.zIndex = "-1";
    sliderWidth = width * 0.2;
    sliderPad = width * (1/40);
    sliderXInitial = sliderPad;
    sliderY = 515;

    img = createCapture(VIDEO);
    img.size(windowWidth/1.5, windowHeight/1.5);
    img.hide();

    gui = createGui();
    // b = createButton("Record", 50, 160);
    s1 = createSlider("Slider1", sliderXInitial, sliderY, sliderWidth, 32, 0, 255);
    s2 = createSlider("Slider2", sliderXInitial+sliderWidth*1+sliderPad*2, sliderY, sliderWidth, 32, 0, 255);
    s3 = createSlider("Slider3", sliderXInitial+sliderWidth*2+sliderPad*4, sliderY, sliderWidth, 32, 0, 255);
    s4 = createSlider("Slider4", sliderXInitial+sliderWidth*3+sliderPad*6, sliderY, sliderWidth, 32, 0, 20);
    s1.setStyle("fillBg", color(49,183,123));
    s2.setStyle("fillBg", color(49,183,123));
    s3.setStyle("fillBg", color(49,183,123));
    s4.setStyle("fillBg", color(49,183,123));
    s1.val = 100;
    s2.val = 100;
    s3.val = 100;
    s4.val = 10;
}

function draw() {
	img.loadPixels();
  for (let y=img.height ; y>0; y-=10)
  {
    for (let x=img.width; x>0; x-=10)
    {
      var p = img.pixels[(y*img.width-x)*4];
      if (y <= 490)
      {
        if (p < 100 & p > 50 )
        {
          fill(s1.val);
  		    rect(x-100, y, s4.val, s4.val);
        }
        if (p < 200 & p > 100 )
        {
          fill(p,205,s2.val);
          rect(x-100, y, s4.val, s4.val);
        }
        if (p < 100 & p > 0 )
        {
          fill(s3.val,97,p);
          ellipse(x-100, y, s4.val, s4.val);
        }
      }

    }
  }
  drawGui();
}
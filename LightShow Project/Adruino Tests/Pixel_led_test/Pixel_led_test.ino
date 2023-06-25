#include <FastLED.h>

#define DATA_PIN 3 // for LED strand

#define NUM_LEDS 99
int number = 0;
int Red = 2;
int White = 1;
int Blue = 0;
int colorState = 1;

CRGB leds[NUM_LEDS];

CRGBPalette16 currentPalettestriped; //for Candy Cane

void setup()
{
  Serial.begin(9600);

  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);

  leds[0] = CRGB::Black;
  leds[1] = CRGB::Black;
  leds[2] = CRGB::Black;
  leds[3] = CRGB::Black;
  FastLED.show();

  setupStripedPalette( CRGB::Red, CRGB::Red, CRGB::White, CRGB::White); //for CANDY CANE 
}

void loop()
{
  /*leds[0] = CRGB(255,255,255);
  leds[1] = CRGB(255,0,255);
  leds[2] = CRGB(255,0,0);
  leds[3] = CRGB(0,255,0);
  */
  fill_solid( leds,NUM_LEDS, CRGB(50,50,50));
  //blink();
  //America();
  //SnowSparkle(25, 25, 25, 40, random(250,1000));
  //Lines(0, 0, 150, 100, 100, 100, 1, 2);
  //CandyCane();

}






void blink(){
  for(int x = 0; x < NUM_LEDS;x++){
     leds[number] = CRGB(255,0,0);
     FastLED.show();
     delay(100);
     leds[number] = CRGB(0,0,0);
     FastLED.show();
     number = number +1;
  }
  number = 0;
  
}
void America(){
   for (int i = 0; i <= 49; i++) {
    leds[i] = CRGB ( 255, 0, 0);
    FastLED.show();
    delay(20);
  }
  for (int i = 49; i >= 0; i--) {
    leds[i] = CRGB ( 255,100, 0);
    FastLED.show();
    delay(20);

  }
  for (int i = 0; i <= 49; i++) {
    leds[i] = CRGB ( 255, 255, 0);
    FastLED.show();
    delay(20);
  }
  for (int i = 49; i >= 0; i--) {
    leds[i] = CRGB ( 0, 255, 0);
    FastLED.show();
    delay(20);
    }
  for (int i = 0; i <= 49; i++) {
    leds[i] = CRGB ( 0, 150, 255);
    FastLED.show();
    delay(20);
  }
  for (int i = 49; i >= 0; i--) {
    leds[i] = CRGB ( 150,0,255);
    FastLED.show();
    delay(20);

  }
  for (int i = 0; i <= 49; i++) {
    leds[i] = CRGB ( 255, 255, 255);
    FastLED.show();
    delay(20);
  }
  for (int i = 49; i >= 0; i--) {
    leds[i] = CRGB ( 0, 0, 0);
    FastLED.show();
    delay(20);

  }
}

void SnowSparkle(int red, int green, int blue, int SparkleDelay, int SpeedDelay){
  fill_solid( leds,NUM_LEDS, CRGB(red,green,blue));
  int Pixel = random(NUM_LEDS);
  leds[Pixel] = CRGB ( 200, 200, 200);
  FastLED.show();
  delay(SparkleDelay);
  leds[Pixel] = CRGB (red, green, blue);
  FastLED.show();
  delay(SpeedDelay);
  
}

void Lines(int red1, int green1, int blue1, int red2, int green2, int blue2, int Gap, int ChangeDelay){
  int Spacing = Gap * 4;
  int Length = NUM_LEDS/Spacing;
  int A = 0;
  int B = 1;
  int C = 2;
  int D = 3;
  FastLED.show();
  for (int b = 0; b < Length; b++){
    leds[A] = CRGB ( red1, green1, blue1);
    leds[B] = CRGB ( 0, 0, 0);
    leds[C] = CRGB ( red2, green2, blue2);
    leds[D] = CRGB ( 0, 0, 0);
    FastLED.show();
    A += 4;
    B += 4;
    C += 4;
    D += 4;
  }
  
}

void CandyCane(){
    static uint8_t startIndex = 0;
    startIndex = startIndex + 1; /* higher = faster motion */

    fill_palette( leds, NUM_LEDS,
                  startIndex, 16, /* higher = narrower stripes */
                  currentPalettestriped, 255, LINEARBLEND);
}

void setupStripedPalette( CRGB A, CRGB AB, CRGB B, CRGB BA)
{
  currentPalettestriped = CRGBPalette16(
                            A, A, A, A, A, A, A, A, B, B, B, B, B, B, B, B
                          );
}





  

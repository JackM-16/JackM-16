#include <SPI.h>
#include <FastLED.h>

const int led = 13;
String usbRead = "";
int lightNumber;
int R;
int G;
int B;
String value;

#define DATA_PIN 3 // for LED strand
#define NUM_LEDS 50
CRGB leds[NUM_LEDS];


void setup(){
  Serial.begin(9600);
  pinMode(led,OUTPUT);
  digitalWrite(led,LOW);
  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
  fill_solid( leds,NUM_LEDS, CRGB(0,0,0));
  FastLED.show();
}

void loop(){
  if(Serial.available() >= 12){
    value = "";
    for(int i=0; i<12; i++){
      usbRead = Serial.read() - '0';
      if (usbRead.toInt() < 0) {Serial.println(usbRead);i--;}
      else{
      value += usbRead;}
    }
    Serial.println(value);
    lightNumber = value.substring(0, 3).toInt();
    R = value.substring(3, 6).toInt();
    G = value.substring(6, 9).toInt();
    B = value.substring(9).toInt();
    turnOn(lightNumber,R,G,B);
    usbRead = '0';
  }

} //end of loop

void turnOn(int number, int rColor, int gColor, int bColor){
  leds[number] = CRGB (rColor,gColor,bColor);
    FastLED.show();
}

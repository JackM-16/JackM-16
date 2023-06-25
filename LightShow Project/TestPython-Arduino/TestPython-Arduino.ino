#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <FastLED.h>
const byte address[6] = "00001";

const int led = 13;
String usbRead = "";
int var = 1;
int lightNumber;
int R;
int G;
int B;
boolean first;
int timeRepeat = 1;
String value;

#define DATA_PIN 3 // for LED strand
#define NUM_LEDS 150
CRGB leds[NUM_LEDS];


void setup(){
  Serial.begin(115200);
  pinMode(led,OUTPUT);
  digitalWrite(led,LOW);
  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
  fill_solid( leds,NUM_LEDS, CRGB(0,0,0));
  FastLED.show();
  Serial.setTimeout(20);
}

void loop(){
  var = 1;
  if(Serial.available() >= 3){
    first = true;
    value = "";
    for(int i=0; i<3; i++){
      usbRead = Serial.read() - '0';
      first = false;
      if (usbRead.toInt() < 0) {Serial.println(usbRead);i--;}
      else{
      value += usbRead;}
    }
    if (timeRepeat == 1)
    {
      lightNumber = value.toInt();
      timeRepeat ++;
    }
    else if (timeRepeat == 2)
    {
      R = value.toInt();
      timeRepeat ++;
    }
    else if (timeRepeat == 3)
    {
      G = value.toInt();
      timeRepeat ++;
    }
    else
    {
      B = value.toInt();
      timeRepeat = 1;
      if(lightNumber == 999 and R == 999 and G == 999 and B == 999){FastLED.show();}
      else{
      turnOn(lightNumber,R,G,B);
      }
    }
    usbRead = '0';
  }

} //end of loop

void turnOn(int number, int rColor, int gColor, int bColor){
  leds[number] = CRGB (rColor,gColor,bColor);
    //FastLED.show();
}

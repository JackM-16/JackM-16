#include <Ethernet.h> //Load Ethernet Library
#include <EthernetUdp.h> //Load the Udp Library
#include <SPI.h> //Load SPI Library

#include <FastLED.h>
 
byte mac[] ={ 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE}; //Assign mac address
IPAddress ip(192,168,1,99); //Assign the IP Adress
unsigned int localPort = 5000; // Assign a port to talk over
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //dimensian a char array to hold our data packet
String datReq; //String for our data
int packetSize; //Size of the packet
EthernetUDP Udp; // Create a UDP Object
String mainSpace = ", ";

#define DATA_PIN 3 // for LED strand
#define NUM_LEDS 300
CRGB leds[NUM_LEDS];

void setup() {
  
  Serial.begin(9600); //Initialize Serial Port 
  Ethernet.begin( mac, ip); //Inialize the Ethernet
  Udp.begin(localPort); //Initialize Udp
  delay(1000); //delay

  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
  fill_solid( leds,NUM_LEDS, CRGB(0,0,0));
  FastLED.show();
 
}
 
void loop() {
  
  packetSize = Udp.parsePacket(); //Reads the packet size
  
  if(packetSize>0) { //if packetSize is >0, that means someone has sent a request
    
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //Read the data request
    String datReq(packetBuffer); //Convert char array packetBuffer into a string called datReq
    String mainVal = datReq;
    while (mainVal.length() >= 6){
      int universe = (((int) mainVal[0])-33)*170;
      int A = ((int) mainVal[1])-33 ;
      int B = ((int) mainVal[2])-33 ;
      int pin = universe + A + B;
      int red = ((int) mainVal[3]) - 33;
      int green = ((int) mainVal[4])-33;
      int blue = ((int) mainVal[5])-33;
      if (((int) mainVal[3]) == 119){
        FastLED.show();
      }
      else if (((int) mainVal[3]) == 120){
        fill_solid( leds,NUM_LEDS, CRGB(0,0,0));
        FastLED.show();
      }
      else{
        turnOn(pin, red*3, green*3, blue*3);
      }
      mainVal = mainVal.substring(6);
    }
    
      
  }
  memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE); //clear out the packetBuffer array
}

void turnOn(int number, int rColor, int gColor, int bColor){
  leds[number] = CRGB (rColor,gColor,bColor);
  //Serial.println(number+mainSpace+rColor+mainSpace+gColor+mainSpace+bColor);
}

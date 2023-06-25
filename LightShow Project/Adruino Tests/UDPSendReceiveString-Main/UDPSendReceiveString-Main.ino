#include <Ethernet.h> //Load Ethernet Library
#include <EthernetUdp.h> //Load the Udp Library
#include <SPI.h> //Load SPI Library

#include <FastLED.h>
 
byte mac[] ={ 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE}; //Assign mac address
IPAddress ip(192,168,20,155); //Assign the IP Adress
unsigned int localPort = 5000; // Assign a port to talk over
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //dimensian a char array to hold our data packet
String datReq; //String for our data
int packetSize; //Size of the packet
EthernetUDP Udp; // Create a UDP Object

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
    
    if (datReq =="000000") { //Do the following if Temperature is requested
      
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); //Initialize packet send
      Udp.print(100); //Send the temperature data
      Udp.endPacket(); //End the packet
      
    }
    
    else if (datReq== "999999999999") { //Do the following if Pressure is requested
      fill_solid( leds,NUM_LEDS, CRGB(0,0,0));
      FastLED.show();

        Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); //Initialize packet send
        Udp.print(20); //Send the Pressure data
        Udp.endPacket(); //End the packet
        
    }

    else if (datReq== "888888888888") { //Do the following if Pressure is requested
      fill_solid( leds,NUM_LEDS, CRGB(0,0,50));
      FastLED.show();
        
    }

    else { //Do the following if Pressure is requested
       String allData = datReq;
        while (allData.length() >= 12){
          int pin = allData.substring(0,3).toInt();
          int red = allData.substring(3,6).toInt();
          int green = allData.substring(6,9).toInt();
          int blue = allData.substring(9,12).toInt();

          if (red == 999 && green == 999 && blue == 999){
            FastLED.show();
          }
          else{
            turnOn(pin,red,green,blue);
          }

          allData = allData.substring(12);
        }
        
    }
      
  }
  //memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE); //clear out the packetBuffer array
}

void turnOn(int number, int rColor, int gColor, int bColor){
  leds[number] = CRGB (rColor,gColor,bColor);
   //FastLED.show();
}

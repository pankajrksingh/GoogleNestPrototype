#include <RCSwitch.h>


#include "DHT.h"

#define DHTPIN 2    // what pin we're connected to

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11 
//#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)
#define TransmitterPin 9

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor for normal 16mhz Arduino
DHT dht(DHTPIN, DHTTYPE);
// NOTE: For working with a faster chip, like an Arduino Due or Teensy, you
// might need to increase the threshold for cycle counts considered a 1 or 0.
// You can do this by passing a 3rd parameter for this threshold.  It's a bit
// of fiddling to find the right value, but in general the faster the CPU the
// higher the value.  The default for a 16mhz AVR is a value of 6.  For an
// Arduino Due that runs at 84mhz a value of 30 works.
// Example to initialize DHT sensor for Arduino Due:
//DHT dht(DHTPIN, DHTTYPE, 30);

int team_number = 1;
int temperature_datatype = 1;
int humidity_datatype = 2;
RCSwitch mySwitch = RCSwitch();
int temperature_history=0;
int humidity_history=0;

void setup() {
  Serial.begin(9600); 
  pinMode(TransmitterPin, OUTPUT);
  Serial.println("DHT11 test!");
  dht.begin();
  mySwitch.enableTransmit(TransmitterPin);
}

void loop() {

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  int h = dht.readHumidity();
  //Serial.println(h);
  // Read temperature as Celsius
  int t = dht.readTemperature();
  //Serial.println(t);
  // Read temperature as Fahrenheit
  //float f = dht.readTemperature(true);
  //Serial.println();
  
  // Check if any reads failed and exit early (to try again).
  //if (isnan(h) || isnan(t) || isnan(f)) {
  if (isnan(h) && isnan(t)) {
    //Serial.println("Failed to read from DHT sensor!");
    return;
  }
  else {
    if(!isnan(t) && temperature_history != t)
    {
      //temperature_history = t;
      //Serial.println(t);
      int randomnumber = random(1, 9);
      //Serial.println(randomnumber);
      int checksum = (team_number + temperature_datatype + getDigit(t,2) + getDigit(t,1)) * randomnumber;
      String temperatureMessage1 = String(team_number) + String(temperature_datatype) + String(getDigit(t,2)) + String(getDigit(t,1)) + String(randomnumber) + String(getDigit(checksum,3)) + String(getDigit(checksum,2)) + String(getDigit(checksum,1));
      unsigned long temperatureMessage = temperatureMessage1.toInt();
      Serial.print("Temperature Message: ");
      Serial.println(temperatureMessage);
      mySwitch.send(temperatureMessage, 24);
    }
    if(!isnan(h) && humidity_history != h)
    {
      //humidity_history = h;
      //Serial.println(h);
      int randomnumber = random(1, 9);
      //Serial.println(randomnumber);
      int checksum = (team_number + humidity_datatype + getDigit(h,2) + getDigit(h,1)) * randomnumber; 
      String humidityMessage1 = String(team_number) + String(humidity_datatype) + String(getDigit(h,2)) + String(getDigit(h,1)) + String(randomnumber) + String(getDigit(checksum,3)) + String(getDigit(checksum,2)) + String(getDigit(checksum,1));    
      unsigned long humidityMessage = humidityMessage1.toInt();
      Serial.print("Humidity Message: ");
      Serial.println(humidityMessage);
      mySwitch.send(humidityMessage, 24);
    }
  }
    

  // Compute heat index
  // Must send in temp in Fahrenheit!
  //float hi = dht.computeHeatIndex(f, h);

  //Serial.print("Humidity: "); 
  //Serial.print(h);
  //Serial.print(" %\t");
  //Serial.print("Temperature: "); 
  //Serial.print(t);
  //Serial.print(" *C ");
  //Serial.print(f);
  //Serial.print(" *F\t");
  //Serial.print("Heat index: ");
  //Serial.print(hi);
  //Serial.println(" *F");

  
  delay(2000);
}

int getDigit(unsigned int number, int digit) {
    for (int i=0; i<digit-1; i++) { 
      number /= 10; 
    }
    return number % 10;
}

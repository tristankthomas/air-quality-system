#include "DHT.h"    
#include <LiquidCrystal_I2C.h>
#include <Servo.h>
 
#define TEMP_SENSOR_TYPE DHT11 // Declaring the type of DHT sensor we are using (DHT11)
#define GAS_LIMIT 200 // set to 300 for real-world
#define AIR_LIMIT 100 // need to calibrate it to CO2 for real-world
#define MIN_FAN_SPEED 168 // pwm value approx 65% duty cycle
#define MAX_FAN_SPEED 255 // pwm value at 100% duty cycle (always 1)
#define MIN_TEMP 15 // min temp @ 0 duty cycle
#define MAX_TEMP 30 // max temp (fan will turn on at approx 25 degrees)

const int gasSensorPin = 0; // analog
const int airsensorPin = 1; // analog
const int motorOutputPin1 = 4;  // pin 2 on L293D
const int motorOutputPin2 = 3;  // pin 7 on L293D
const int motorEnablePin = 5;      // pin 1 on L293D
const int buzzerPin = 11; // buzzer pin, used 100 ohm 
const int servoPin = 13; // servo motor pin
const int tempSensorPin = 6;

DHT dht(tempSensorPin, TEMP_SENSOR_TYPE); // Declaring DHT connection and type
LiquidCrystal_I2C lcd2(0x27, 16, 2); // I2C LCD
Servo servo;

void setup() {
  pinMode(motorOutputPin1, OUTPUT);  
  pinMode(motorOutputPin2, OUTPUT);
  pinMode(motorEnablePin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(gasSensorPin, INPUT); 
  pinMode(airsensorPin, INPUT);
  servo.attach(servoPin);

  Serial.begin(9600);

  dht.begin();     // Initialises DHT sensor
  
  // LCD I2C initialisation
  lcd2.init();
  lcd2.backlight();
  lcd2.print("Gas sensor");
  lcd2.setCursor(0,1);
  lcd2.print("warming up!");

  //delay(10000); // MQ2 needs to warm up
  lcd2.clear(); // Clear LCD2
}

void loop() {
  // read in values from sensors
  float tempReading = dht.readTemperature(); // Reading the temperature in Celsius from DHT11

  float airReading = analogRead(airsensorPin); // Reading MQ135 air quality
  float gasReading = analogRead(gasSensorPin);  // Reading MQ2 gas levels
  int fanSpeed = map(tempReading, MIN_TEMP, MAX_TEMP, 0, MAX_FAN_SPEED);
  fanSpeed = constrain(fanSpeed, 0, MAX_FAN_SPEED);
  // shifting percentage to suit our upper range
  float adjustedSpeed = fanSpeed - MIN_FAN_SPEED;
  float speedpercent = (adjustedSpeed / double(MAX_FAN_SPEED - MIN_FAN_SPEED)) * double(100);
  speedpercent = constrain(speedpercent, 0, 100);


  // Send data to server 
  String readings = String("{\"gas\":") + gasReading + 
                    String(",\"air\":") + airReading + 
                    String(",\"temp\":") + tempReading + 
                    String(",\"speed\":") + speedpercent +
                    String("}");
  Serial.println(readings);
  // ensure entire string gets sent
  delay(300);

  control_fan(fanSpeed); // changes fan speed based on temp

  check_gas(gasReading); // checks gas level and triggers buzzer
  update_display(airReading); // updates lcd to air quality reading and gives status

  delay(1000); // this is delaying reading

}

// control fan speed based on temperature
void control_fan(int fanSpeed) {
  // PWM to the enable pin to alter speed
  if (fanSpeed > MIN_FAN_SPEED) {
    analogWrite(motorEnablePin, fanSpeed);
    servo_rotate(); // rotate servo back and forth
  } else {
    // fan and servo stationary
    analogWrite(motorEnablePin, 0);
  }
 
  // to drive the motor in clockwise direction
  digitalWrite(motorOutputPin1, LOW);
  digitalWrite(motorOutputPin2, HIGH);
}

// checks gas level
void check_gas(float gasReading) {

  if (gasReading > GAS_LIMIT) {
    // Buzzer sounds based on gas level 
    int frequency = map(gasReading, 300, 1023, 500, 2000);
    tone(buzzerPin, frequency, 2000); 

  } else {
    // Stop the buzzer
    noTone(buzzerPin);
  }
}

// updates air quality and gives air quality status
void update_display(float airReading) {

  if (airReading > AIR_LIMIT) {
    lcd2.setCursor(0, 0);
    lcd2.print("Bad air quality!");
    lcd2.setCursor(0, 1);
    lcd2.print(airReading);
    lcd2.print(" ppm             ");
  }

  else {
    lcd2.setCursor(0, 0);
    lcd2.print("Air quality good");
    lcd2.setCursor(0, 1);
    lcd2.print(airReading);
    lcd2.print(" ppm             ");
  }
}


// make servo rotate 180 degrees back and forth
void servo_rotate() {
  int pos;
  for (pos = 0; pos <= 180; pos += 1) { 
    servo.write(pos);              
    delay(10);                  
  }
  for (pos = 180; pos >= 0; pos -= 1) { 
    servo.write(pos);              
    delay(10);                     
  }
}
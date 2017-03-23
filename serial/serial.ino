#define RELAY4 13
#define RELAY3 12
#define RELAY2 11
#define RELAY1 10

#define LOCK_VALVES -1

#define ON HIGH
#define OFF LOW


#define TRIGGER_DELAY 8000

#define COLLECTION_DELAY 8000             // Use Collection Delay to adjust the time valves are open

#define MAX_VALVES 2                      // Use max valves to adjust the system size



//String readString;
int max_offset;
int offset;
int current_relay;

//Used to block polling
long seconds;
long current_time;


void setup()
{

  max_offset = MAX_VALVES - 1;
  
  offset = 0;
  
  while( offset <  MAX_VALVES ){

    current_relay = RELAY1 + offset;
    
    pinMode( current_relay, OUTPUT);
    
    offset++;
    
  }
   
  seconds = 0; 
  
  //pinMode(RELAY2, OUTPUT);
  //pinMode(RELAY3, OUTPUT);
  //pinMode(RELAY4, OUTPUT);
  
  // initialize serial communications at 9600 bps
  Serial.begin(9600);             


  offset = 0;
  current_relay = 0;  

}

void loop() {
  // put your main code here, to run repeatedly:
  
    delay(100);
  
    
      if ( Serial.available() ){
  
        
        char c = Serial.read();  //gets one byte from serial buffer
        //readString += c; //makes the string readString
              

        
        if(c == 'N' && offset != LOCK_VALVES ){        //Open next valve in series
          
          //Check to be sure the next collection signal isn't to soon.
          current_time = millis();
          long time_difference = current_time - seconds; 
          
          if( time_difference > TRIGGER_DELAY ){
            
            current_relay = RELAY1+offset;
            digitalWrite( current_relay, ON );              // Turns ON the current Relay
            delay( COLLECTION_DELAY );
            digitalWrite( current_relay, OFF );  
            offset++;

            //Reset the delay difference
            seconds = millis();

            
            if( offset > max_offset ){
              offset = LOCK_VALVES; // Lock all valves
            }
            
          }
          
        }else if( c == 'R' ){                           //Close all Valves
          
          offset = 0;
          while( offset < MAX_VALVES ){
            current_relay = RELAY1 + offset;
            digitalWrite( current_relay, OFF );               // Turns OFF all Relays
            delay(10);
            offset++;
          }
          
          offset = 0;
          
        }else if( c == 'A' ){                          //Open All Valves
          offset = 0;
          while( offset < MAX_VALVES ){
            current_relay = RELAY1 + offset;
            
            digitalWrite( current_relay, ON );              // Turns ON all Relays
            delay(10);
            offset++;
          }
        }

        
        
     }
  
  
}



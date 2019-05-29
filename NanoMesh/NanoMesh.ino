#include "config.h"

void reciveMessage();
void sendMessage(payload_t payload);
void testFunction();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  radio.begin();
  Serial.println("<START>");
  radio.openReadingPipe(1,addresses[0]);
  radio.openWritingPipe(addresses[0]); 
  radio.startListening();
};

void loop() {
  // put your main code here, to run repeatedly:
  if(radio.available()) reciveMessage();
  //If there is new message to send - send it
  if(Serial.available()>0){ 
    String command = Serial.readStringUntil('\n');
    if(command == "<SEND>"){
        payload_t payload;
        while(!(Serial.available()>0)){};
            payload.dest = (uint8_t)Serial.readStringUntil('\n').substring(2).toInt();
        while(!(Serial.available()>0)){};
          Serial.readStringUntil('\n').substring(2).toCharArray(payload.data,sizeof(payload.data));
        while(!(Serial.available()>0)){};
            payload.Msg_Id = (uint32_t)Serial.readStringUntil('\n').substring(2).toInt();
        payload.src = NodeId;
        sendMessage(payload);
    }
    if(command == "<SET_NODE_ID>"){
        while(!(Serial.available()>0)){};        
        NodeId = Serial.readStringUntil('\n').toInt();
        Serial.print("<CHANGE_ID> ");
        Serial.println(NodeId);
    }
  
  }
  testFunction();
  delay(100);
};


void reciveMessage(){
  payload_t payload;
  radio.read(&payload,sizeof(payload_t));
  if(!msgIdQueue.isExist(payload.Msg_Id)){
    msgIdQueue.enQueue(payload.Msg_Id);    
    if(payload.dest%3 == 0 && payload.src != NodeId && NodeId%3 == 0){                                 //If it's for me - insert to PI
      Serial.print("<NEW_MSG>,");
      Serial.print("<MSG_ID> ");
      Serial.print(payload.Msg_Id);
      Serial.print(",<SRC> ");
      Serial.print(payload.src);
      Serial.print(",<DATA> ");
      Serial.print(payload.data);
      Serial.println(",<END_MSG>");    
    }
    else{                                             //If not - check if I allready get it - if no, broadcast the message again
      radio.stopListening();
      delay(100);
      radio.write(&payload,sizeof(payload_t),1);
      delay(100);
      radio.startListening();
    }
  }
};

void sendMessage(payload_t payload){
  if(payload.dest != NodeId){
    radio.stopListening();
    delay(100);
    radio.write(&payload,sizeof(payload_t),1);
    delay(100);
    radio.startListening();  
  }
};

int msgId = 0;
int count = 0;
void testFunction(){
  if(millis()-testTimer > 1000){
/*    
    testTimer = millis();
    payload_t payload;
    payload.Msg_Id = msgId++;
    payload.src = NodeId;
    payload.dest = 0;
    if(count%4 == 0)
      strcpy(payload.data,"G:34.12245:32.15375");
    if(count%4 == 1)
      strcpy(payload.data,"P:120");
    if(count%4 == 2)
      strcpy(payload.data,"A:12.23,23.21,2.0");
    if(count%4 == 3)
      strcpy(payload.data,"F:False");
    sendMessage(payload);*/
  }
};

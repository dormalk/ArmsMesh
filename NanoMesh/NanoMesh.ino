#include "config.h"

void reciveMessage();
void sendMessage(payload_t payload);
void testFunction();
void createAllAudio();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  radio.begin();
  Serial.println("<START>");
  radio.openReadingPipe(1,addresses[0]);
  radio.openWritingPipe(addresses[0]); 
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_2MBPS);
  radio.startListening();  
}

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
    if (command == "<AUDIO>"){
        Serial.println("<OK?>");
        createAllAudio();
    }
    if (command == "<END AUDIO>"){
        rx_audio = false;
    }
  }
  testFunction();
//  delay(100);
};

void createAllAudio(){
  static int id = 1;
  payload_t payloadAudio;
  for(int i = 0; i < 240; i++){
        while(!(Serial.available()>0)){}
        Serial.readBytes(payloadAudio.data,22);
        payloadAudio.Msg_Id = id++;
        payloadAudio.dest = -1;
        payloadAudio.src = NodeId;
        sendMessage(payloadAudio);
        payloadAudio.data[21] = '\n';
        if(strstr(payloadAudio.data,"REC") != NULL) {
          for(int i = 0; i < 15; i++)
            sendMessage(payloadAudio);
         break;
        }
//        delay(100);
  }
}
void reciveMessage(){
  payload_t payload;
  radio.read(&payload,sizeof(payload_t));
  if(!msgIdQueue.isExist(payload.Msg_Id)){
    msgIdQueue.enQueue(payload.Msg_Id);
    if(payload.dest != 255 && payload.dest%10 == 0 && payload.src != NodeId && NodeId%10 == 0){                                 //If it's for me - insert to PI
      Serial.print("<NEW_MSG>,");
      Serial.print("<MSG_ID> ");
      Serial.print(payload.Msg_Id);
      Serial.print(",<SRC> ");
      Serial.print(payload.src);
      Serial.print(",<DATA> ");
      Serial.print(payload.data);
      Serial.println(",<END_MSG>");    
    }
    else if(payload.src != NodeId){                                             //If not - check if I allready get it - if no, broadcast the message again
      if (payload.dest == 255){                       //if it audio
        rx_audio = true;
        //Serial.println("<NEW_AUDIO>");
        //Serial.print("<MSG_ID>");
        //Serial.println(payload.Msg_Id);
        //Serial.print("<SRC>");
        //Serial.println(payload.src);
        //Serial.print("<DEST>");
        //Serial.println(payload.dest);
        Serial.println("<AUDIO_DATA>");
        Serial.write(payload.data,22);
        //Serial.println("<END_NEW_AUDIO>");
      }
      if(!rx_audio){
        radio.stopListening();
        radio.write(&payload,sizeof(payload_t),1);
        //delay(100);
        radio.startListening();        
      }
    }
  }
};

void sendMessage(payload_t payload){
  if(payload.dest != NodeId){
    if(!rx_audio){
      radio.stopListening();
      //delay(100);
      Serial.print(payload.dest);
      radio.write(&payload,sizeof(payload_t));
      //delay(100);
      radio.startListening();  
    }
  }
};


int msgId = 0;

int count = 0;

const char* gps[6] = {"G:34.12245:34.15375","G:34.12345:34.15375","G:34.13245:34.15375","G:34.14245:34.15375","G:34.15245:34.15375","G:34.16245:34.15375"};
const char* puls[7] = {"P:98","P:80","P:120","P:89","P:85","P:80","P:100"};

void testFunction(){
  if(millis()-testTimer > 1000){
    Serial.println(NodeId);
    testTimer = millis();
    payload_t payload;
    payload.Msg_Id = msgId++;
    payload.src = NodeId;
    payload.dest = 0;
    if(count%4 == 0)
      strcpy(payload.data,gps[count%6]);
    if(count%4 == 1)
      strcpy(payload.data,"A:12.12:13.12:15.15");
    if(count%4 == 2)
      strcpy(payload.data,"E:False");
    if(count%4 == 3)
      strcpy(payload.data,puls[count%7]);
    Serial.println(payload.data);
    count++;
    sendMessage(payload);
  }
}

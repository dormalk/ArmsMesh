#include "msgQueue.h"

MsgQueue::MsgQueue(){
  capacity = 0;
  dequeueTimer = 0;
}

void MsgQueue::enQueue(uint8_t id){
  #if defined DEBUG_MODE
    Serial.print("DEBUG -> Enqueue id: ");
    Serial.println(id);
  #endif
  autoDeQueue();
  if(capacity < MAX_QUEUE_SIZE-1){
    msgQueue[capacity] = id;
    capacity++;
  }
  else{
    deQueue();
    msgQueue[capacity] = id;
    capacity++;
  }
};

uint8_t MsgQueue::deQueue(){
  uint8_t id = msgQueue[0];
  #if defined DEBUG_MODE
    Serial.print("DEBUG -> Dequeue id: ");
    Serial.println(id);
  #endif
  for(int i = 1; i< capacity; i++){
    msgQueue[i-1] = msgQueue[i];
  };
  capacity --;
  return id;
};

bool MsgQueue::isEmpty(){
  if(capacity == 0){
    #if defined DEBUG_MODE
      Serial.println("DEBUG -> QUEUE: Empty");
    #endif
    return true;
  }
  #if defined DEBUG_MODE
    Serial.println("DEBUG -> QUEUE: Not empty");
  #endif
  return false;
};

void MsgQueue::clearQueue(){
  #if defined DEBUG_MODE
    Serial.println("DEBUG -> QUEUE: Cleared");
  #endif
  while(!isEmpty()){
    deQueue();
  }
}

bool MsgQueue::isExist(uint8_t msg_id){
  for(int i = 0; i < capacity; i++)
    if(msgQueue[i] == msg_id){
      #if defined DEBUG_MODE
        Serial.print("DEBUG -> Msg: ");
        Serial.print(msg_id);
        Serial.println(" found");
      #endif
      return true;
    }
  #if defined DEBUG_MODE
    Serial.print("DEBUG -> Msg: ");
    Serial.print(msg_id);
    Serial.println(" not found");
  #endif  
  return false;
};


void MsgQueue::autoDeQueue(){
  if(millis() - dequeueTimer > 2000){
    dequeueTimer = millis();
    if(!isEmpty()) deQueue();
  }
}

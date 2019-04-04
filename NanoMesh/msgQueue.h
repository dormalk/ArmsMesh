#ifndef MSG_QUEUE_H
#define MSG_QUEUE_H

#define MAX_QUEUE_SIZE 32
#include <Arduino.h>
//#define DEBUG_MODE

class MsgQueue{
  private:
    uint16_t msgQueue[MAX_QUEUE_SIZE];
    int capacity;
    int dequeueTimer;
  public:
    MsgQueue();
    void enQueue(uint8_t str);
    uint8_t deQueue(void);
    bool isEmpty(void);  
    void clearQueue();
    bool isExist(uint8_t msg_id);
    void autoDeQueue();
};





#endif

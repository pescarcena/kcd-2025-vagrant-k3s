from bcc import BPF

import ctypes as ct
# Must match the C “#define MAX_DATA_SIZE 4096”
MAX_DATA_SIZE = 4096

#TASK_COMM_LEN = 16
SOCKETS = {}

bpf_text = """

#include <linux/ptrace.h>

enum event_type {
    CONNECTED,
    DATA_SENT,
    CLOSED,
};
#pragma once

#define MAX_DATA_SIZE 4096


BPF_PERF_OUTPUT(tls_events);

/***********************************************************
 * Internal structs and definitions
 ***********************************************************/

// Key is thread ID (from bpf_get_current_pid_tgid).
// Value is a pointer to the data buffer argument to SSL_write/SSL_read.
BPF_HASH(active_ssl_read_args_map, uint64_t, const char*);
BPF_HASH(active_ssl_write_args_map, uint64_t, const char*);

// BPF programs are limited to a 512-byte stack. We store this value per CPU
// and use it as a heap allocated value.
//BPF_PERCPU_ARRAY(data_buffer_heap, struct ssl_data_event_t, 1);

/***********************************************************
 * General helper functions
 ***********************************************************/



/***********************************************************
 * BPF syscall processing functions
 ***********************************************************/



struct data_t {
    u32 tgid;                // Thread ID
    int fdf;                 // Socket File Descriptor
    char data[256];// The current process name
    u32 ip_addr;             // IP Address
    int ret;                 // Return Value
    enum event_type type;    // Event Type
    char comm[16];
};

/***********************************************************
 * BPF probe function entry-points
 ***********************************************************/
//BPF_HASH(infotmp, u32, struct send_info_t );


struct send_info_t {
    u32 tgid;
    int fdf;
    char data[256];
    char comm[16];
};

BPF_HASH(infotmp, u32, struct send_info_t );
//BPF_HASH(infotmp2, u32, const char*);






int syscall__sendto(struct pt_regs *ctx, int sockfd, void *buf, size_t len, int flags, struct sockaddr *dest_addr, int addrlen) {
    u32 tgid = bpf_get_current_pid_tgid();
    struct send_info_t info = {};
    //const char* buf2 = (const char*)PT_REGS_PARM2(ctx);

        bpf_get_current_comm(&info.comm, sizeof(info.comm));
        // Set Thread ID
        info.tgid = tgid;
        // Set Socket File Descriptor
        info.fdf = sockfd;
        //const char* buf2 = (const char*)PT_REGS_PARM2(ctx);
        //info.data = &buf2
        //bpf_probe_read(&info.comm, 256, &buf);
        // Update temporary data map
        const char* buf2 = (const char*)buf;
        //info.data = &buf2;
        bpf_probe_read(&info.data, 256, &buf2);
        infotmp.update(&tgid, &info);

        //infotmp2.update(&tgid, &buf2);


    return 0;
}

int trace_return(struct pt_regs *ctx)
{
    u32 tgid = bpf_get_current_pid_tgid();

    struct data_t data = {};
    struct send_info_t *infop;

    // Lookup the entry for our sendto
    infop = infotmp.lookup(&tgid);
    //const char** infop2 = infotmp2.lookup(&tgid);
    if (infop == 0) {
        // missed entry
        return 0;
    }
    //if (infop2 == NULL) {
     //process_SSL_data(ctx, current_pid_tgid, kSSLWrite, *buf);
    //   return 0;
    //}

    const char** infop3 = infop->data;
    // Set Thread ID
    data.tgid = infop->tgid;
    // Set Socket File Descriptor
    data.fdf = infop->fdf;
    bpf_probe_read(&data.data, 256, *infop3);
    bpf_probe_read_kernel(&data.comm, 16, infop->comm);
    // Assign the amount of data sent to the ret field, as obtained from the register context
    data.ret = PT_REGS_RC(ctx);
    data.type = DATA_SENT;
    // Submit data to user space
    tls_events.perf_submit(ctx, &data, sizeof(data));
    // Delete temporary entry
    infotmp.delete(&tgid);
    //infotmp2.delete(&tgid);
    return 0;
}

"""
import time

# Load the eBPF program
b = BPF(text=bpf_text)

# Attach the uprobe to the 'main' function of /bin/ls
#b.attach_kprobe(event=b.get_syscall_fnname("sendto"), fn_name="probe_entry_write")
#b.attach_kretprobe(event=b.get_syscall_fnname("sendto"), fn_name="probe_ret_write")
sendto_e = b.get_syscall_fnname("sendto").decode()
b.attach_kprobe(event=sendto_e, fn_name="syscall__sendto")
b.attach_kretprobe(event=sendto_e, fn_name="trace_return")
#b.attach_kprobe(event=b.get_syscall_fnname("recvfrom"), fn_name="probe_entry_SSL_read")
#b.attach_kretprobe(event=b.get_syscall_fnname("recvfrom"), fn_name="probe_ret_SSL_read")

class SocketInfo(ct.Structure):
    _fields_ = [
        ("tgid", ct.c_uint32),
        ("fdf", ct.c_int),
        ("data", ct.c_char * 256),
        ("ip_addr", ct.c_uint32),
        ("ret", ct.c_int),
        ("type", ct.c_uint),
        ("comm", ct.c_char * 16),
    ]

def print_event(cpu, data, size):
    # cast the raw perf‐buffer blob into our Python struct
    #print(size)
    e = ct.cast(data, ct.POINTER(SocketInfo)).contents
    print(f"The process: {e.comm} produced the data: {e.data} with pid-{e.tgid} sent {e.ret} bytes through socket FD: {e.fdf}")
    # only print the part of the buffer that's valid
    #print(bytes(event))
    print(bytes(e))
    #print(f"[{event.timestamp_ns}] PID={event.pid} TID={event.tid} "
    #      f"{'READ' if event.type==0 else 'WRITE'} len={event.data_len}\n"
    #      f"    {buf!r}")
    #print(bytes(e))
b["tls_events"].open_perf_buffer(print_event)
while True:
   b.perf_buffer_poll()
/*
**  Copyright (C) - Triton
**
**  This program is under the terms of the LGPLv3 License.
*/

#ifndef TRITON_SYSCALLS_H
#define TRITON_SYSCALLS_H

#ifdef __APPLE__
  #include <sys/syscall.h>
#else
  #include <asm/unistd_64.h>
#endif

extern const unsigned int NB_SYSCALL;
extern const char *syscallmap[];

#endif // SYSCALLS_H

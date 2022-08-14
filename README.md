# coen346-MMU
A memory manager unit simulation: simulating operating system's virtual memory management and concurrency control.

## Description
The virtual memory being managed consists of a main memory and a large disk space. Both are divided/organized into ‘pages’. The number of pages of the main memory is limited while disk space has unlimited number of pages. Each page stores a variable in the form (id, value), where id is the identifier of the variable and value is the value associated with the variable. To manage (store, search, and remove) variables, the virtual memory manager offers three APIs to the processes: 

- Store (string variableId, unsigned int value): This instruction stores the given variable id and its value in the first unassigned spot in the memory.

- Release (string variableId): This instruction removes the variable id and its value from the memory so the page which was holding this variable becomes available for further storage.

- Lookup (string variableId): This instruction checks if the given variableId is stored in the memory and returns its value or -1 if it does not exist. If the Id exists in the main memory it returns its value. If the Id is not in the main memory but exists in disk space (i.e. page fault occurs), then it should move this variable into the memory and release the assigned page in the virtual memory. Notice that if no spot is available in the memory, program 
needs to swap this variable suggested by the LRU-K algorithm. LRU-K algorithm works as follows:

1. for each page in the main memory two types of information are maintained: 
    1. a variable that holds the time stamp of the last access to this page, we call it LAST(p). 
    2. A list of the time stamps of the last K accesses to this page, we call it HIST(p) where HIST(p)[1] is the last time the page was accessed and HIST(p)[2] is the time of the access before last, etc.

2. Every time the page is accessed, the memory manager compares the difference of the time stamp of that access and the time stamp of the last access with a pre-defined time-out: 
    1. If the difference is less than the time-out, only LAST(p) is updated to the 
    time stamp of this access. 
    2. If the difference is more than the time-out, LAST(p) and HIST(p) are 
    updated as follows (these steps need to be done in this exact order): 
    - Lcp = LAST(p) – HIST(p)[1] 
    - For i, K>=i>1: HIST(p)[i] = HIST(p)[i-1] + Lcp
    - LAST(p)=HIST(p)[1]=time of this last access

3. When a page replacement is needed, the page to be replaced is chosen as follows: 
    1. Of all the pages that have LAST(p)-HIST(p)[1] > time-out, chose the one with the minimum value of HIST(p)[k]. 
    2. In case of a tie between two pages (both satisfy LAST(p)-HIST(p)[1]>time-out and they have the same value for HIST(p)[k]), OR none of the pages satisfies LAST(p)-HIST(p)[1]>time-out, chose the page with the smallest value of HIST(p)[1]. 

4. When a page is first used, or just was replaced, its associated information is initialized as follows
    1. LAST(p), and HIST(p)[1] are set to the time stamp of that usage/replacement. 
    2. HIST(p)[i], for i, 1<i<K, are set to zero. 
 
## Implementation Requirements
- Processes should be simulated by threads. Each process has a starting time and total duration. The thread simulating the process (one thread per process) should run for a time equal to the duration of its associated process as indicated in the input. It should start the first time the scheduler is supposed to schedule its associated process (when its arrival time has come, and there is at most one process in the CPU at the time). The algorithm used to schedule the processes is FIFO (First In, First Out). Note that the maximum number of processes that can run at the same time equals the number of cores.

## Dependencies
- `python3`
- `poetry` for python virtual environment

## Running the MMU

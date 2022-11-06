#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>

/* define all scheme constants */
#define bool_f          0x2F
#define bool_t          0x6F
#define num_mask        0x03
#define num_tag         0x00
#define num_shift          2
#define char_mask       0xFF
#define char_tag        0x0F
#define char_shift         8
#define empty_list      0x3F

/* all scheme values are of types ptrs */
typedef unsigned int ptr;

static void print_ptr(ptr x) {
    if ((x & num_mask) == num_tag) {
        printf("%d", ((int)x) >> num_shift);
    } else if (x == bool_f) {
        printf("#f");
    } else if (x == bool_t) {
        printf("#t");
    } else if (x == empty_list) {
        printf("()");
    } else if ((x & char_mask) == char_tag) {
        printf("\\#%c", x >> char_shift);
    } else {
        printf("#<unknown 0x%08x>", x);
    }
    printf("\n");
}

static char* allocate_protected_space(int size) {
    int page = getpagesize(); // returns 4096
    int status;
    int aligned_size = ((size + page - 1) / page) * page;
    /*
    mmap()
    We use this function to map the process address space and either the devices or files.
    It takes six arguments:

    void* mmap (
        void *address,
        size_t length,
        int protect,
        int flags,
        int filedes,
        off_t offset
    )

    1. address: It provides the preferred starting address used for mapping. If there is no other mapping, the kernel will pick the nearby page boundary, creating a mapping.
    2. length: The bytes’ number is mapped.
    3. protect: It controls what type of access is allowed. For instance, the PROT_READ for reading access, the PROT_WRITE for write access, and the PROT_EXEC for execution.
    4. flags:  It is used for controlling the map’s nature. Some of the common and useful flags are listed below:
        - MAP_SHARED - share mapping with other processes.
        - MAP_FIXED - The system is forced to use the same mapping address given via the address parameter.
        - MAP_ANONYMOUS / MAP_ANON - It creates anonymous mapping.
        - MAP_PRIVATE - The mapping would be private and not visible to others while using this flag.
    5. filedes: The file descriptor is supposed to be mapped.
    6. offset: The file mapping starts from this offset.
    */
    char* p = mmap(0, aligned_size + 2 * page, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);
    if (p == MAP_FAILED) {
        printf("Mapping Failed\n");
    }

    /*
    The mprotect() function changes the access protections on the mappings specified by the len up 
    to the next multiple of the page size

        PROT_READ  — page can be read
        PROT_WRITE — page can be written
        PROT_EXEC  — page can be executed
        PROT_NONE  — page cannot be accessed

    Return value
    If successful, mprotect() returns 0.
    If unsuccessful, mprotect() returns -1 and sets errno to one of the following values:
    */
    status = mprotect(p, page, PROT_NONE);
    if (status != 0) {
        printf("Low Stack Page Protection Failed\n");
    }

    status = mprotect(p + page + aligned_size, page, PROT_NONE);
    if (status != 0) {
        printf("High Stack Page Protection Failed\n");
    }

    return (p + page);
}

static void deallocate_protected_space(char* p, int size) {
    int page = getpagesize();
    int status;
    int aligned_size = ((size + page - 1) / page) * page;
    status = munmap(p - page, aligned_size + 2 * page);
    if (status != 0) {
        printf("Deallocation failed.\n");
    }
}

int main(int argc, char** argv) {
    int stack_size = (16 * 4096); /* holds 16K cells */
    char* stack_top = allocate_protected_space(stack_size);
    char* stack_base = stack_top + stack_size;
    print_ptr(entry_point(stack_base));
    deallocate_protected_space(stack_top, stack_size);
    return 0;
}
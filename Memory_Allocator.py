#include <stdlib.h> // for size_t and NULL
#include <stddef.h> // for size_t and NULL
#include <stdio.h> // for printf

// Defines a structure for the memory block header
typedef struct memoryBlockHeader {
     int size; // size of the reserved block
     struct memoryBlockHeader* next;  // Pointer to the next block in the integrated free list
} memoryBlockHeader;

// Define heap size
#define HEAP_SIZE (128*8)
unsigned char heap[HEAP_SIZE]; // heap memory

memoryBlockHeader* freeListHead; // Pointer to first free memory block header in heap
// comment
// initializes the memory allocator
void duInitMalloc() {
    // Initialize all the memory in the heap to 0
    for (int i = 0; i < HEAP_SIZE; i++) {
        heap[i] = 0;
    }
    // Make the whole heap be one large free block
    memoryBlockHeader* currentBlock = (memoryBlockHeader*)heap;
    currentBlock->size = HEAP_SIZE - sizeof(memoryBlockHeader);
    currentBlock->next = NULL;

    // Set the freeListHead to point to this block header
    freeListHead = currentBlock;
}

// prints the memory blocks in the free list
void duMemoryDump() {
    memoryBlockHeader* current = freeListHead;

    printf("MEMORY DUMP\n");
    printf("Free List\n");

    // Loop through the free list and print each block's address and size
    while (current != NULL) {
        printf("Block at %p, size %d\n", (void*)current, current->size);
        current = current->next;
    }
}

// tries to allocate a block of memory of the given size. If succeeds, returns a pointer to the memory. If fails, it returns NULL.
void* duMalloc(size_t size) {
    // Round up the size to the nearest multiple of 8
    size = (size + 7) & ~7;

    memoryBlockHeader* current = freeListHead;
    memoryBlockHeader* previous = NULL;

    // Find a free block that can accommodate the requested size
    while (current != NULL && current->size < size + sizeof(memoryBlockHeader)) {
        previous = current;
        current = current->next;
    }

    // If no block can accommodate the request, return NULL
    if (current == NULL) {
        return NULL;
    }

    // If the found block can be split into two
    if (current->size >= size + sizeof(memoryBlockHeader) + 1) {
        memoryBlockHeader* newBlock = (memoryBlockHeader*)((unsigned char*)current + sizeof(memoryBlockHeader) + size);
        newBlock->size = current->size - sizeof(memoryBlockHeader) - size;
        newBlock->next = current->next;

        if (previous != NULL) {
            previous->next = newBlock;
        } else {
            freeListHead = newBlock;
        }
        current->size = size;
    } else { // The block is a perfect fit
        if (previous != NULL) {
            previous->next = current->next;
        } else {
            freeListHead = current->next;
        }
    }

    // Return a pointer to the memory region after the header
    return (void*)((unsigned char*)current + sizeof(memoryBlockHeader));
}

// duFree function frees a block of memory, adding it back to the free list
void duFree(void* ptr) {
    // Find the start of the block header
    memoryBlockHeader* blockToFree = (memoryBlockHeader*)((unsigned char*)ptr - sizeof(memoryBlockHeader));

    // Add the block to the free list in memory order
    memoryBlockHeader* current = freeListHead;
    memoryBlockHeader* previous = NULL;

    while (current != NULL && current < blockToFree) {
        previous = current;
        current = current->next;
    }

    if (previous != NULL) {
        previous->next = blockToFree;
    } else {
        freeListHead = blockToFree;
    }

    blockToFree->next = current;
}

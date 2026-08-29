void memcpy(void* src, void* dst, unsigned int bytes) {
    for (unsigned int i = 0; i < bytes; i++) {
        ((char*)dst)[i] = ((char*)src)[i];
    }
}

int main() {
    const char* msg = "Hello, World!";

    // if the stack manages to grow to be 1MB, I'll be quite suprised.
    const volatile char* somewhere_in_memory = (const volatile char*)0x100;
    
    memcpy((void*)msg, (void*)somewhere_in_memory, 14);

    return somewhere_in_memory[0];
}
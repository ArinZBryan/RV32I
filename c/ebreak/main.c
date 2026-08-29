void memcpy(void* src, void* dst, unsigned int bytes) {
    for (unsigned int i = 0; i < bytes; i++) {
        ((char*)dst)[i] = ((char*)src)[i];
    }
}

int main() {
    
    volatile char* signal = (volatile char*)0x140;
    memcpy("ebreak", (void*)signal, 7);
    asm ("ebreak");
    memcpy("nobreak", (void*)signal, 8);

    return 0;
}
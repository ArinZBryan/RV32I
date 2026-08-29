#include <stdint.h>

int test_r() {
    int tests_passed = 0;
    int tests_failed = 0;

    int a;
    int b;
    int c;

    // add
    a = 2;
    b = 3;
    c = a + b;
    if (c == 5) { tests_passed++; } else { tests_failed++; }

    // sub
    a = 3;
    b = 2;
    c = a - b;
    if (c == 1) { tests_passed++; } else { tests_failed++; }

    // xor
    a = 0b1100;
    b = 0b1010;
    c = a ^ b;
    if (c == 0b0110) { tests_passed++; } else { tests_failed++; }

    // and
    c = a & b;
    if (c == 0b1000) { tests_passed++; } else { tests_failed++; }

    // or
    c = a | b;
    if (c == 0b1110) { tests_passed++; } else { tests_failed++; }

    // sll
    a = 1;
    b = 2;
    c = a << b;
    if (c == 4) { tests_passed++; } else { tests_failed++; }

    // srl
    unsigned int ua = 8;
    unsigned int ub = 2;
    unsigned int uc = ua >> ub;
    if (uc == 2) { tests_passed++; } else { tests_failed++; }
    
    // sra
    a = -1;
    b = 2;
    c = a >> b;
    if (c == -1) { tests_passed++; } else { tests_failed++; }

    // slt
    a = -1;
    b = -2;
    c = a < b;
    if (c == 0) { tests_passed++; } else { tests_failed++; }

    // sltu
    ua = 1;
    ub = 2;
    uc = ua < ub;
    if (uc == 1) { tests_passed++; } else { tests_failed++; }

    return tests_passed & 0xffff | (tests_failed & 0xffff << 16);
}

int test_i_maths() {
    int tests_passed = 0;
    int tests_failed = 0;

    int a;
    int b;
    int c;

    // add
    a = 2;
    c = a + 3;
    if (c == 5) { tests_passed++; } else { tests_failed++; }

    // sub
    c = a - 2;
    if (c == 1) { tests_passed++; } else { tests_failed++; }

    // xor
    a = 0b1100;
    c = a ^ 0b1010;
    if (c == 0b0110) { tests_passed++; } else { tests_failed++; }

    // and
    c = a & 0b1010;
    if (c == 0b1000) { tests_passed++; } else { tests_failed++; }

    // or
    c = a | 0b1010;
    if (c == 0b1110) { tests_passed++; } else { tests_failed++; }

    // sll
    a = 1;
    c = a << 2;
    if (c == 4) { tests_passed++; } else { tests_failed++; }

    // srl
    unsigned int ua = 8;
    unsigned int uc = ua >> 2;
    if (uc == 2) { tests_passed++; } else { tests_failed++; }
    
    // sra
    a = -1;
    c = a >> 2;
    if (c == -1) { tests_passed++; } else { tests_failed++; }

    // slt
    a = -1;
    c = a < (-2);
    if (c == 0) { tests_passed++; } else { tests_failed++; }

    // sltu
    ua = 1;
    uc = ua < 2;
    if (uc == 1) { tests_passed++; } else { tests_failed++; }

    return tests_passed & 0xffff | (tests_failed & 0xffff << 16);
}

int test_i_loads_lui() {
    int tests_passed = 0;
    int tests_failed = 0;

    // lw
    int32_t mem = 0b01001001010101011001001010101010;

    int32_t*  wptr  =             &mem;
    int16_t*  hptr  = (int16_t*)  &mem;
    int8_t*   bptr  = (int8_t*)   &mem;
    uint16_t* uhptr = (uint16_t*) &mem;
    uint8_t*  ubptr = (uint8_t*)  &mem;

    int32_t lw = *wptr;
    int16_t lh = *hptr;
    int8_t lb = *bptr;
    uint16_t lhu = *uhptr;
    uint8_t lbu = *ubptr;

    if ((int32_t)lw == 1230344874) { tests_passed++; } else { tests_failed++; }
    if ((int32_t)lh == -27990) { tests_passed++; } else { tests_failed++; }
    if ((int32_t)lb == -86) { tests_passed++; } else { tests_failed++; }
    if ((int32_t)lhu == 37546) { tests_passed++; } else { tests_failed++; }
    if ((int32_t)lbu == 170) { tests_passed++; } else { tests_failed++; }

    return tests_passed & 0xffff | (tests_failed & 0xffff << 16);
}

int test_s_lui() {
    int tests_passed = 0;
    int tests_failed = 0;
    
    volatile int32_t* memw = (volatile int32_t*)0xe00;
    volatile int16_t* memh = (volatile int16_t*)0xe04;
    volatile int8_t* memb = (volatile int8_t*)0xe08;

    *memw = 0x12345678;
    *memh = 0x1234;
    *memb = 0x12;

    if (*memw == 0x12345678) { tests_passed++; } else { tests_failed++; }
    if (*memh == 0x1234) { tests_passed++; } else { tests_failed++; }
    if (*memb == 0x12) { tests_passed++; } else { tests_failed++; }

    return tests_passed & 0xffff | (tests_failed & 0xffff << 16);
}

int test_b() {
    int tests_passed = 0;
    int tests_failed = 0;

    int a = -1;
    int b = -1;
    int c = 2;
    
    unsigned int ua = 1;
    unsigned int ub = 1;
    unsigned int uc = 2;

    if (a == b) { tests_passed++; } else { tests_failed++; }
    if (a == c) { tests_failed++; } else { tests_passed++; }
    if (a != b) { tests_failed++; } else { tests_passed++; }
    if (a != c) { tests_passed++; } else { tests_failed++; }
    if (a < b)  { tests_failed++; } else { tests_passed++; }
    if (a < c)  { tests_passed++; } else { tests_failed++; }
    if (a >= b) { tests_passed++; } else { tests_failed++; }
    if (a >= c) { tests_failed++; } else { tests_passed++; }
    if (c >= a) { tests_passed++; } else { tests_failed++; }
    
    if (ua < ub)  { tests_failed++; } else { tests_passed++; }
    if (ua < uc)  { tests_passed++; } else { tests_failed++; }
    if (ua >= ub) { tests_passed++; } else { tests_failed++; }
    if (ua >= uc) { tests_failed++; } else { tests_passed++; }
    if (uc >= ua) { tests_passed++; } else { tests_failed++; }

    return tests_passed & 0xffff | (tests_failed & 0xffff << 16);
}

int test_jal() {
    int tests_passed = 0;
    int tests_failed = 0;

    goto gohere;
    
    dontgohere:
    tests_passed = -1;
    tests_failed = 1;
    
    gohere:
    ++tests_passed;

    return tests_passed & 0xffff | (tests_failed & 0xffff << 16);
}

int main() {
    int tests_passed = 0;
    int tests_failed = 0;

    int result = test_r();
    tests_passed += result & 0xffff;
    tests_failed += (result >> 16) & 0xffff;

    result = test_i_maths();
    tests_passed += result & 0xffff;
    tests_failed += (result >> 16) & 0xffff;

    result = test_i_loads_lui();
    tests_passed += result & 0xffff;
    tests_failed += (result >> 16) & 0xffff;

    result = test_s_lui();
    tests_passed += result & 0xffff;
    tests_failed += (result >> 16) & 0xffff;

    result = test_b();
    tests_passed += result & 0xffff;
    tests_failed += (result >> 16) & 0xffff;

    result = test_jal();
    tests_passed += result & 0xffff;
    tests_failed += (result >> 16) & 0xffff;

    // jalr and auipc are tested by the function calls

    return tests_passed; //42 total tests
}
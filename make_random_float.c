double make_random_float(uint64_t random_int) {
    uint64_t random_max = 0xffffffffffffffff;
    double f;
    f = ((double)1.0) / random_max;
    f = f * random_int;
    return f;
}


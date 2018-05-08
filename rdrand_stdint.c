#include "rdrand_stdint.h"

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>

typedef struct {
        uint32_t EAX;
        uint32_t EBX;
        uint32_t ECX;
        uint32_t EDX;
} CPUIDinfo;

void get_cpuid_windows(int leaf, CPUIDinfo *info) {
uint32_t a;
uint32_t b;
uint32_t c;
uint32_t d;

asm("\n\
    mov %4, %%eax\n\
    cpuid\n\
    mov %%eax,%0\n\
    mov %%ebx,%1\n\
    mov %%ecx,%2\n\
    mov %%edx,%3":"=r"(a),"=r"(b),"=r"(c),"=r"(d):"r"(leaf):"%eax","%ebx","%ecx","%edx");
    info->EAX = a;
    info->EBX = b;
    info->ECX = c;
    info->EDX = d;
}

/*void get_cpuid_linux(CPUIDinfo *info, const uint32_t func, const uint32_t subfunc)*/
/*{*/
/*asm(".intel_syntax noprefix\n");*/
/*asm("mov r8, rdi\n");*/
/*asm("mov r9, rsi\n");*/
/*asm("mov r10, rdx\n");*/
/*asm("push rax\n");*/
/*asm("push rbx\n");*/
/*asm("push rcx\n");*/
/*asm("push rdx\n");*/
/*asm("mov eax, r9d\n");*/
/*asm("mov ecx, r10d\n");*/
/*asm("cpuid;\n");*/
/*asm("mov DWORD PTR [r8], eax\n");*/
/*asm("mov DWORD PTR [r8+4], ebx\n");*/
/*asm("mov DWORD PTR [r8+8], ecx\n");*/
/*asm("mov DWORD PTR [r8+12], edx\n");*/
/*asm("pop rdx\n");*/
/*asm("pop rcx\n");*/
/*asm("pop rbx\n");*/
/*asm("pop rax\n");*/
/*asm(".att_syntax prefix\n");*/
/*}*/

/* Trying GAS format to make clang happy*/
void get_cpuid_linux(CPUIDinfo *info, const uint32_t func, const uint32_t subfunc)
{
asm(".intel_syntax noprefix;\n\
mov r8, rdi;\n\
mov r9, rsi;\n\
mov r10, rdx;\n\
push rax;\n\
push rbx;\n\
push rcx;\n\
push rdx;\n\
mov eax, r9d;\n\
mov ecx, r10d;\n\
cpuid;\n\
mov DWORD PTR [r8], eax;\n\
mov DWORD PTR [r8+4], ebx;\n\
mov DWORD PTR [r8+8], ecx;\n\
mov DWORD PTR [r8+12], edx;\n\
pop rdx;\n\
pop rcx;\n\
pop rbx;\n\
pop rax;\n\
.att_syntax prefix\n");
}


void get_cpuid(CPUIDinfo *info, const uint32_t func, const uint32_t subfunc) {
    #if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
        get_cpuid_windows(func, info);
    #else
        get_cpuid_linux(info, func, subfunc);
    #endif
}

typedef uint32_t DWORD;

int check_is_intel() {
    CPUIDinfo info;
   
    get_cpuid(&info,0,0);
	if(memcmp((char *)(&info.EBX), "Genu", 4) == 0 &&
		memcmp((char *)(&info.EDX), "ineI", 4) == 0 &&
		memcmp((char *)(&info.ECX), "ntel", 4) == 0) {
			return 1;
	}
    
    return 0;
}

int check_is_amd() {
    CPUIDinfo info;
   
    get_cpuid(&info,0,0);

    if( memcmp((char *)(&info.EBX), "Auth", 4) == 0 &&
		memcmp((char *)(&info.EDX), "enti", 4) == 0 &&
		memcmp((char *)(&info.ECX), "cAMD", 4) == 0) {
			return 1;
	}
    return 0;
}

int check_rdrand() {
    CPUIDinfo info;
   
    get_cpuid(&info,1,0);
   
    if ((info.ECX & 0x40000000)==0x40000000) return 1;
    return 0;
}

int check_rdseed() {
    CPUIDinfo info;
   
    get_cpuid(&info,7,0);
   
   if ((info.EBX & 0x00040000)==0x00040000) return 1;
   return 0;
}

int rdrand_check_support()
{
	if ((check_is_intel()==1) || (check_is_amd()==1)){
        if (check_rdrand()==1) return 1;
	}
	return 0;
}

int rdseed_check_support()
{
	if ((check_is_intel()==1) || (check_is_amd()==1)){
        if (check_rdseed()==1) return 1;
	}
	return 0;
}

/***************************************************/
/* Gathers 16 bits of entropy through RDRAND       */
/*   The 16 bit result is zero extended to 32 bits */
/*   Writes that entropy to *therand.              */
/*   Returns 1 on success, or 0 on underflow      */
/***************************************************/

int rdrand16_step(uint16_t *therand)
{
uint16_t foo;
int cf_error_status;
asm("\n\
        rdrand %%ax;\n\
        mov $1,%%edx;\n\
        cmovae %%ax,%%dx;\n\
        mov %%edx,%1;\n\
        mov %%ax, %0;":"=r"(foo),"=r"(cf_error_status)::"%ax","%dx");
        *therand = foo;
return cf_error_status;

}

int rdseed16_step(uint16_t *therand)
{
uint16_t foo;
int cf_error_status;
asm("\n\
        rdseed %%ax;\n\
        mov $1,%%edx;\n\
        cmovae %%ax,%%dx;\n\
        mov %%edx,%1;\n\
        mov %%ax, %0;":"=r"(foo),"=r"(cf_error_status)::"%ax","%dx");
        *therand = foo;
return cf_error_status;
}

/**********************************************/
/* Gathers 32 bits of entropy through RDRAND  */
/*   Writes that entropy to *therand.         */
/*   Returns 1 on success, or 0 on undeerflow */
/**********************************************/

int rdrand32_step(uint32_t *therand)
{
int foo;
int cf_error_status;
asm("\n\
	rdrand %%eax;\n\
        mov $1,%%edx;\n\
        cmovae %%eax,%%edx;\n\
        mov %%edx,%1;\n\
        mov %%eax,%0;":"=r"(foo),"=r"(cf_error_status)::"%eax","%edx");
        *therand = foo;
return cf_error_status;

}

int rdseed32_step(uint32_t *therand)
{
int foo;
int cf_error_status;
asm("\n\
	rdseed %%eax;\n\
        mov $1,%%edx;\n\
        cmovae %%eax,%%edx;\n\
        mov %%edx,%1;\n\
        mov %%eax,%0;":"=r"(foo),"=r"(cf_error_status)::"%eax","%edx");
        *therand = foo;
return cf_error_status;

}

/**********************************************/
/* Gathers 64 bits of entropy through RDRAND  */
/*   Writes that entropy to *therand.         */
/*   Returns 1 on success, or 0 on underflow  */
/**********************************************/

int rdrand64_step(uint64_t *therand)
{
uint64_t foo;
int cf_error_status;
asm("\n\
        rdrand %%rax;\n\
        mov $1,%%edx;\n\
        cmovae %%rax,%%rdx;\n\
        mov %%edx,%1;\n\
        mov %%rax, %0;":"=r"(foo),"=r"(cf_error_status)::"%rax","%rdx");
        *therand = foo;
return cf_error_status;
}

int rdseed64_step(uint64_t *therand)
{
uint64_t foo;
int cf_error_status;
asm("\n\
        rdseed %%rax;\n\
        mov $1,%%edx;\n\
        cmovae %%rax,%%rdx;\n\
        mov %%edx,%1;\n\
        mov %%rax, %0;":"=r"(foo),"=r"(cf_error_status)::"%rax","%rdx");
        *therand = foo;
return cf_error_status;
}

/**************************************************/
/* Uses RdRand to acquire a 32 bit random number  */
/*   Writes that entropy to (uint32_t *)dest. */
/*   Will not attempt retry on underflow          */
/*   Returns 1 on success, or 0 on underflow      */
/**************************************************/

int rdrand_get_uint32(uint32_t *dest)
{
	uint32_t therand;
	if (rdrand32_step(&therand))
	{
		*dest = therand;
		return 1;
	}
	else return 0;
}

int rdseed_get_uint32(uint32_t *dest)
{
	uint32_t therand;
	if (rdseed32_step(&therand))
	{
		*dest = therand;
		return 1;
	}
	else return 0;
}

int rdrand_get_uint64(uint64_t *dest)
{
	uint64_t therand;
	if (rdrand64_step(&therand))
	{
		*dest = (uint64_t)therand;
		return 1;
	}
	else return 0;
}

int rdseed_get_uint64(uint64_t *dest)
{
	uint64_t therand;
	if (rdseed64_step(&therand))
	{
		*dest = (uint64_t)therand;
		return 1;
	}
	else return 0;
}

/**************************************************/
/* Uses RdRand to acquire a 32 bit random number  */
/*   Writes that entropy to (uint32_t *)dest. */
/*   Will retry up to retry_limit times           */
/*   Returns 1 on success, or 0 on underflow      */
/**************************************************/

int rdrand_get_uint32_retry(uint32_t retry_limit, uint32_t *dest)
{
int success;
int count;
uint32_t therand;

  count = 0;

  do
  {
	success=rdrand32_step(&therand);
  } while((success == 0) || (count++ < retry_limit));
  
  if (success == 1)
  {
	*dest = therand;
	return 1;
  }
  else
  {
	return 0;
  }
}

int rdrand_get_uint64_retry(uint32_t retry_limit, uint64_t *dest)
{
int success;
int count;
uint64_t therand;

  count = 0;

  do
  {
	success=rdrand64_step(&therand);
  } while((success == 0) || (count++ < retry_limit));
  
  if (success == 1)
  {
	*dest = therand;
	return 1;
  }
  else
  {
	return 0;
  }
}

int rdseed_get_uint32_retry(uint32_t retry_limit, uint32_t *dest)
{
int success;
int count;
uint32_t therand;

  count = 0;

  do
  {
	success=rdseed32_step(&therand);
  } while((success == 0) || (count++ < retry_limit));
  
  if (success == 1)
  {
	*dest = therand;
	return 1;
  }
  else
  {
	return 0;
  }
}

int rdseed_get_uint64_retry(uint32_t retry_limit, uint64_t *dest)
{
int success;
int count;
uint64_t therand;

  count = 0;

  do
  {
	success=rdseed64_step(&therand);
  } while((success == 0) || (count++ < retry_limit));
  
  if (success == 1)
  {
	*dest = therand;
	return 1;
  }
  else
  {
	return 0;
  }
}



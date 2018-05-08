HCRYPTPROV hCryptProv = NULL;  // CSP Handle
LPCSTR name = "AKeyContainer";
BYTE         pbData[16];
int          success = 0;

// Aquire a context
if(CryptAcquireContext(
   &hCryptProv, 
   name, 
   NULL,    // NULL indicates the default provider
   PROV_RSA_FULL,
   0))
{
    success = 1;
}
else { 
    // Failed to get the default context, so try to make one

    if (GetLastError() == NTE_BAD_KEYSET) {
        if(CryptAcquireContext(&hCryptProv, UserName, 
        NULL, PROV_RSA_FULL, CRYPT_NEWKEYSET)) {
            success = 1;
        }
    }
    else {
        printf("Error. Failed to get or make new Crypto Context.\n");
        exit(1);
    }
}

if (success == 1) {
    if(CryptGenRandom(hCryptProv, 8, pbData)) {
        for (i=0;i<8;i++) printf("%02x",pbData[i]);
    }
    else {
        printf("CryptGenRandom() did not return random numbers\n");
    }
    // Release the handle
    CryptReleaseContext(hCryptProv,0);    
}


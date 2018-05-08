int _rdrand_get_n_qints_retry(unsigned int n, unsigned int retry_limit, unsigned long long int *dest)
{
       int success;
       unsigned int count;
       unsigned int i;
 
       for (i = 0; i<n; i++)
       {
              count = 0;
              do
              {
                     success = _rdrand64_step(dest);
              } while ((success == 0) && (count++ < retry_limit));
              if (success == 0) return 0;
              dest = &(dest[1]);
       }
       return 1;
}


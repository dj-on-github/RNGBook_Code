#!/usr/bin/env python
#!/usr/bin/env python

import random
r = random.SystemRandom()

for i in range(5):
    key = r.getrandbits(256)
    print "  %064x" % key


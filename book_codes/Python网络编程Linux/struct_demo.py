

import struct
xx = struct.pack("2if", 1, 2, 3.5)
print(xx)
x1, x2, x3 = struct.unpack("2if", xx)
print(x1, x2, x3)

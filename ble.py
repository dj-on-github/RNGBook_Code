def ble(x3,x2,x1,x0,y3,y2,y1,y0):
    out0 = x3*y3 ^ x2*y2 ^ x1*y1 ^ x0*y0
    out1 = X_2 Y_3 + X_1 Y_2 + X_3 X_0 Y_1 + X_3 Y_0
    out2 = X_1 Y_3 + X_3 X_0 Y_2 + X_3 X_2 X_1 + X_2 Y_0
    out3 = X_3 X_0 Y_3 + X_3 X_2 Y_2 + X_2 X_1 X_1 + X_1 Y_0
    return (out3, out2, out1, out0)


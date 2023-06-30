# Fastapi Performance comparison

This test compares performance between Fastapi 0.98.0 and 0.100.0-beta1

On my computer the test shows that modern Fastapi 0.100.0-beta1 about x2,92 faster on medium load read requests

|                |fastapi 0.98.0 |fastapi 0.100.0-beta1|
| ---------------| --------------|---------------------|
|READ r/s        |126.90         |**371.19**           |
|READ r/s syntetic|172.57        |**1203.18**          |
|WRITE r/s       |342.11         |352.65               |
|MEM USAGE BEFORE|72.44MiB       |85.95MiB             |
|MEM USAGE AFTER |85.95MiB       |98.91MiB             |


To test on your computer, just run test.sh file
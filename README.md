## `G`rande `U`nified `M` ulticast `D` aemon, 


---
` " I've been googling for some time now, and still have yet to find a working example of Python multicast..."`


 > Is what your mom and your sister used to say, before gumd.


---



*  __Requires__ 
    * python3.6 +

* __Install__

```smalltalk

git clone https://github.com/futzu/gumd

cd gumd

### as root

install gumd.py /usr/local/bin/gumd 

```

* __Use__

   * Supported input mpegts URIs:
   
      * files  `gumd -i /home/me/vid.ts`
      * http(s) `gumd -i https://futzu.com/xaa.ts`
      * multicast `gumd -i udp://@235.1.2.3:4567`
  
      * reading from stdin `cat myvideo.ts | gumd`

```smalltalk

usage: gumd [-h] [-i INPUT] [-a ADDR] [-t TTL]

options:
  -h, --help            show this help message and exit
  
  -i INPUT, --input INPUT
                        like "/home/a/vid.ts" 
                        or "https://futzu.com/xaa.ts"
                        
                        default: sys.stdin.buffer
                        
  -a ADDR, --addr ADDR  multicast stream address like "235.35.3.5:3535"
        
                        default "235.35.3.5:3535"
  
  -t TTL, --ttl TTL     ttl value for stream, range 1 - 255
  
                        default 1

```
   * start gumd

```smalltalk
gumd -i video.ts
```


   * play gumd stream with ffplay

```smalltalk
ffplay udp://@235.35.3.5:3535
```
   * segment stream from gumd into hls with [x9k3](https://github.com/futzu/x9k3)

```smalltalk
pypy3 x9k3.py -i udp://@235.35.3.5:3535
```
  * On Linux, this is how I set up for receiving a multicast stream.
```
## <dev> is the network device

ip link set <dev> multicast on allmulticast on

ethtool  -G <dev> rx 4096

sysctl -w net.core.rmem_default=50000000

sysctl -w net.core.rmem_max=150000000
```
![image](https://user-images.githubusercontent.com/52701496/166299701-72ee908a-5053-45fc-a716-4b8ca4b1ef32.png)

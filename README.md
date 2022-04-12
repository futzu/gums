# mudpie
__M__ ulticast __U__ nified __D__ aemon in __P__ ython __I__ __E__ xplained

# Requires 
* python3.6 +

# Install
* make install installs the  script /usr/local/bin/mudpie

```smalltalk

git clone https://github.com/futzu/mudpie

cd mudpie

### as root

make install 

```

# Use
* Supported input mpegts URIs:
  * files  `/home/me/vid.ts`
  * http(s) `https://futzu.com/xaa.ts`
  * multicast `udp://@235.1.2.3:4567`

```smalltalk

usage: mudpie [-h] [-i INPUT] [-a ADDR] [-t TTL]

options:
  -h, --help            show this help message and exit
  
  -i INPUT, --input INPUT
                        like "/home/a/vid.ts" 
                        or "https://futzu.com/xaa.ts"
                        
                        default: None
                        
  -a ADDR, --addr ADDR  multicast stream address like "235.35.3.5:3535"
        
                        default "235.35.3.5:3535"
  
  -t TTL, --ttl TTL     ttl value for stream, range 1 - 255
  
                        default 1

```
* start mudpie

```smalltalk
mudpie -i video.ts
```

* play mudpie stream with ffplay

```smalltalk
ffplay udp://@235.35.3.5:3535
```
* segment stream from mudpie into hls with [x9k3](https://github.com/futzu/x9k3)

```smalltalk
pypy3 x9k3.py udp://@235.35.3.5:3535
```

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
* stream  multicast mpegts 

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

```smalltalk

mudpie -i video.ts 

```


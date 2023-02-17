[project super kabuki](https://github.com/futzu/superkabuki) SCTE-35 Packet Injection

## `G`rande `U`nified `M` ulticast `D` aemon, 

# &

## `G`rande `U`nified `M` ulticast `C` lient, 

---
` " I've been googling for some time now, and still have yet to find a working example of Python multicast"`

~ said everyone before gumd


---

* __Install__

```smalltalk

python3 -mpip install gumd

```
* The cli tools __gumc and gumd__ try to install to /usr/local/bin, if you dont get them installed, clone the repo and copy them from the bin directory to wherever you like.

* __Use__

   * Supported input mpegts URIs:
   
      * files  `gumd -i /home/me/vid.ts`
      * http(s) `gumd -i https://futzu.com/xaa.ts`
      * multicast `gumd -i udp://@235.1.2.3:4567`
  
      * reading from stdin `cat myvideo.ts | gumd`

```smalltalk
usage: gumd [-h] [-i INPUT] [-a ADDR] [-t TTL] [-v]

options:

-h, --help            show this help message and exit

-i INPUT, --input INPUT
                        like "/home/a/vid.ts" or
                        "udp://@235.35.3.5:3535" or
                        "https://futzu.com/xaa.ts"

-a ADDR, --addr ADDR  like "227.1.3.10:4310"

-t TTL, --ttl TTL     1 - 255

-v, --version         Show version

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
 
 ## gumc The client
 ```js
 a@stream:~$ gumc -h
usage: gumc [-h] [-i INSTUFF] [-b BYTESIZE] 

optional arguments:
  -h, --help            show this help message and exit
  -i INSTUFF, --instuff INSTUFF
                        default is 'udp://@235.35.3.5:3535'
  -b BYTESIZE, --bytesize BYTESIZE
                        Number of bytes to read. default is 1

 ```

 * read 13 bytes from a multicast stream
 ```lua
 gumc -i udp://@235.35.3.5:3535 -b 13
 ```
 * read 10000 bytes from a multicast stream
 ```lua
  gumc -i udp://@235.35.3.5:3535 -b 13
```
 #### Note: a multicast client works a little differently than most people expect.
 #### You must specify a size to read or the client will never return.
  
 
![image](https://user-images.githubusercontent.com/52701496/166299701-72ee908a-5053-45fc-a716-4b8ca4b1ef32.png)

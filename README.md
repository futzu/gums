[project super kabuki](https://github.com/futzu/threefive/blob/master/superkabuki.md)

## `G`rande `U`nified `M` ulticast `D` aemon, 


---
` " I've been googling for some time now, and still have yet to find a working example of Python multicast"`

~ said everyone before gumd


---
![image](https://user-images.githubusercontent.com/52701496/186205046-3577218f-e0e1-4e17-aca5-f2a8c9f3737f.png)

* __Install__

```smalltalk

python3 -mpip install gumd

```

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
 
![image](https://user-images.githubusercontent.com/52701496/166299701-72ee908a-5053-45fc-a716-4b8ca4b1ef32.png)

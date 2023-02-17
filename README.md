[project super kabuki](https://github.com/futzu/superkabuki) SCTE-35 Packet Injection

## `G`rande `U`nified `M` ulticast `D` aemon, 

# &

## `G`rande `U`nified `M` ulticast `C` lient, 

---
` " I've been googling for some time now, and still have yet to find a working example of Python multicast"`

~ said everyone before gumd

---
### Latest is `v.0.0.9`

* __Install__

```smalltalk

python3 -mpip install gumd

```

### Use gumd (Daemon) programatically
```py3
>>>> from gumd import GumD
>>>> gumd =GumD('235.35.3.5:3535',1)
>>>> gumd.mcast("/home/a/stuff")
stream uri: udp://@235.35.3.5:3535
>>>>
```
### Use gumc (Client) programatically
```py3
>>>> from gumc import GumC
>>>> gumc = GumC("udp://@235.35.3.5:3535")
>>>> data = gumc.read(8)
>>>> data
b'Helloooo'

```
## Cli tools
 The cli tools __gumd and gumc__ try to install to /usr/local/bin.

 if you dont get them installed, roll your own.
 
* __gumd__ _(Daemon)_

 ```lua

   #!/usr/bin/env python3

   from gumd import cli 

   cli()
```

* __gumc__ _(Client)_

```lua
  #!/usr/bin/env python3

  from gumc import cli 

  cli()


```


#### __Use gumd (Daemon) cli__

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
#### __start gumd (Daemon) cli__
```smalltalk
a@debian:~/gumd$ gumd -i /home/a/abc.py 
stream uri: udp://@235.35.3.5:3535
a@debian:~/gumd$ 
```
#### __use gumc (Client) cli__
```lua
usage: gumc [-h] [-i INSTUFF] [-b BYTESIZE] [-v]

options:
  -h, --help            show this help message and exit
  -i INSTUFF, --instuff INSTUFF
                        default is 'udp://@235.35.3.5:3535'
  -b BYTESIZE, --bytesize BYTESIZE
                        Number of bytes to read. default is 1
  -v, --version         Show version
```

### start gumc (Client) cli
```lua
a@debian:~/build/clean/gumd$ gumc -i udp://@235.35.3.5:3535 -b 1024

```
### Test gumd and gumc together
* first terminal, start the client, __gumc__
```lua
a@debian:~/build/clean/gumd$ pypy3 gumc.py -b 5 -i udp://@235.35.3.5:3535
```
* second terminal,start the daemon, gumd__ and send a "hello"
```lua
a@debian:~/build/clean/gumd$ printf 'hello' | gumd -a 235.35.3.5:3535
stream uri: udp://@235.35.3.5:3535
```
### play gumd (Daemon) stream with ffplay

```smalltalk
ffplay udp://@235.35.3.5:3535
```
### segment stream from gumd  (Daemon) into hls with [x9k3](https://github.com/futzu/x9k3)

```smalltalk
pypy3 x9k3.py -i udp://@235.35.3.5:3535
```
 
### read 13 bytes from a multicast stream with gumc (Client)
 ```lua
 gumc -i udp://@235.35.3.5:3535 -b 13
 ```
### read 10000 bytes from a multicast stream with gumc (Client)
 ```lua
  gumc -i udp://@235.35.3.5:3535 -b 13
```
#### Note: a multicast client works a little differently than most people expect.
#### You must specify a size to read or the client will never return.


![image](https://user-images.githubusercontent.com/52701496/166299701-72ee908a-5053-45fc-a716-4b8ca4b1ef32.png)

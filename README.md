<I> "I've been googling for some time now, and still have yet to find a working example of Python multicast"</I>

#  Behold gumd.

---
## `G`<I>rande</I> `U`<I>nicast</I> `M` <I>ulticast</I> `D` <I>aemon</I> 


---

### Latest is `v.0.0.17`

![image](https://user-images.githubusercontent.com/52701496/223828007-7d5e0bbc-7a21-400a-8ea8-5eff9620bc5a.png)


* __Install__

```smalltalk

python3 -mpip install gumd

```

### Use gumd (Daemon) programmatically
```py3
>>>> from gumd import GumD
>>>> gumd =GumD('235.35.3.5:3535',ttl=1)
>>>> gumd.send_stream("/home/a/stuff")
stream uri: udp://@235.35.3.5:3535
>>>>
```
### Use gumc (Client) programmatically
```py3
>>>> from gumc import GumC
>>>> gumc = GumC("udp://@235.35.3.5:3535")
>>>> data = gumc.read(8)
>>>> data
b'Helloooo'

```
## Cli tools
* The cli tools __gumd and gumc__ try to install to ~/.local/bin
* make sure ~/.local/bin is in your path I have this at the end my .bashrc 
```sh
PLAN9=/home/a/plan9port export PLAN9
PATH=/home/a/.local/bin:$PLAN9:$PATH export PATH
```
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
#### Install cli tools
```

install gumd /usr/local/bin  # or ~/.local/bin
install gumc /usr/local/bin  # or ~/.local/bin


```
#### __Use gumd (Daemon) cli__

   * Supported input mpegts URIs:
   
     
     * files  `gumd -i /home/me/vid.ts`
     
     * http(s) `gumd -i https://futzu.com/xaa.ts`
     
     * udp `gumd -i udp://127.0.0.1:4000`

     * multicast `gumd -i udp://@235.1.2.3:4567`
     
     * reading from stdin `cat myvideo.ts | gumd`

```smalltalk
usage: gumd [-h] [-i INPUT] [-a ADDR] [-u] [-b BIND_ADDR] [-t TTL] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        like "/home/a/vid.ts" or "udp://@235.35.3.5:3535" or "https://futzu.com/xaa.ts"
  -a ADDR, --addr ADDR  Destination Address:Port like "227.1.3.10:4310"
  -u, --unicast         Use Unicast instead of Multicast
  -b BIND_ADDR, --bind_addr BIND_ADDR
                        Local IP and Port to bind to like "192.168.1.34:5555". Default is "0.0.0.0:1025"
  -t TTL, --ttl TTL     Multicast TTL 1 - 255
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
  gumc -i udp://@235.35.3.5:3535 -b 10000
```
#### Note: a multicast client works a little differently than most people expect.
#### You must specify a size to read or the client will never return.
___


<details> <summary><h2> .</h2> </summary>

 Phase One: Expose the Pep Deep State
</h2> </summary>
  * [Phase One has begun](https://github.com/python/peps/compare/main...futzu:peps:main)
  
</details>


___

![image](https://user-images.githubusercontent.com/52701496/166299701-72ee908a-5053-45fc-a716-4b8ca4b1ef32.png)

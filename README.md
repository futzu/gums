# `G`<I>rande</I> `U`<I>nicast</I> `M` <I>ulticast</I> `S` <I>ender</I> 


###  `gums` is multicast that just works, right out of the box.
---

## gums is designed for multicast mpegts video, but works with any multicast stream.

### Latest is v.`0`.`0`.`31`

 ![image](https://github.com/futzu/gums/assets/52701496/f8bfad92-2e1e-47c1-a5b2-53e5d3152e0f)




## __Install__

```smalltalk

python3 -mpip install gums

```




### Use gums (Sender) programmatically
```py3
a@debian:~/gums$ pypy3
Python 3.9.16 (7.3.11+dfsg-2, Feb 06 2023, 16:52:03)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from gums import GumS
>>>> gummie = GumS("235.35.3.5:3535")
>>>> gummie.send_stream("/home/a/mpegts/pcrvid.ts")

	Multicast Stream
	udp://@235.35.3.5:3535

	Source
	0.0.0.0:38835

49636512 Bytes Sent

>>>> 

```

## __gums (Sender) cli__

   * Supported input mpegts URIs:
   
     * files  `gums -i /home/me/vid.ts`
     
     * http(s) `gums -i https://futzu.com/xaa.ts`
     
     * udp `gums -i udp://127.0.0.1:4000`

     * multicast `gums -i udp://@235.1.2.3:4567`
     
     * reading from stdin `cat myvideo.ts | gums`

```smalltalk
usage: gums [-h] [-i INPUT] [-a ADDR] [-b BIND_ADDR] [-t TTL] [-v]

optional arguments:
  -h, --help           Show this help message and exit

-i INPUT, --input INPUT
                       Like "/home/a/vid.ts" or "udp://@235.35.3.5:3535" or "https://futzu.com/xaa.ts"

-a ADDR, --addr ADDR     
                       Destination IP:Port like "227.1.3.10:4310"

-b BIND_ADDR, --bind_addr BIND_ADDR
                        
                       Local IP to bind to like "192.168.1.34". Default is 0.0.0.0

-t TTL, --ttl TTL       
                       Multicast TTL 1 - 255

-v, --version          
                       Show version

```
#### __start gums (Sender) cli__
```smalltalk
a@debian:~/gums$ gums -i any.file 
stream uri: udp://@235.35.3.5:3535
a@debian:~/gums$ 
```
## __gumc (Client) cli__
```lua
usage: gumc [-h] [-i INSTUFF] [-b BYTESIZE] [-v]

options:
  -h, --help            show this help message and exit
  -i INSTUFF, --instuff INSTUFF
                        default is 'udp://@235.35.3.5:3535'
  -b BYTESIZE, --bytesize BYTESIZE
                        Number of bytes to read. default is to read all.
  -v, --version         Show version
```

### start gumc (Client) cli
```lua
a@debian:~/build/clean/gums$ gumc -i udp://@235.35.3.5:3535 -b 1024

```
### Test gums and gumc together
* first terminal, start the client, __gumc__
```lua
a@debian:~/build/clean/gums$  gumc -b 5 -i udp://@235.35.3.5:3535
```
* second terminal,start the sender, gums__ and send a "hello"
```lua
a@debian:~/build/clean/gums$ printf 'hello' | gums -a 235.35.3.5:3535
stream uri: udp://@235.35.3.5:3535
```
### read all bytes from  multicast stream and write to file with gumc (Client)
```lua
gumc -i udp://@235.35.3.5:3535 -o output.ts
	
### read 13 bytes from a multicast stream with gumc (Client)
 ```lua
 gumc -i udp://@235.35.3.5:3535 -b 13
 ```
### read 10000 bytes from a multicast stream with gumc (Client)
 ```lua
  gumc -i udp://@235.35.3.5:3535 -b 10000
```

___



___

![image](https://user-images.githubusercontent.com/52701496/166299701-72ee908a-5053-45fc-a716-4b8ca4b1ef32.png)


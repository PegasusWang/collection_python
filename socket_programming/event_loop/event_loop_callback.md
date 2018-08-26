
这篇文章我们从 socket 编程的例子来看看 Python 异步框架是如何工作的，需要了解下简单的 socket 编程。
其实 Python 异步框架也是基于操作系统底层提供的 I/O 复用机制来实现的，比如 linux 下可以使用 select/poll/epoll 等。
我们先看个简单的 python socket server 例子，Python 代码使用 Python3，确保可以使用 selectors 模块。


## 一个 socket 回显示例

```py
import socket

HOST = 'localhost'    # The remote host
PORT = 8888 # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(50)
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            while 1:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
```

我们下边用一个 golang 的 tcp client 测试下它:


```golang
package main

import (
	"fmt"
	"net"
	"os"
	"sync"
)

func sendMessage(msg string) error {
	conn, err := net.Dial("tcp", "localhost:8888")
	if err != nil {
		return fmt.Errorf("error: %v", err)
	}
	defer conn.Close()

	_, err = conn.Write([]byte("hello"))
	if err != nil {
		return fmt.Errorf("error: %v", err)
	}

	reply := make([]byte, 1024)

	_, err = conn.Read(reply)
	if err != nil {
		println("Write to server failed:", err.Error())
		os.Exit(1)
	}

	println("reply from server=", string(reply))
	return nil
}

func main() {
	var wg sync.WaitGroup
	nbGoroutines := 20
	wg.Add(nbGoroutines)
	for k := 0; k < nbGoroutines; k++ {
		go func() {
			err := sendMessage("hello")
			if err != nil {
				fmt.Printf("fail: %v\n", err)
			}
			wg.Done()
		}()
	}
	wg.Wait()
}
```

使用 go 运行它可以看到输出。


## selectors 示例

接下来我们使用 python3 提供的 selectros 来改造它，这个模块封装了操作系统底层提供的 I/O 复用机制，比如 linux 上使用了
epoll。通过 I/O 复用机制我们可以监听多个文件描述符的可读写事件并且注册回调函数，拥有更好的并发性能。
先看 python3 的 selectors 文档给的例子

```py
import selectors
import socket

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('localhost', 1234))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:  # 这其实就是通常在异步框架中所说的 event loop 啦
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
```

我们来运行下这个 使用了 seelctors I/O 复用机制的 tcp echo server 看下输出结果。


## 使用 EventLoop 改造下

但是这个代码不太优雅，我们使用 EventLoop 类来改造，先来编写一个简单的 EventLoop 类。事件循环是异步框架中都会提到的东西，
其实它的实现原理就是 EventLoop 类中将要实现的 run_forever 函数，在一个死循环里调用 selector.select 函数，这个函数会在
我们注册了感兴趣的 I/O 事件发生后返回(比如有 socket 可读或者可写了)，然后我们针对不同事件调用我们的回调函数。

```py
import selectors
import socket


class EventLoop:

    def __init__(self, selector=None):
        if selector is None:
            selector = selectors.DefaultSelector()
        self.selector = selector

    def run_forever(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    callback = key.data
                    callback(key.fileobj)
                else:
                    callback, msg = key.data
                    callback(key.fileobj, msg)

```

接下来我们写一个 TCPEchoServer，它将接受一个额外的参数 loop 实例，用来执行事件循环。


```py
class TCPEchoServer:
    def __init__(self, host, port, loop):
        self.host = host
        self.port = port
        self._loop = loop
        self.s = socket.socket()

    def run(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(128)
        self.s.setblocking(False)
        self._loop.selector.register(self.s, selectors.EVENT_READ, self._accept)
        self._loop.run_forever()

    def _accept(self, sock):
        conn, addr = sock.accept()
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self._loop.selector.register(conn, selectors.EVENT_READ, self._on_read)

    def _on_read(self, conn):
        msg = conn.recv(1024)
        if msg:
            print('echoing', repr(msg), 'to', conn)
            self._loop.selector.modify(conn, selectors.EVENT_WRITE, (self._on_write, msg))
        else:
            print('closing', conn)
            self._loop.selector.unregister(conn)
            conn.close()

    def _on_write(self, conn, msg):
        conn.sendall(msg)
        self._loop.selector.modify(conn, selectors.EVENT_READ, self._on_read)


event_loop = EventLoop()
echo_server = TCPEchoServer('localhost', 8888, event_loop)
echo_server.run()
```


到这里就差不多了，我们再继续运行 go 写的 tcp client 来测试它看结果。

在后边教程中我们将使用 python 的 coroutine 而不是回调函数来改造这个例子，这样一来我们就能使用 async/await 来运行它了

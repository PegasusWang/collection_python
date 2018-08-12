# 几分钟带你了解 Python 高性能 web 框架是如何工作的[视频]

这篇文章我们从 socket 编程的简单例子来看看 Python 异步框架是如何实现并发的。
其实 Python 异步框架也是基于操作系统底层提供的 I/O 复用机制来实现的，比如 linux 下可以使用 select/poll/epoll 等。

我们先看个简单的 python socket server 例子，Python 代码使用 Python3，确保可以使用 selectors 模块。


# Echo server program

```py
import socket

HOST = 'localhost'    # The remote host
PORT = 8888 # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
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

但是这个 tcp echo server 比较低效，我们下边用一个 golang 的 tcp client 并发地给它发请求测试下它的性能：


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

接下来我们使用python3 提供的 selectros 来改造它，这个模块封装了操作系统底层提供的 I/O 复用机制，比如 linux 上使用了
epoll。通过 I/O 复用机制我们可以监听多个文件描述符的读写事件并且注册回调函数。下边的例子我们会看到如何 selectors 模块，
如何注册注册事件和回调函数。先看python3 的 selectors 文档给的例子（建议先简单过一下 selectors 模块的文档）

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

我们来运行下这个 使用了 seelctors I/O 复用机制的 tcp echo server，你会发现并发性能比之前的 echo server 强很多。

但是这个代码不太优雅，我们使用 EventLoop 类来改造，听我边敲代码边扯（中间过程大脑可能会有短路）

// https://codereview.stackexchange.com/questions/181415/golang-concurrent-tcp-server
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
	nbGoroutines := 300
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

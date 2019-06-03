package main

import (
	"fmt"
	"os"
	"crypto/md5"
	"math/rand"
	"time"
	"encoding/hex"
	"strings"
)

var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

func randSeq(n int) string {
    b := make([]rune, n)
    for i := range b {
        b[i] = letters[rand.Intn(len(letters))]
    }
    return string(b)
}

func main() {
	//warning - don't try this at home
	//OWASP kills a panda every time you seed random with timepstamps
	rand.Seed(time.Now().UnixNano())

	//argument from cmdline
	prefix := os.Args[1]

	//generate md5 from random strings
	for {
		attemp := randSeq(8)
		hash := md5.New()
        	hash.Write([]byte(attemp))                
        	hashString := hex.EncodeToString(hash.Sum(nil))

		//compare the cmdline input with the md5 prefix 
		if strings.HasPrefix(hashString,prefix){
			fmt.Printf("%s\n",attemp)
			break
		}
		
	}
}
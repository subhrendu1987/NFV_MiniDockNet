## Start Process
`setsid ./test.sh  < /dev/null &> test.log &`
## Dump Process
`sudo criu dump -t $(pgrep test.sh) -v4 -o dump.log`
## View Images
`crit decode -i core-1791.img --pretty`

## Restore Process
`criu restore -d -vvv -o restore.log && echo OK`

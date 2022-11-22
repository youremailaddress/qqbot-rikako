ps -ef | grep cqhttp | grep -v grep | awk '{print $2}' | xargs -i -t kill {}
rm -f ./cqhttp/session.token
mkdir -p ./cqhttp/logs
nohup ./cqhttp/go-cqhttp > ./cqhttp/logs/runtime.log 2>&1 &


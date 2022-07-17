ps -ef | grep cqhttp | grep -v grep | awk '{print $2}' | xargs -i -t kill {}
rm -f session.token
mkdir -p logs
nohup ./go-cqhttp > logs/runtime.log 2>&1 &


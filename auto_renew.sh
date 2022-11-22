cd /home/qqbot/qqbot-rikako/
. env/bin/activate
git checkout mainuse
git pull
ps -ef | grep bot | grep -v grep | awk '{print $2}' | xargs -i -t kill {}
nohup python bot.py > ./cqhttp/logs/pyruntime.log 2>&1 &
deactivate
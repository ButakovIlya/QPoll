# #!/bin/bash

# # Остановка существующего процесса node start.js
# PID=$(ps aux | grep 'node start.js' | grep -v grep | awk '{print $2}')

# if [ -n "$PID" ]; then
#     echo "Stopping existing node process with PID: $PID"
#     kill $PID
#     sleep 10
# fi

# # Остановка существующего процесса bash
# PID2=$(ps aux | grep '[b]ash' | awk '{print $2}')

# if [ -n "$PID2" ]; then
#     echo "Stopping existing bash process with PID: $PID2"
#     kill $PID2
#     sleep 10
# fi

# echo "Starting new process in screen..."
# # Создание и запуск нового процесса в screen
# screen -dmS my_node_session bash -c 'node start.js > output.log 2>&1'

# # Проверка, что screen сессия была запущена
# if screen -list | grep -q "my_node_session"; then
#     echo "New process started in screen session 'my_node_session'"
# else
#     echo "Failed to start new process in screen"
# fi

node start.js

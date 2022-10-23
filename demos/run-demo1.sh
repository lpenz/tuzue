#!/bin/bash

DIR=$(mktemp -d)
trap 'rm -rf $DIR' EXIT
SOCKET="$DIR/tmux"

set -e -x

rm -f demo1.cast

SHELL=/bin/bash
tmux -S "$SOCKET" \
    new-session \; \
    split-window -h \; \
    split-window -v \; \
    resize-pane -x 70 -y 20 \; \
    send-keys -t 2 'asciinema rec -c "./demo1.py" demo1.cast; tmux send-keys -t 1 exit C-m; tmux send-keys -t 0 exit C-m; exit' C-m

docker run --rm -v "$PWD:/data" asciinema/asciicast2gif -S1 demo1.cast demo1.gif

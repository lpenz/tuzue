#!/bin/bash

DIR=$(mktemp -d)
trap 'rm -rf $DIR' EXIT
SOCKET="$DIR/tmux"

set -e -x

for demo in "demo-navigate" "demo-pdb"; do

    rm -f "${demo}.cast"

    SHELL=/bin/bash
    tmux -S "$SOCKET" \
        new-session \; \
        split-window -h \; \
        split-window -v \; \
        resize-pane -x 80 -y 24 \; \
        send-keys -t 2 "asciinema rec -c \"./demo.py ${demo}\" ${demo}.cast; tmux send-keys -t 1 exit C-m; tmux send-keys -t 0 exit C-m; exit" C-m

    docker run --rm -v "$PWD:/data" asciinema/asciicast2gif -S1 "${demo}.cast" "${demo}.gif"
done

#!/bin/sh
pdfcpu stamp add -mode text -- "[Begin page %p]" "pos:tc, scale:1.0 abs, rot:0" "$@"

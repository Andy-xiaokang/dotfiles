#!/bin/bash
files=$(ls -a ~/gits/dotfiles | grep -E '\..*' | grep -v .git)
for file in `echo $files`; do
	ln -s ~/gits/dotfiles/$file ~/$file # create softlink
done


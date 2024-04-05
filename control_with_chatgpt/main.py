#! /usr/bin/env python
import generative


def main():
    while True:
        print('AIにやってほしいことを指示してね')
        instruction = input()
        if instruction != '':
            generative.control_from_ai(instruction)


if __name__ == '__main__':
    main()
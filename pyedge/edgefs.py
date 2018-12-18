# -*- coding: utf-8 -*-

import os
import re
import time
from halo import Halo

from pyconfigstore import ConfigStore
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict, Separator)

from pyfiglet import figlet_format

from app import start_edge
try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

config = ConfigStore("edgefs")

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            print(colored(string, color))
        else:
            print(colored(figlet_format(
                string, font=font), color))
    else:
        print(string)


class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))

def ui_connect():
    questions = [
        {
            'type': 'list',
            'name': 'node_type',
            'message': 'Node setup',
            'choices': [
                {
                    'key': 'm',
                    'name': 'Master node',
                    'value': 'master'
                },
                {
                    'key': 'c',
                    'name': 'Connect to an Edge',
                    'value': 'client'
                }]
        },
        {
            'type': 'input',
            'name': 'edge_id',
            'message': 'Type the Edge ID you want to connect to:',
            'when': lambda answers: answers['node_type'] != 'master'
        }
    ]
    
    answers = prompt(questions, style=style)
    return answers

def ui_inside_edgefs():
    questions = [
        {
            'type': 'list',
            'name': 'first_loop',
            'message': "What's next?",
            'choices': [
                {
                    'key': 'v',
                    'name': 'View open files',
                    'value': 'view_files'
                },
                {
                    'key': 'u',
                    'name': 'Upload file',
                    'value': 'upload'
                }]
        },
    ]
    
    answers = prompt(questions, style=style)
    return answers

def ui_view_files(all_files):
    questions = [
        {
            'type': 'checkbox',
            'name': 'selected_files',
            'message': 'Select files to download',
            'choices': all_files
        }
    ]
    
    answers = prompt(questions, style=style)
    return answers

def main():
    """
    CLI for managing an EdgeFS node
    """
    log("EdgeFS", color="red", figlet=True)
    # TODO: add a version number of the current build
    # TODO: check for updates

    # Look in the settings for an exiting Edge
    
    if config.has("edge_to_connect"):
        edge_to_connect = config.get("edge_to_connect")
        spinner = Halo(text='Connecting to Edge', spinner='pong', text_color='green')
        spinner.start()
        # TODO: send a ping to the node
        time.sleep(2)
        spinner.succeed("Connected")
    else:
        selection = ui_connect()
        if selection['node_type'] == 'client':
            spinner = Halo(text='Connecting to Edge ^'+selection['edge_id'], spinner='pong', text_color='green')
            spinner.start()
            time.sleep(4)
            edge = start_edge(selection['edge_id'])
            if edge:
                spinner.succeed("Connected to Edge ^"+ selection['edge_id'])
            else:
                spinner.fail("Connecting to ^"+selection['edge_id']+" failed")
            
    
    log("Welcome to EdgeFS, Group 661", color="green")
    log("20 Edges found, total 35 open files", color="green")
    
    selection = ui_inside_edgefs()
    if selection['first_loop'] == 'view_files':
        spinner = Halo(text='Downloading list from Edges, it might take a while', spinner='dots3', text_color='green')
        spinner.start()
        time.sleep(2)

        # TODO: download list of files
        list_of_files_from_edges = [{'name': 'one.jpg'}, 
                                    {'name': 'two.jpg'}]

        spinner.succeed("List of files downloaded")
        response = ui_view_files(list_of_files_from_edges)

        spinner = Halo(text='Downloading files', spinner='dots3', text_color='green')
        spinner.start()
        time.sleep(2)

        log("Downloaded " + str(len(response['selected_files'])) + " files", color="green")

if __name__ == '__main__':
    main()
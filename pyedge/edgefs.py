import os
import re
import time
from halo import Halo

from pyconfigstore import ConfigStore
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict, Separator)

from pyfiglet import figlet_format

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


class FilePathValidator(Validator):
    def validate(self, value):
        if len(value.text):
            if os.path.isfile(value.text):
                return True
            else:
                raise ValidationError(
                    message="File not found",
                    cursor_position=len(value.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


class APIKEYValidator(Validator):
    def validate(self, value):
        if len(value.text):
            sg = sendgrid.SendGridAPIClient(
                api_key=value.text)
            try:
                response = sg.client.api_keys._(value.text).get()
                if response.status_code == 200:
                    return True
            except:
                raise ValidationError(
                    message="There is an error with the API Key!",
                    cursor_position=len(value.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


def askAPIKEY():
    questions = [
        {
            'type': 'input',
            'name': 'api_key',
            'message': 'Enter SendGrid API Key (Only needed to provide once)',
            'validate': APIKEYValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers

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
        spinner = Halo(text='Connecting to Edge', spinner='dots', text_color='green')
        spinner.start()
        # TODO: send a ping to the node
        time.sleep(2)
        spinner.succeed("Connected")
    else:
        selection = ui_connect()
        if selection['node_type'] == 'client':
            spinner = Halo(text='Connecting to Edge ^'+selection['edge_id'], spinner='dots', text_color='green')
            spinner.start()
            # TODO: send a ping to the node
            time.sleep(2)
            #spinner.fail("Connecting to ^"+selection['edge_id']+" failed")
            spinner.succeed("Connected to Edge ^"+ selection['edge_id'])
    
    log("Welcome to EdgeFS, Group 661", color="green")
    ui_inside_edgefs()


if __name__ == '__main__':
    main()
#!/usr/bin/env python3

import shlex  # For splitting the command string safely, handling quotes/escapes
from typing import Dict, List  # For type hints (optional, but improves readability)

def parse_curl_command(curl_cmd: str) -> Dict[str, any]:
    if not curl_cmd.startswith('curl '):
        raise ValueError("Command must start with 'curl '")
    
    tokens = shlex.split(curl_cmd)  # Split safely
    
    if tokens[0] != 'curl':
        raise ValueError("Not a valid curl command")
    
    result = {
        'url': None,
        'method': 'GET',  # Default for curl
        'headers': {},    # key: value
        'body': [],       # List for multiple data parts
        'user': None,     # For basic auth
        'other_flags': [] # Catch-all for unhandled
    }
    
    i = 1  # Skip 'curl'
    while i < len(tokens):
        token = tokens[i]
        
        if token in ('-X', '--request'):
            i += 1
            result['method'] = tokens[i]
        
        elif token in ('-H', '--header'):
            i += 1
            header = tokens[i]
            if ':' in header:
                key, value = header.split(':', 1)
                result['headers'][key.strip()] = value.strip()
            else:
                result['headers'][header] = None  # Edge case
        
        elif token in ('-d', '--data', '--data-raw', '--data-binary'):
            i += 1
            result['body'].append(tokens[i])
        
        elif token in ('-u', '--user'):
            i += 1
            result['user'] = tokens[i]
        
        elif not token.startswith('-'):
            if result['url'] is not None:
                raise ValueError("Multiple URLs detected; only one supported")
            result['url'] = token
        
        else:
            other_flag = token
            i += 1
            if i < len(tokens) and not tokens[i].startswith('-'):
                other_flag += f" {tokens[i]}"
            result['other_flags'].append(other_flag)
        
        i += 1
    
    if result['url'] is None:
        raise ValueError("No URL found in curl command")
    
    return result

def format_curl_to_readable(parsed: Dict[str, any]) -> str:
    output = []
    
    output.append("URL:")
    output.append(f"  {parsed['url']}\n")
    
    output.append("Method:")
    output.append(f"  {parsed['method']}\n")
    
    if parsed['headers']:
        output.append("Headers:")
        for key, value in parsed['headers'].items():
            output.append(f"  {key}: {value}")
        output.append("")  # Blank line
    
    if parsed['body']:
        output.append("Body/Data:")
        body_str = ' & '.join(parsed['body']) if len(parsed['body']) > 1 else parsed['body'][0]
        output.append(f"  {body_str}\n")
    
    if parsed['user']:
        output.append("Authentication (User):")
        output.append(f"  {parsed['user']}\n")
    
    if parsed['other_flags']:
        output.append("Other Flags:")
        for flag in parsed['other_flags']:
            output.append(f"  {flag}")
        output.append("")  # Blank line
    
    return '\n'.join(output)

if __name__ == "__main__":
    print("Welcome to Curl Parser Tool. Enter 'quit' to exit.")
    while True:
        curl_input = input("Enter curl command: ")
        if curl_input.lower() == 'quit':
            break
        try:
            parsed = parse_curl_command(curl_input)
            readable = format_curl_to_readable(parsed)
            print("\nParsed Output:\n")
            print(readable)
        except ValueError as e:
            print(f"Error: {e}")
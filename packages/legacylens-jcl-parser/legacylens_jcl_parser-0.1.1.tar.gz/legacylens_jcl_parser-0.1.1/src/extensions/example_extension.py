#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example extension for the JCL Parser

This demonstrates how to extend the JCL Parser with additional functionality.
"""

import re
from typing import Dict, Any

from ..jcl_parser import JCLParser


class ExtendedJCLParser(JCLParser):
    """Extended JCL Parser with additional features"""
    
    def __init__(self):
        """Initialize the extended parser"""
        # Call the parent initializer first
        super().__init__()
        
        # Add additional regex patterns for new statement types
        self.if_pattern = re.compile(r'//\s+IF\s+(.*)')
        self.else_pattern = re.compile(r'//\s+ELSE\s*(.*)')
        self.endif_pattern = re.compile(r'//\s+ENDIF\s*(.*)')
        # Updated pattern to correctly separate member name and additional parameters
        self.include_pattern = re.compile(r'//\s+INCLUDE\s+MEMBER=(\S+)(.*)')
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a JCL file with extended functionality"""
        # Start with the basic parsing from the parent class
        jcl_data = super().parse_file(file_path)
        
        # Add a new section for conditional logic
        jcl_data["conditionals"] = []
        
        # Reopen the file to look for conditionals
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                # Check for IF statement
                if_match = self.if_pattern.match(line)
                if if_match:
                    condition = if_match.group(1)
                    jcl_data["conditionals"].append({
                        "type": "if",
                        "condition": condition,
                        "line": line_num
                    })
                    continue
                
                # Check for ELSE statement
                else_match = self.else_pattern.match(line)
                if else_match:
                    jcl_data["conditionals"].append({
                        "type": "else",
                        "line": line_num
                    })
                    continue
                
                # Check for ENDIF statement
                endif_match = self.endif_pattern.match(line)
                if endif_match:
                    jcl_data["conditionals"].append({
                        "type": "endif",
                        "line": line_num
                    })
                    continue
                
                # Check for INCLUDE statement
                include_match = self.include_pattern.match(line)
                if include_match:
                    member_name, include_params = include_match.groups()
                    if "includes" not in jcl_data:
                        jcl_data["includes"] = []
                    
                    # Extract the member name from any potential comma
                    # This handles cases like "MEMBER=STDDD,LIB=CUSTOM.PROCLIB"
                    if ',' in member_name:
                        member_name, additional_params = member_name.split(',', 1)
                        include_params = ',' + additional_params + include_params
                    
                    jcl_data["includes"].append({
                        "member": member_name,
                        "parameters": self.parse_parameters(include_params),
                        "line": line_num
                    })
                    continue
        
        return jcl_data


# Example usage
if __name__ == "__main__":
    import sys
    import os
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python example_extension.py <jcl_file>")
        sys.exit(1)
    
    jcl_file = sys.argv[1]
    if not os.path.exists(jcl_file):
        print(f"Error: File '{jcl_file}' not found")
        sys.exit(1)
    
    parser = ExtendedJCLParser()
    try:
        jcl_data = parser.parse_file(jcl_file)
        print(json.dumps(jcl_data, indent=2))
    except Exception as e:
        print(f"Error parsing JCL file: {e}")
        sys.exit(1) 
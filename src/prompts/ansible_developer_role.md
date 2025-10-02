# Role

You are an expert Python and Ansible developer specializing in Ansible module creation.
You are passionate about best practice coding, including concepts such as dependency
injection, separation of concerns, single responsibility, modularity, intuitive and
consistent method and variable names, etc. You favor composition over inheritance. You
love generating beautiful code that others can easily understand and maintain, and
that is extensible.

## Task

Your task is to create an Ansible module, written in Python 3.12 or higher. The module will
manage Nexus Dashboard VRFs and will handle the following Ansible states.

- deleted
- merged
- overridden
- query
- replaced

Each state should be impemented in a separate class with corresponding names.

- Deleted
- Merged
- Overridden
- Query
- Replaced

If you have questions about what a given state should do, please feel free to ask!

### Requirements

Here are the requirements for the Ansible module you are developing:

- **Functionality:** The module should connect to a Nexus Dashboard version 3 server using a connection plugin that is already defined for this project.
- **Inputs:**
  - `hostname`: Is already defined in the Ansible inventory and is not required by the Ansible module you are writing.
  - `username`: Is already defined in the Ansible inventory and is not required by the Ansible module you are writing.
  - `password`: Is already defined in the Ansible inventory and is not required by the Ansible module you are writing.
  - `config`: This is the Ansible playbook `config` field.  `config` is a list of dictionaries, where each dictionary contains the field(s) that define a VRF configuration.
  - `state`: The Ansible state associated with the config.  For example, deleted state should result in the Deleted() class being called.
- **Outputs:**
  - Return a JSON dictionary containing the standard output and standard error of the executed command.
  - Indicate whether the command executed successfully or failed.
- **Dependencies:**
  - Use Pydantic (Version 2 or higher) to validate all payloads, controller responses, and playbook config data.
- **Python Coding Conventions**
  - Use type hints for all method/function signatures and variables.
  - Clean separation of concerns.
  - Methods should be short, and follow the single responsibility principle.
  - Use composition over inheritence.
  - Use dependency injection where it makes sense.
  - Use Python 3.9+ modern type hinting syntax rather than objects (Dict, List, etc) from the typing library.
- **Ansible Module Conventions:**
  - Follow standard Ansible module structure.
  - Use `AnsibleModule` to handle module arguments and return results.
  - Include proper docstrings for the module and relevant functions.
  - Handle errors gracefully and return informative error messages in the output.
- **Output Format:** Provide the complete Python code for the module in a code block. Include a brief explanation of the code and how to use the module within an Ansible playbook.

## Important

Think step-by-step to plan the module structure, including handling arguments, determining the state to be used, and returning the results in the specified format.

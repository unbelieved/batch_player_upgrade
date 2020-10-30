#Assumptions and Technical Decisions
## Target User
It is assumed that the target user for this tool is a employee in technical support or client services. As such they have some familiarity with command line tools, but are not necessarily experts.

## Environment
Is is assumed that the user has python installed, for linux users it is assumed that they are using a currently supported LTS version of Ubuntu

#Technical Decisions
- The script should be backwards compatible with python 3.5 as that is the version shipped in Ubuntu 16.04. Windows and Mac versions are likely to be more up to date
- The script should be in a single file, to allow for easy distribution between team members
- The script should use only python builtins in order to avoid a need to perform additional installation 
- A functional paradigm was used since it seemed more appropriate for the use case
- It is assumed that the token will not expire within the timeframe of the scripts execution, so it is only acquired at the beginning of execution
- Likewise, clientId and application versions are set at the initialization of the script
- CSV files with or without header rows are accepted, and the field name is ignored as it is assumed that the first column is to contain mac addresses.
- The script could benefit from proper integration tests with a mock http server, but I felt that to be outside the scope of the current project
- Extra command line parameters were added to set the "hardcoded" values in the requirements, allowing limited usage out of the box without having to implement functions in the code
- The API server url is set with an environment variable to facilitate automation or use in a microservice
- The unit tests do not cover the calling of the entry point when the scripts are run from the command line (ie the function call under the block :
(if \_\_name\_\_ == "\_\_main\_\_") 
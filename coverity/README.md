# Coverity Report Tool

## Setup
1. **Create and Activate Virtual Environment**  
   Execute the following commands to create and activate a virtual environment:
   ```sh
   # Create virtual environment and activate it
   uv venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**  
   Run the command below to install the necessary dependencies:
   ```sh
   # Install dependencies
   uv add "mcp[cli]"
   ```

## Features
- **Issue Summary**  
  Aggregates and summarizes Coverity issues by checkerName.

- **Query a Specific Coverity Object by Category**  
  Retrieve a single Coverity object that matches the specified category (checkerName). The output format is as follows:
  ```json
  {
      "type": "AUTO_CAUSES_COPY",
      "mainEventFilepath": "/home/scratch.louiliu_vlsi_1/work/nvtools_louiliu_2/nvtools/cad/cadlib/vector/JetBasis/PropertyMap.h",
      "mainEventLineNumber": 230,
      "functionDisplayName": "auto vectorlib::PropertyMapBase<...>",
      "events": {
          "eventDescription": [
              "This lambda has an unspecified return type. This implies \"auto\" and causes the copy of an object of type \"std::string\".",
              "Use \"-> const auto &\" \"std::string\".",
              "This return statement creates a copy."
          ],
          "subcategoryLongDescription": "Using the auto keyword without an & causes a copy."
      }
  }
  ```
  注意：輸出中的 "type" 欄位實際上對應報告中的 "checkerName" 值。

- **Auto Fix by Cursor**  
  Automatically fix issues for a given category by processing each matching entry. This generates a prompt that can be fed to an LLM. For example:
  ```
  Need to fix the coverity issue: {checkerName} file is {mainEventFilepath} at line {mainEventLineNumber} in function {functionDisplayName}. Reason: {events.subcategoryLongDescription}. Details: {events.eventDescription joined by a space or newline}.
  ```

## Implementation Specification
1. **Issue Aggregation**  
   - Parse the report file's `issues` property.
   - Group the issues by `checkerName` and return a list that indicates each `checkerName` along with its count.

2. **Querying a Specific Coverity Object**  
   - Search the report file's `issues` for the first object that matches the specified category (`checkerName`).
   - The output should include the following properties:
     - `type` (contains the value of `checkerName`)
     - `mainEventFilepath`
     - `mainEventLineNumber`
     - `functionDisplayName`
     - `subcategoryLongDescription` (directly from the issue)
   - **Events Field**:  
     - Concatenate all entries from the issue's `events.eventDescription` array and include them under the `eventDescription` section.

3. **Auto Fix Feature**  
   - For a given category, process each matching issue sequentially.
   - Generate a prompt for each issue that an LLM can use to suggest or apply a fix.
   - The prompt should adhere to the format provided above.
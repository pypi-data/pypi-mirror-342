import requests
import argparse
import json
import os
from fastmcp import FastMCP, Client

mcp = FastMCP("Dolt Database Explorer")

# Configuration - you can adjust these as needed
DOLT_API_URL = "https://www.dolthub.com/api/v1alpha1"
DATABASE_OWNER = "calvinw"  
DATABASE_NAME = "BusMgmtBenchmarks" 
DATABASE_BRANCH = "main"
API_TOKEN = None 

def get_dolt_query_url():
    """Get the URL for executing SQL queries against the Dolt database"""
    return f"{DOLT_API_URL}/{DATABASE_OWNER}/{DATABASE_NAME}/{DATABASE_BRANCH}"

def get_auth_headers():
    """Get headers with API token for authorized requests"""
    headers = {"Content-Type": "application/json"}
    if API_TOKEN:
        headers["Authorization"] = API_TOKEN
    return headers

@mcp.resource("schema://main")
def get_schema() -> str:
    """Provide the database schema as a resource"""
    try:
        # Query to get all tables
        tables_query = "SHOW TABLES"
        tables_response = requests.get(
            get_dolt_query_url(),
            params={"q": tables_query}
        )
        tables_response.raise_for_status()
        tables_data = tables_response.json()

        schema_parts = []

        # For each table, get its schema
        for row in tables_data.get("rows", []):
            # Extract table name from the row object based on JSON structure
            table_name = row.get(f"Tables_in_{DATABASE_NAME}")

            if table_name:
                # Get schema for this table
                schema_query = f"SHOW CREATE TABLE `{table_name}`"
                schema_response = requests.get(
                    get_dolt_query_url(),
                    params={"q": schema_query}
                )
                schema_response.raise_for_status()
                schema_data = schema_response.json()

                if schema_data.get("rows") and len(schema_data["rows"]) > 0:
                    # Extract Create Table statement from the response
                    create_statement = schema_data["rows"][0].get("Create Table")
                    if create_statement:
                        schema_parts.append(create_statement)

        return "\n\n".join(schema_parts)
    except Exception as e:
        return f"Error retrieving schema: {str(e)}"

@mcp.tool()
def read_query(sql: str) -> str:
    """Execute SQL read queries safely on the Dolt database"""
    try:
        # Execute the query
        response = requests.get(
            get_dolt_query_url(),
            params={"q": sql}
        )
        response.raise_for_status()
        result = response.json()

        # Format the result
        if "rows" not in result or not result["rows"]:
            return "No data returned or query doesn't return rows."

        # Get column names from the schema
        columns = result.get("schema", [])
        column_names = [col.get("columnName", f"Column{i}") for i, col in enumerate(columns)]

        # Create header row
        output = [" | ".join(column_names)]
        output.append("-" * len(" | ".join(column_names)))

        # Add data rows
        for row in result["rows"]:
            # Get values in the same order as column names
            row_values = []
            for col_name in column_names:
                val = row.get(col_name)
                row_values.append(str(val) if val is not None else "NULL")
            output.append(" | ".join(row_values))

        return "\n".join(output)
    except Exception as e:
        return f"Error executing query: {str(e)}"

@mcp.tool()
def write_query(sql: str) -> str:
    """Execute write operations (INSERT, UPDATE, DELETE) on the Dolt database"""
    try:
        # Check if API token is available
        if not API_TOKEN:
            return "Error: API token is required for write operations. Please start the server with --api-token parameter."
        
        # Verify this is a write operation
        sql_upper = sql.upper().strip()
        if not (sql_upper.startswith('INSERT') or 
                sql_upper.startswith('UPDATE') or 
                sql_upper.startswith('DELETE') or
                sql_upper.startswith('CREATE') or
                sql_upper.startswith('DROP') or
                sql_upper.startswith('ALTER')):
            return "Error: This function only accepts write operations (INSERT, UPDATE, DELETE, CREATE, DROP, ALTER)"
        
        # Set up headers with API token
        headers = get_auth_headers()
        
        # Execute the write query using POST request
        write_url = f"{DOLT_API_URL}/{DATABASE_OWNER}/{DATABASE_NAME}/write/{DATABASE_BRANCH}/{DATABASE_BRANCH}"
        
        # Use params instead of json
        response = requests.post(
            write_url,
            params={"q": sql},
            headers=headers
        )
        response.raise_for_status()
        result = response.json()
        
        # Check for errors in the response
        if "errors" in result and result["errors"]:
            return f"Error executing write query: {result['errors']}"
        
        # If we received an operation_name, poll for completion
        if "operation_name" in result:
            operation_name = result["operation_name"]
            
            # Define the polling function
            def get_operation(op_name):
                """Get the status of an operation by its name"""
                op_res = requests.get(
                    f"{DOLT_API_URL}/{DATABASE_OWNER}/{DATABASE_NAME}/write",
                    params={"operationName": op_name},
                    headers=headers
                )
                op_res.raise_for_status()
                return op_res.json()
            
            def poll_operation(op_name):
                """Poll an operation until it's done or max retries is reached"""
                done = False
                max_retries = 10
                retry_count = 0
                
                while not done and retry_count < max_retries:
                    poll_res = get_operation(op_name)
                    done = poll_res.get("done", False)
                    
                    if done:
                        return poll_res
                    else:
                        import time
                        time.sleep(3)  # Wait 3 seconds between polls
                        retry_count += 1
                
                # If we've reached max retries but the operation isn't done
                if retry_count >= max_retries:
                    return {"done": False, "max_retries_reached": True}
                
                return poll_res
            
            # Poll the operation
            poll_result = poll_operation(operation_name)
            
            if poll_result.get("max_retries_reached", False):
                return f"Write operation submitted (ID: {operation_name}), but is taking longer than expected to complete. It may still be processing."
            
            if poll_result.get("done", False):
                res_details = poll_result.get("res_details", {})
                query_status = res_details.get("query_execution_status")
                query_message = res_details.get("query_execution_message", "")
                
                # Add final commit step with empty query to finalize changes
                merge_url = f"{DOLT_API_URL}/{DATABASE_OWNER}/{DATABASE_NAME}/write/{DATABASE_BRANCH}/{DATABASE_BRANCH}"
                merge_response = requests.post(
                    merge_url,
                    params=None,  # Empty query to finalize/commit changes
                    headers=headers
                )
                
                if merge_response.status_code == 200:
                    merge_result = merge_response.json()
                    if "operation_name" in merge_result:
                        # Poll the commit operation
                        commit_poll_result = poll_operation(merge_result["operation_name"])
                        if commit_poll_result.get("done", False):
                            return f"Write operation successful and committed: {query_message}"
                        else:
                            return f"Write operation successful but commit is still processing: {query_message}"
                    else:
                        return f"Write operation successful: {query_message}"
                else:
                    return f"Write operation successful but commit failed: {query_message}"
            
            return f"Write operation status unknown. Operation ID: {operation_name}"
        
        # For direct responses with rows_affected
        if "rows_affected" in result:
            return f"Success: {result['rows_affected']} row(s) affected"
            
        # Default success message
        return "Success: Query executed successfully"
            
    except Exception as e:
        return f"Error executing write query: {str(e)}"

@mcp.tool()
def list_tables() -> str:
    """List the tables in the database"""
    try:
        response = requests.get(
            get_dolt_query_url(),
            params={"q": "SHOW TABLES"}
        )
        response.raise_for_status()
        result = response.json()

        if "rows" not in result or not result["rows"]:
            return "No tables found."

        # Debug information
        debug_info = [
            "Debug information:",
            f"DATABASE_NAME: {DATABASE_NAME}",
            f"Expected column: Tables_in_{DATABASE_NAME}"
        ]
        
        if len(result["rows"]) > 0:
            first_row = result["rows"][0]
            debug_info.append(f"Available keys in first row: {list(first_row.keys())}")
            
            # Add sample row data
            import json
            debug_info.append(f"Sample row: {json.dumps(first_row, indent=2)}")
        
        # Extract table names from the rows
        tables = []
        expected_column = f"Tables_in_{DATABASE_NAME}"
        
        for row in result["rows"]:
            # Try both the expected column name and direct value extraction
            table_name = None
            
            # Try the expected column name format
            if expected_column in row:
                table_name = row.get(expected_column)
            # If row has only one key, use its value (simpler API responses)
            elif len(row) == 1:
                table_name = list(row.values())[0]
            # Look for any key ending with 'Tables_in_'
            else:
                for key in row:
                    if key.startswith("Tables_in_"):
                        table_name = row.get(key)
                        break
            
            if table_name:
                tables.append(table_name)
        
        if not tables:
            # If we couldn't extract tables with the methods above, 
            # just return all values from all rows as a fallback
            for row in result["rows"]:
                tables.extend([str(v) for v in row.values() if v])
        
        # Add tables info to debug output
        debug_info.append(f"Extracted tables count: {len(tables)}")
        if tables:
            debug_info.append("First few tables: " + ", ".join(tables[:3]))
        
        # Print debug info to server console
        print("\n".join(debug_info))
        
        # Return the table list to the client
        return "\n".join(tables)
    except Exception as e:
        error_msg = f"Error listing tables: {str(e)}"
        print(error_msg)  # Print to server console for debugging
        return error_msg

@mcp.tool()
def describe_table(table_name: str) -> str:
    """Describe the structure of a specific table"""
    try:
        response = requests.get(
            get_dolt_query_url(),
            params={"q": f"DESCRIBE `{table_name}`"}
        )
        response.raise_for_status()
        result = response.json()

        if "rows" not in result or not result["rows"]:
            return f"Table '{table_name}' not found or is empty."

        # Debug information
        debug_info = [
            f"Debug for describe_table({table_name}):",
            f"Result has {len(result.get('rows', []))} rows"
        ]
        
        if len(result.get("rows", [])) > 0:
            first_row = result["rows"][0]
            debug_info.append(f"Keys in first row: {list(first_row.keys())}")
            
            # Add sample row data
            import json
            debug_info.append(f"Sample row: {json.dumps(first_row, indent=2)}")
        
        # Print debug info to server console
        print("\n".join(debug_info))

        # Expected column names for DESCRIBE command
        expected_columns = ["Field", "Type", "Null", "Key", "Default", "Extra"]
        
        # Format the results
        output = [" | ".join(expected_columns)]
        output.append("-" * len(" | ".join(expected_columns)))

        # Add data rows
        for row in result["rows"]:
            # Map the row data to the expected columns
            row_values = []
            for col_name in expected_columns:
                val = row.get(col_name)
                row_values.append(str(val) if val is not None else "NULL")
            output.append(" | ".join(row_values))

        return "\n".join(output)
    except Exception as e:
        error_msg = f"Error describing table: {str(e)}"
        print(error_msg)  # Print to server console for debugging
        return error_msg

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

def main():
    global DATABASE_OWNER, DATABASE_NAME, DATABASE_BRANCH, API_TOKEN
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Dolt Database Explorer MCP Server')
    parser.add_argument('--owner', help='Database owner (default: calvinw)')
    parser.add_argument('--database', help='Database name (default: BusMgmtBenchmarks)')
    parser.add_argument('--branch', help='Database branch (default: main)')
    parser.add_argument('--api-token', help='API token for write operations')
    
    args = parser.parse_args()
    
    # Update configuration if provided in arguments
    if args.owner:
        DATABASE_OWNER = args.owner
    if args.database:
        DATABASE_NAME = args.database
    if args.branch:
        DATABASE_BRANCH = args.branch
    if args.api_token:
        API_TOKEN = args.api_token
    
    print("Dolt Database Explorer MCP Server is running")
    print(f"Connected to: {DATABASE_OWNER}/{DATABASE_NAME}, branch: {DATABASE_BRANCH}")
    print(f"API Token: {'Configured' if API_TOKEN else 'Not configured (read-only)'}")
    mcp.run()

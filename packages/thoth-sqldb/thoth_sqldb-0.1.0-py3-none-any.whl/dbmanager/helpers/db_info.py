import logging
import re
from typing import Dict, List, Any

import pandas as pd

from multi_db_generator import MultiDbGenerator
from schema import DatabaseSchema
from django_api.django_api_using_apikey import get_db_tables, get_table_columns


def get_db_all_tables(db_name: str) -> List[str]:
    """
    Retrieves all table names from the database.

    Args:
        db_name (str): The path to the database file.

    Returns:
        List[str]: A list of table names.
    """
    try:
        table_list = get_db_tables(db_name)
        return [table["name"] for table in table_list]
    except Exception as e:
        logging.error(f"Error in get_db_all_tables: {e}")
        raise e

def get_table_all_columns(db_name: str, table_name: str) -> List[str]:
    """
    Retrieves all column names for a given table.

    Args:
        db_name (str): The path to the database file.
        table_name (str): The name of the table.

    Returns:
        List[str]: A list of column names.
    """
    try:
        column_list = get_table_columns(db_name, table_name)
        return [column["original_column_name"] for column in column_list]
    except Exception as e:
        logging.error(f"Error in get_table_all_columns: {e}\nTable: {table_name}")
        raise e

def get_db_schema(db_name: str) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Retrieves the complete schema of the database with detailed column information.
    
    The returned structure matches Django's column fields:
    {
        "table_name": {
            "columns": {
                "original_column_name": {        # This is the key in the columns dict
                    "original_column_name": str,  # Original name (required)
                    "column_name": str,          # Expanded name (required)
                    "data_format": str,          # Data type from ColumnDataTypes enum
                    "column_description": str,    # Column description (optional)
                    "generated_comment": str,     # Generated documentation (optional)
                    "value_description": str,     # Value description (optional)
                    "pk_field": str,             # Primary key info (optional)
                    "fk_field": str,             # Foreign key info (optional)
                }
            }
        }
    }
    """
    try:
        schema = {}
        table_list = get_db_tables(db_name)
        
        for table in table_list:
            table_name = table["name"]
            schema[table_name] = {"columns": {}}
            
            try:
                columns = get_table_columns(db_name, table_name)
                for column in columns:
                    original_name = column["original_column_name"]
                    
                    # Handle pk_field: convert to empty string if 0/False
                    pk_field = column.get("pk_field", "")
                    if not pk_field or pk_field == "0" or pk_field == 0:
                        pk_field = ""
                    
                    # Handle fk_field similarly
                    fk_field = column.get("fk_field", "")
                    if not fk_field or fk_field == "0" or fk_field == 0:
                        fk_field = ""
                    
                    # Handle column_name: if not present, use original_column_name
                    expanded_name = column.get("column_name", "").strip()
                    if not expanded_name:
                        expanded_name = original_name
                    
                    # Create standardized column info matching Django fields
                    column_info = {
                        "original_column_name": original_name,
                        "column_name": expanded_name,
                        "data_format": column.get("data_format", "VARCHAR"),
                        "column_description": column.get("column_description", ""),
                        "generated_comment": column.get("generated_comment", ""),
                        "value_description": column.get("value_description", ""),
                        "pk_field": pk_field,
                        "fk_field": fk_field
                    }
                    
                    schema[table_name]["columns"][original_name] = column_info
                    
            except Exception as e:
                logging.error(f"Error getting columns for table {table_name}: {e}")
                continue
                
        return schema
        
    except Exception as e:
        logging.error(f"Error in get_db_schema: {e}")
        raise e

def load_tables_description(
    db_name: str, use_value_description: bool
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Loads table descriptions from CSV files in the database directory.

    Args:
        db_name (str): The path to the database directory.
        use_value_description (bool): Whether to include value descriptions.

    Returns:
        Dict[str, Dict[str, Dict[str, str]]]: A dictionary containing table descriptions.
    """
    table_description = {}
    table_list = get_db_tables(db_name)
    for table in table_list:
        table_name = table["name"].lower().strip()
        table_description[table_name] = {}
        could_read = False
        try:
            table_description_df = get_table_columns(db_name, table_name)
            for row in table_description_df:
                column_name = row["original_column_name"]
                expanded_column_name = (
                    row.get("column_name", "").strip()
                    if row.get("column_name")
                    not in (None, "", "nan", "NaN", "null", "NULL")
                    else ""
                )
                column_description = (
                    row.get("column_description", "")
                    .replace("\n", " ")
                    .replace("commonsense evidence:", "")
                    .strip()
                    if pd.notna(row.get("column_description", ""))
                    else ""
                )
                value_description = ""
                if use_value_description and row.get("value_description") not in (
                    None,
                    "",
                    "nan",
                    "NaN",
                    "null",
                    "NULL",
                ):
                    value_description = (
                        row["value_description"]
                        .replace("\n", " ")
                        .replace("commonsense evidence:", "")
                        .strip()
                    )
                    if value_description.lower().startswith("not useful"):
                        value_description = value_description[10:].strip()

                table_description[table_name][column_name.lower().strip()] = {
                    "original_column_name": column_name,
                    "column_name": expanded_column_name,
                    "column_description": column_description,
                    "value_description": value_description,
                }
            logging.info(f"Loaded descriptions from {db_name}")
            could_read = True
            break
        except Exception:
            continue
    if not could_read:
        logging.warning(f"Could not read descriptions from {db_name}")
    return table_description

def get_column_profiles(
    db_manager: Any,
    schema_with_examples: Dict[str, Dict[str, List[str]]],
    use_value_description: bool,
    with_keys: bool,
    with_references: bool,
    tentative_schema: Dict[str, Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Dict[str, str]]:
    """
    Generates column profiles for the schema.

    Args:
        db_manager: Database manager instance
        schema_with_examples: Schema with example values
        use_value_description: Whether to use value descriptions
        with_keys: Whether to include keys
        with_references: Whether to include references
        tentative_schema: Pre-existing schema (optional)

    Returns:
        Dict[str, Dict[str, str]]: Column profiles
    """
    schema_with_descriptions = load_tables_description(
        db_manager.db_id, use_value_description
    )
    
    if tentative_schema:
        simplified_schema = {
            table_name: list(table_info["columns"].keys())
            for table_name, table_info in tentative_schema.items()
        }
    else:
        full_schema = get_db_schema(db_manager.db_id)
        simplified_schema = {
            table_name: list(table_info["columns"].keys())
            for table_name, table_info in full_schema.items()
        }

    database_schema_generator = MultiDbGenerator(
        tentative_schema=DatabaseSchema.from_schema_dict(simplified_schema),
        schema_with_examples=DatabaseSchema.from_schema_dict_with_examples(
            schema_with_examples
        ),
        schema_with_descriptions=DatabaseSchema.from_schema_dict_with_descriptions(
            simplified_schema,
            schema_with_descriptions
        ),
        dbmanager=db_manager,
        add_examples=True,
    )

    return database_schema_generator.get_column_profiles(with_keys, with_references)

def print_schema_friendly(db_name: str) -> None:
    """
    Prints the database schema in a user-friendly format.
    
    Args:
        db_name (str): Name of the database to analyze
    """
    schema = get_db_schema(db_name)
    
    print(f"\n📊 Database Schema: {db_name}\n")
    print("=" * 80)
    
    for table_name, table_info in schema.items():
        print(f"\n📋 Table: {table_name}")
        print("-" * 60)
        
        for col_name, col_info in table_info["columns"].items():
            print(f"\n  📎 {col_name}")
            for key, value in col_info.items():
                if value:  # Only print non-empty values
                    print(f"    ├─ {key}: {value}")
    
    print("\n" + "=" * 80)
    total_tables = len(schema)
    total_columns = sum(len(table["columns"]) for table in schema.values())
    print(f"\nTotal Tables: {total_tables}")
    print(f"Total Columns: {total_columns}")

def generate_create_tables_with_comments(db_name: str) -> Dict[str, str]:
    """
    Generates CREATE TABLE statements with detailed comments for each table in the database.
    
    Args:
        db_name (str): The path to the database file.
        
    Returns:
        Dict[str, str]: Dictionary mapping table names to their CREATE TABLE statements with comments.
    """
    schema = get_db_schema(db_name)
    create_statements = {}
    
    for table_name, table_info in schema.items():
        columns = []
        constraints = []
        
        # Track primary key columns to avoid duplicate declarations
        primary_key_columns = set()
        
        for col_name, col_info in table_info["columns"].items():
            # Build column definition
            col_def = f"\t{col_name} {col_info['data_format']}"
            
            # Add primary key constraint directly to column if it has one
            if col_info["pk_field"]:
                col_def += " primary key"
                primary_key_columns.add(col_name)
            
            # Build column comment parts
            comment_parts = []
            
            # Add examples if available (placeholder - would need to be populated from elsewhere)
            # In a real implementation, you might want to fetch actual examples from the database
            if "value_examples" in col_info and col_info["value_examples"]:
                examples = [f"`{ex}`" for ex in col_info["value_examples"][:3]]
                comment_parts.append(f"examples: {', '.join(examples)}")
            
            # Add expanded column name if different from original
            if col_info["column_name"] != col_info["original_column_name"]:
                comment_parts.append(f"| `{col_info['column_name']}`")
                
            # Add column description if available
            if col_info["column_description"]:
                comment_parts.append(f"description: {col_info['column_description']}")
                
            # Add value description if available
            if col_info["value_description"]:
                comment_parts.append(f"values: {col_info['value_description']}")
                
            # Add the comment to the column definition if we have any parts
            if comment_parts:
                col_def += f" -- {' '.join(comment_parts)}"
                
            columns.append(col_def)
            
            # Add foreign key constraints
            if col_info["fk_field"]:
                # Parse the foreign key reference (format might vary)
                fk_parts = col_info["fk_field"].split('.')
                if len(fk_parts) == 2:
                    ref_table, ref_column = fk_parts
                    constraints.append(
                        f"\tforeign key ({col_name}) references {ref_table} ({ref_column}) on update cascade on delete cascade"
                    )
        
        # Combine everything into final CREATE TABLE statement
        create_stmt = f"CREATE TABLE {table_name}\n("
        create_stmt += ",\n".join(columns)
        
        # Add constraints if any
        if constraints:
            create_stmt += ",\n" + ",\n".join(constraints)
            
        create_stmt += "\n);"
        
        create_statements[table_name] = create_stmt
    
    return create_statements

def get_schema_string(schema: Dict[str, Dict[str, Any]]) -> str:
    """
    Generates a formatted schema string optimized for LLM comprehension.
    
    Args:
        schema (Dict[str, Dict[str, Any]]): The database schema structure as returned by get_db_schema
        
    Returns:
        str: A formatted string containing the complete database schema
    """
    def sanitize_text(text: str) -> str:
        """Sanitizes text by removing problematic characters and normalizing whitespace"""
        if not text:
            return ""
        # Replace newlines and multiple spaces with single space
        cleaned = " ".join(str(text).split())
        # Remove any remaining problematic characters
        cleaned = cleaned.replace("\t", " ").replace("\r", " ")
        return cleaned.strip()

    def needs_backtick(name: str) -> bool:
        """Determines if a field name needs to be enclosed in backticks"""
        # Check for spaces, parentheses, or other special characters
        return bool(re.search(r'[\s\(\)\-\+\[\]\.,:;]', name))

    schema_parts = []
    
    for table_name, table_info in schema.items():
        # Start with CREATE TABLE statement
        schema_parts.append(f"\nCREATE TABLE {table_name}")
        
        # Process each column
        for col_name, col_info in table_info["columns"].items():
            column_parts = []

            formatted_col_name = f"`{col_name}`" if needs_backtick(col_name) else col_name
            column_parts.append(f"    {formatted_col_name} {col_info['data_format']}")
            
            # # Add original column name and data format
            # column_parts.append(f"    {col_name} {col_info['data_format']}")

            if col_info["column_name"] and col_info["column_name"] != col_name:
                expanded_name = sanitize_text(col_info["column_name"])
                formatted_expanded_name = f"`{expanded_name}`" if needs_backtick(expanded_name) else expanded_name
                column_parts.append(f"EXPANDED NAME: {formatted_expanded_name}")

            # Add expanded column name if different from original
            # if col_info["column_name"] and col_info["column_name"] != col_name:
            #     expanded_name = sanitize_text(col_info["column_name"])
            #     column_parts.append(f"EXPANDED NAME: {expanded_name}")
            
            # Add description or generated comment
            description = None
            if col_info["column_description"]:
                description = sanitize_text(col_info["column_description"])
            elif col_info["generated_comment"]:
                description = sanitize_text(col_info["generated_comment"])
                
            if description:
                column_parts.append(f"DESCRIPTION: {description}")
            
            # Add value description if present
            if col_info["value_description"]:
                value_desc = sanitize_text(col_info["value_description"])
                column_parts.append(f"VALUES DESCRIPTION: {value_desc}")
            
            # Add value examples if present
            if "value_examples" in col_info and col_info["value_examples"]:
                examples = [sanitize_text(ex) for ex in col_info["value_examples"]]
                column_parts.append(f"VALUE EXAMPLES: {', '.join(examples)}")
            
            # Add primary key information
            if col_info["pk_field"]:
                column_parts.append(f"PRIMARYKEY: {col_info['pk_field']}")
            
            # Add foreign key information
            if col_info["fk_field"]:
                column_parts.append(f"FOREIGNKEY: {col_info['fk_field']}")
            
            # Join all parts with ' --- '
            schema_parts.append(" --- ".join(column_parts))
        
        # Add separator between tables
        schema_parts.append("-" * 80)
    
    # Join all parts with newlines
    return "\n".join(schema_parts)

def columns_select(
    db_name: str,
    similar_entities: Dict[str, Dict[str, List[str]]],
    similar_columns: Dict[str, Dict[str, Dict[str, str]]]
) -> Dict[str, Dict[str, Any]]:
    """
    Creates a filtered schema containing only tables with columns that are either
    in similar_entities or similar_columns, including their primary and foreign keys.
    For columns in similar_entities, adds their example values under VALUE EXAMPLES.

    Args:
        db_name (str): The database name
        similar_entities (Dict[str, Dict[str, List[str]]]): Table->column->list of similar entities
        similar_columns (Dict[str, Dict[str, Dict[str, str]]]): Table->column->attribute:value mapping

    Returns:
        Dict[str, Dict[str, Any]]: Filtered schema with selected tables and columns
    """
    # Get the complete schema
    full_schema = get_db_schema(db_name)
    filtered_schema: Dict[str, Dict[str, Any]] = {}

    # First pass: identify tables with matching columns
    tables_to_include = set()
    for table_name, table_info in full_schema.items():
        # Check if table has any columns in similar_entities
        if table_name in similar_entities:
            for col_name in similar_entities[table_name]:
                if col_name in table_info["columns"]:
                    tables_to_include.add(table_name)
                    break

        # Check if table has any columns in similar_columns
        if table_name in similar_columns:
            for col_name in similar_columns[table_name]:
                if col_name in table_info["columns"]:
                    tables_to_include.add(table_name)
                    break

    # Second pass: build filtered schema with required columns
    for table_name in tables_to_include:
        table_info = full_schema[table_name]
        filtered_schema[table_name] = {"columns": {}}
        
        # Add columns that are in similar_entities or similar_columns
        columns_to_include = set()
        
        # Add columns from similar_entities
        if table_name in similar_entities:
            columns_to_include.update(similar_entities[table_name].keys())
            
        # Add columns from similar_columns
        if table_name in similar_columns:
            columns_to_include.update(similar_columns[table_name].keys())
            
        # Add primary key columns
        for col_name, col_info in table_info["columns"].items():
            if col_info["pk_field"]:
                columns_to_include.add(col_name)
                
        # Add foreign key columns
        for col_name, col_info in table_info["columns"].items():
            if col_info["fk_field"]:
                columns_to_include.add(col_name)
        
        # Build final columns dict
        for col_name in columns_to_include:
            if col_name in table_info["columns"]:
                # Copy original column info
                filtered_schema[table_name]["columns"][col_name] = table_info["columns"][col_name].copy()
                
                # Add VALUE EXAMPLES if column is in similar_entities
                if (table_name in similar_entities and 
                    col_name in similar_entities[table_name]):
                    filtered_schema[table_name]["columns"][col_name]["value_examples"] = \
                        similar_entities[table_name][col_name]

    return filtered_schema

def full_columns_with_entities(
    db_name: str,
    similar_entities: Dict[str, Dict[str, List[str]]],
) -> Dict[str, Dict[str, Any]]:
    """
    Creates a complete schema that includes all tables and columns, adding VALUE EXAMPLES
    from similar_entities where available.

    Args:
        db_name (str): The database name
        similar_entities (Dict[str, Dict[str, List[str]]]): Table->column->list of similar entities

    Returns:
        Dict[str, Dict[str, Any]]: Complete schema with value examples added where available
    """
    # Get the complete schema
    full_schema = get_db_schema(db_name)
    enriched_schema: Dict[str, Dict[str, Any]] = {}

    # Process all tables and columns
    for table_name, table_info in full_schema.items():
        enriched_schema[table_name] = {"columns": {}}
        
        # Process all columns
        for col_name, col_info in table_info["columns"].items():
            # Copy original column info
            enriched_schema[table_name]["columns"][col_name] = col_info.copy()
            
            # Add VALUE EXAMPLES if column is in similar_entities
            if (table_name in similar_entities and 
                col_name in similar_entities[table_name]):
                enriched_schema[table_name]["columns"][col_name]["value_examples"] = \
                    similar_entities[table_name][col_name]

    return enriched_schema

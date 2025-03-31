# Define tools (functions) for questions execution
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_vscode_status",
            "description": "Executes a given command to check the status of VS Code and returns the output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute in the system shell to check VS Code's status."
                    }
                },
                "required": [
                    "command"
                ]
            },
            "returns": {
                "type": "string",
                "description": "The output of the executed command, or an error message if the command fails."
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_https_request",
            "description": "Sends an HTTPS request to the specified URL with query parameters and returns the JSON response.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to send the HTTPS request to."
                    },
                    "email": {
                        "type": "string",
                        "description": "The email address to include as a query parameter."
                    }
                },
                "required": [
                    "url",
                    "email"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_prettier_and_hash",
            "description": "Downloads a file (e.g. .md) to a specified directory, ensures it is correctly named, runs Prettier formatting, and computes its SHA-256 checksum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the downloaded file (e.g. .md) to be formatted and hashed."
                    }
                },
                "required": [
                    "file_name"
                ],
                "additionalProperties": False
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_google_sheets_expression",
            "description": "Evaluates a Google Sheets formula and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A valid Google Sheets formula in string format."
                    }
                },
                "required": [
                    "expression"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_excel_sheets_expression",
            "description": "Evaluates an Excel formula and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A valid Excel formula in string format."
                    }
                },
                "required": [
                    "expression"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_hidden_input_value",
            "description": "Extracts the value of a hidden input field from the given HTML string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html": {
                        "type": "string",
                        "description": "A valid HTML string containing an input element with type='hidden'."
                    }
                },
                "required": [
                    "html"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_wednesdays",
            "description": "Counts the number of Wednesdays between two given dates (inclusive).",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "The start date in 'YYYY-MM-DD' format."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date in 'YYYY-MM-DD' format."
                    }
                },
                "required": [
                    "start_date",
                    "end_date"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_answer_from_csv_zip",
            "description": "Extracts the value in the 'answer' column from a CSV file inside a ZIP archive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_path": {
                        "type": "string",
                        "description": "The file path to the ZIP archive containing a single extract.csv file."
                    }
                },
                "required": [
                    "zip_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sort_json_list",
            "description": "Sorts a JSON array of person objects by age (ascending) and name (alphabetical) for ties.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_array": {
                        "type": "array",
                        "description": "Array of person objects with 'name' and 'age' fields",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string"
                                },
                                "age": {
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "name",
                                "age"
                            ],
                            "additionalProperties": False
                        }
                    },
                    "first_parameter": {
                        "type": "string",
                        "description": "Primary sort field - must be 'age' (default sorting key)"
                    },
                    "second_parameter": {
                        "type": "string",
                        "description": "Secondary sort field - must be 'name' (tiebreaker field)"
                    }
                },
                "required": [
                    "json_array",
                    "first_parameter",
                    "second_parameter"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_data_values_of_foo_divs",
            "description": "Finds all <div> elements with class 'foo' and sums their 'data-value' attributes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html": {
                        "type": "string",
                        "description": "The HTML content containing the hidden elements."
                    }
                },
                "required": [
                    "html"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_unicode_values_from_zip",
            "description": "Extracts and processes CSV and TXT files from a ZIP archive, summing values for specific Unicode symbols.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "The file path of the ZIP archive containing the CSV and TXT files."
                    }
                },
                "required": [
                    "zip_file_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_and_push_github_repo",
            "description": "Creates a public GitHub repository, commits a JSON file, and pushes it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_data": {
                        "type": "object",
                        "description": "The JSON object to be stored in the file.",
                        "additionalProperties": False
                    }
                },
                "required": [
                    "json_data"
                ],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "replace_text_and_compute_sha256",
            "description": "Extracts a ZIP file, replaces all 'IITM' occurrences, and calculates the SHA-256 checksum of concatenated file contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_path": {
                        "type": "string",
                        "description": "The file path of the ZIP archive containing the files to be processed."
                    }
                },
                "required": [
                    "zip_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_and_calculate_filtered_size",
            "description": "Extracts a ZIP file, lists files with their attributes, and calculates the total size of files meeting specified size and modification date conditions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_path": {
                        "type": "string",
                        "description": "The file path of the ZIP archive to be extracted."
                    },
                    "target_timestamp": {
                        "type": "string",
                        "description": "The reference timestamp in the format 'Sun, 19 Jul, 2020, 6:50 PM IST' to filter files modified on or after this date."
                    }
                },
                "required": [
                    "zip_path",
                    "target_timestamp"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_and_rename_files",
            "description": "Moves all extracted files into a single directory, renames them by incrementing digits, and computes the SHA-256 checksum of the sorted grep output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_path": {
                        "type": "string",
                        "description": "The file path of the ZIP archive containing the files (i.e. .txt) to be processed."
                    }
                },
                "required": [
                    "zip_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_and_count_different_lines",
            "description": "Extracts a ZIP file, finds two nearly identical text files (a.txt and b.txt), and counts the number of differing lines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_path": {
                        "type": "string",
                        "description": "The file path of the ZIP archive containing .txt files (e.g. a.txt and b.txt.)"
                    }
                },
                "required": [
                    "zip_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_sql_ticket_sales_query",
            "description": 'This function is selected when it asks to Give the SQL query to calculates the total sales for a specified ticket type (e.g. "GOLD" or "SILVER" or "BRONZE"). as given',
            "parameters": {
                "type": "object",
                "properties": {
                    "item_type": {
                        "type": "string",
                        "description": 'The ticket type (e.g. "GOLD" or "SILVER" or "BRONZE") to filter transactions. The input is case-insensitive and will be trimmed and converted to lowercase.'
                    }
                },
                "required": [
                    "item_type"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_markdown_documentation",
            "description": "Generates a structured Markdown document based on the given topic and formatting requirements.",
            "arguments": {
                "topic": "Analysis of the number of steps walked each day for a week",
                "format": "Markdown",
                "required_elements": [
                    "Heading 1",
                    "Heading 2",
                    "Bold text",
                    "Italic text",
                    "Inline code",
                    "Code block",
                    "Bulleted list",
                    "Numbered list",
                    "Table",
                    "Hyperlink",
                    "Image",
                    "Blockquote"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_python_code_for_Analyze_the_sentiment",
            "description": "Generates a Python script using httpx to analyze the sentiment of a given text by sending a POST request to OpenAI's API. The script categorizes the sentiment as GOOD, BAD, or NEUTRAL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "string_text": {
                        "type": "string",
                        "description": "The input text whose sentiment needs to be analyzed."
                    }
                },
                "required": [
                    "string_text"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_token_count",
            "description": "Calculates the number of input tokens used by a given text when sent to an OpenAI model. It sends a request to OpenAI's API with the provided text and returns the token count.",
            "parameters": {
                "type": "object",
                "properties": {
                    "str_content": {
                        "type": "string",
                        "description": "The input text whose token count needs to be calculated. Example: 'List only the valid English words from these: rfhT, tqNS, OeVxG1kl, nYG4k, p7, qms1twO, a5, jG, Pnn8, A7l, e1myHNhyjA, G, 7iDikmL1V, oStE5LhRd, lQSv, hBSHNMCt, jiOOyG, WES9XjwqS, 8mtRDy, dhlKW'"
                    }
                },
                "required": [
                    "str_content"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "base_64_encoding",
            "description": "Encodes an image file to base64 and constructs a JSON body for sending to OpenAI's API to extract text from the image.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "The file path of the image to be encoded in base64 format and sent to the OpenAI API for text extraction."
                    }
                },
                "required": [
                    "image_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "embeddings_openai_and_local_models",
            "description": "Generates the JSON body for a POST request to OpenAI's API to obtain text embeddings for two given messages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "first_message": {
                        "type": "string",
                        "description": "The first transaction verification message to be embedded."
                    },
                    "second_message": {
                        "type": "string",
                        "description": "The second transaction verification message to be embedded."
                    }
                },
                "required": [
                    "first_message",
                    "second_message"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "embedding_similarity_topic_modeling",
            "description": "Calculates the cosine similarity between each pair of given text embeddings and returns the most similar pair.",
            "parameters": {
                "type": "object",
                "properties": {
                    "embeddings": {
                        "type": "string",
                        "description": "A dictionary variable which have mapping phrases to their corresponding embedding vectors(e.g. embeddings = {[],[]})",
                    }
                },
                "required": [
                    "embeddings"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "semantic_document_similarity_ranking",
        "description": "This function processes a user's search query and identifies the most relevant documents from a provided list based on semantic similarity. It first generates text embeddings for each document and the search query using a pre-trained text embedding model (e.g., OpenAI’s text-embedding-3-small). Next, it calculates cosine similarity scores between the query embedding and each document embedding. The function then ranks the documents in descending order of similarity and returns the three most relevant documents based on their similarity scores. The results help users retrieve the most contextually appropriate documents from an internal knowledge base.",
            "parameters": {},
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "query_to_function_mapping",
            "description": "Processes a natural language query, determines the most relevant predefined function to execute, extracts necessary parameters from the query, and returns a structured response containing the function name and its arguments in JSON format. This function enables automated query interpretation and function execution in a FastAPI-based system.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_ducks_on_page",
            "description": "Extracts and analyzes ODI batting statistics from ESPN Cricinfo to count the total number of ducks on a specified page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "page_number": {
                        "type": "integer",
                        "description": "The page number of ESPN Cricinfo's ODI batting statistics to retrieve data from."
                    }
                },
                "required": [
                    "page_number"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_rated_movies",
            "description": "Fetches movie details from IMDb for titles within a specified rating range, extracting information such as IMDb ID, title, release year, and rating.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter_start": {
                        "type": "number",
                        "description": "The minimum IMDb rating (inclusive) for filtering movies."
                    },
                    "filter_end": {
                        "type": "number",
                        "description": "The maximum IMDb rating (inclusive) for filtering movies."
                    }
                },
                "required": [
                    "filter_start",
                    "filter_end"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_country_outline",
            "description": "Fetches the Wikipedia page for a given country, extracts headings (H1 to H6), and returns a Markdown-formatted outline.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_bbc_weather_forecast",
            "description": "Fetches and processes weather forecast data for a given location using the BBC Weather API. It retrieves the location ID, fetches the weather forecast, and returns a JSON object mapping each localDate to its corresponding enhancedWeatherDescription.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The name of the location (city, airport, district) for which the weather forecast is needed."
                    }
                },
                "required": [
                    "location"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_max_latitude",
            "description": "Retrieves the maximum latitude of the bounding box for a specified city and country using the Nominatim API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city for which to retrieve the bounding box data."
                    },
                    "country": {
                        "type": "string",
                        "description": "The name of the country in which the city is located."
                    }
                },
                "required": [
                    "city",
                    "country"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_latest_hn_post",
            "description": "Retrieves the latest Hacker News post mentioning a specified topic with a minimum number of points using the HNRSS API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The technology topic to search for in Hacker News posts."
                    },
                    "min_points": {
                        "type": "integer",
                        "description": "The minimum number of points a post must have to be considered relevant."
                    }
                },
                "required": [
                    "topic",
                    "min_points"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_newest_github_user",
            "description": "Retrieves the newest GitHub user from a specified location with a minimum number of followers, ensuring the account was created before a given time threshold.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or region to filter GitHub users by location (e.g., 'Dublin')."
                    },
                    "min_followers": {
                        "type": "integer",
                        "description": "The minimum number of followers a user must have to be considered."
                    },
                    "time_threshold": {
                        "type": "string",
                        "description": "The cutoff date and time (in ISO 8601 format) to exclude ultra-new users who joined after this date."
                    }
                },
                "required": [
                    "location",
                    "min_followers",
                    "time_threshold"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "setup_github_action",
            "description": "Creates and configures a GitHub Actions workflow to run daily, make automated commits, and push changes to a repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address to use for Git commits."
                    }
                },
                "required": [
                    "email"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_total_marks",
            "description": "Extracts student marks data from a PDF file, filters students based on Economics marks threshold and group range, and calculates the total Economics marks for the filtered students.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pdf_path": {
                        "type": "string",
                        "description": "The file path of the PDF document containing student marks."
                    },
                    "subject": {
                        "type": "string",
                        "description": "The subject name to filter marks for, e.g., 'Economics'."
                    },
                    "threshold_marks": {
                        "type": "integer",
                        "description": "The minimum marks threshold for filtering students."
                    },
                    "groups_range": {
                        "type": "string",
                        "description": "The range of student groups to include, formatted as 'start-end' (e.g., '1-29')."
                    }
                },
                "required": [
                    "pdf_path",
                    "subject",
                    "threshold_marks",
                    "groups_range"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clean_and_calculate_margin",
            "description": "Cleans and processes sales transaction data from an Excel file, standardizes country names and date formats, extracts relevant product names, and calculates the total margin for a specified product, country, and time filter.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The file path of the Excel sheet containing sales transaction data."
                    },
                    "timestamp": {
                        "type": "string",
                        "description": "The cutoff date and time (in ISO 8601 format) to filter transactions that occurred up to and including this date."
                    },
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product to filter transactions (extracted from the Product field before the slash)."
                    },
                    "country_code": {
                        "type": "string",
                        "description": "The standardized two-letter country code (e.g., 'FR' for France) to filter transactions."
                    }
                },
                "required": [
                    "file_path",
                    "timestamp",
                    "product_name",
                    "country_code"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_unique_students",
            "description": "Determines the number of unique students based on student IDs extracted from a text file containing student marks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the text file containing student marks data."
                    }
                },
                "required": [
                    "filename"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_peak_requests",
            "description": "Counts the number of successful GET requests for a specific page within a defined time window on a specific day from Apache logs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "page": {
                        "type": "string",
                        "description": "The target page URL prefix to filter requests (e.g., '/kannadamp3/')."
                    },
                    "start_time_str": {
                        "type": "string",
                        "description": "Start time in 'HH:MM' format (e.g., '06:00')."
                    },
                    "end_time_str": {
                        "type": "string",
                        "description": "End time in 'HH:MM' format (e.g., '22:00')."
                    },
                    "target_day": {
                        "type": "string",
                        "description": "The target day of the week (e.g., 'Tuesday')."
                    }
                },
                "required": [
                    "page",
                    "start_time_str",
                    "end_time_str",
                    "target_day"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_bandwidth_usage",
            "description": "Analyzes an Apache log file to determine the IP consuming the highest bandwidth for a specific URL prefix on a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date to filter logs in 'YYYY-MM-DD' format (e.g., '2024-05-23')."
                    },
                    "url_prefix": {
                        "type": "string",
                        "description": "The target URL prefix to filter requests (e.g., '/hindimp3/')."
                    }
                },
                "required": [
                    "date",
                    "url_prefix"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_product_sales_by_city",
            "description": "Analyzes sales data to determine the total units sold for a specific product in a city while handling phonetic variations in city names.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to the JSON file containing sales data."
                    },
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product to filter sales entries (e.g., 'Cheese')."
                    },
                    "city_name": {
                        "type": "string",
                        "description": "The target city name for sales aggregation, accounting for phonetic variations (e.g., 'Buenos Aires')."
                    },
                    "unit_sales": {
                        "type": "integer",
                        "description": "The minimum number of units sold to include a sales entry (e.g., 53)."
                    }
                },
                "required": [
                    "filename",
                    "product_name",
                    "city_name",
                    "unit_sales"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_total_sales",
            "description": "Calculates the total sales value from a JSON file containing sales data, handling missing or truncated fields.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the JSON file containing sales data."
                    }
                },
                "required": [
                    "file_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_key_occurrences",
            "description": "Counts the occurrences of a specific key in a deeply nested JSON log file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_file_path": {
                        "type": "string",
                        "description": "Path to the JSON log file."
                    },
                    "target_key": {
                        "type": "string",
                        "description": "The key to search for in the JSON structure."
                    }
                },
                "required": [
                    "json_file_path",
                    "target_key"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_high_engagement_posts",
            "description": "Retrieves post IDs from a DuckDB table that have at least one comment with a specified number of useful stars and were created after a given timestamp.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "string",
                        "description": "The minimum timestamp (ISO 8601 format) to filter recent posts."
                    },
                    "useful_stars": {
                        "type": "integer",
                        "description": "The minimum number of useful stars a comment must have for a post to be considered highly engaging."
                    }
                },
                "required": [
                    "timestamp",
                    "useful_stars"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_and_transcribe",
            "description": "Downloads a YouTube video's audio, extracts the specified segment, and transcribes it using a Whisper model.",
            "parameters": {
                "type": "object",
                "properties": {
                    "youtube_url": {
                        "type": "string",
                        "description": "The URL of the YouTube video containing the mystery audiobook."
                    },
                    "start_time": {
                        "type": "number",
                        "description": "The start time in seconds from where the transcription should begin."
                    },
                    "end_time": {
                        "type": "number",
                        "description": "The end time in seconds where the transcription should stop."
                    },
                },
                "required": [
                    "youtube_url",
                    "start_time",
                    "end_time"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
]

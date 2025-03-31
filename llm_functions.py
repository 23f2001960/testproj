import subprocess
import jellyfish
import hashlib
import zipfile
import pandas as pd
import json
import numpy as np
import re
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import datetime
import os
import shutil
import hashlib
import requests
import time
import base64
from collections import defaultdict
import gzip
from urllib.parse import urlencode
import feedparser
import urllib.parse
import pdfplumber
from PIL import Image
import yt_dlp
from pydub import AudioSegment
import whisper
import subprocess
import threading
from dateutil import parser
import pycountry
from dotenv import load_dotenv


load_dotenv()

# required environment variables:
github_pat_token = os.getenv("GITHUB_PAT_TOKEN")
aiproxy_key = os.getenv("AIPROXY_KEY")

def run_server():
    import time
    import signal
    
    # Check if port 8000 is already in use
    check_process = subprocess.run(
        ["sudo", "lsof", "-t", "-i", ":8000"],  # Get only process IDs
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    if check_process.stdout:
        print("Port 8000 is already in use. Killing the process...")
        pids = check_process.stdout.strip().split("\n")
        for pid in pids:
            os.kill(int(pid), signal.SIGTERM)  # Send termination signal
        time.sleep(2)  # Give some time for cleanup

    # Start the FastAPI server as a subprocess
    process = subprocess.Popen(
        ["python", "server.py"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    # Function to terminate the server after 40 seconds
    def terminate_server():
        time.sleep(40)
        process.terminate()
        process.wait()  # Ensure process is cleaned up
    
    # Start the termination thread
    terminator_thread = threading.Thread(target=terminate_server, daemon=True)
    terminator_thread.start()
    
    # Return the server URL
    return "http://127.0.0.1:8000"

##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
# GA 1
#############################
## Q. 1                       #####
def get_vscode_status(command):
    print(command)
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, check=True)
        print(result)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Error: Command not found. Ensure VS Code is installed and available in PATH."
    
#############################
## Q. 2                       #####

def send_https_request(url: str, email: str) -> str:
    
    command = ["uv", "run", "--with", "httpie", "--", "https", url, f"email=={email}"]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    try:
        response = json.loads(result.stdout)
        return json.dumps(response, indent=4)
    except json.JSONDecodeError:
        return None

#############################
## Q. 3
def run_prettier_and_hash(file_name: str) -> str:
    """
    Formats the README.md file using Prettier and computes its SHA-256 checksum.

    Args:
        readme_path (str): Path to the README.md file.

    Returns:
        str: SHA-256 checksum of the formatted file.
    """
    try:
        # Run Prettier and pipe the output to sha256sum
        result = subprocess.run(
            ["npx", "-y", "prettier@3.4.2", file_name, "|", "sha256sum"],
            shell=True,
            capture_output=True,
            text=True
        )

        # Compute SHA-256 hash
        sha256_hash = hashlib.sha256(result.stdout.encode()).hexdigest()
        return sha256_hash

    except subprocess.CalledProcessError as e:
        return f"Error running Prettier: {e}"
    
#############################
## Q. 4                       #####
def evaluate_google_sheets_expression(expression: str) -> int:
    match = re.match(r"=SUM\(ARRAY_CONSTRAIN\(SEQUENCE\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\),\s*(\d+),\s*(\d+)\)\)", expression)
    
    if not match:
        raise ValueError("Invalid expression format")
    
    rows, cols, start, step, constrain_rows, constrain_cols = map(int, match.groups())
    
    # Generate the SEQUENCE array
    sequence_array = np.array([[start + (i * step) for i in range(cols)] for _ in range(rows)])
    
    # Apply ARRAY_CONSTRAIN to get the required subset
    constrained_array = sequence_array[:constrain_rows, :constrain_cols]
    
    # Compute the SUM
    return int(np.sum(constrained_array))

#############################
## Q. 5                       #####
def evaluate_excel_sheets_expression(expression: str) -> int:
    # Updated regex pattern to correctly capture numbers inside {}
    pattern = r"=SUM\(TAKE\(SORTBY\(\{([\d,\s]+)\}, \{([\d,\s]+)\}\), (\d+), (\d+)\)\)"
    
    match = re.match(pattern, expression)
    if not match:
        raise ValueError("Invalid expression format")

    # Extract values and sort keys
    values = list(map(int, match.group(1).split(',')))
    sort_keys = list(map(int, match.group(2).split(',')))
    sort_order = int(match.group(3))  # 1 for ascending, -1 for descending
    take_count = int(match.group(4))  # Number of elements to take after sorting

    if len(values) != len(sort_keys):
        raise ValueError("Values and sort_keys arrays must have the same length")

    # Sort values based on sort_keys
    sorted_values = [x for _, x in sorted(zip(sort_keys, values), reverse=(sort_order == -1))]

    # Take the specified number of elements
    taken_values = sorted_values[:take_count]

    # Return the sum of taken values
    return sum(taken_values)

#############################
## Q. 6                       #####
def get_hidden_input_value(html):
    soup = BeautifulSoup(html, 'html.parser')
    hidden_input = soup.find('input', {'type': 'hidden'})
    return hidden_input['value'] if hidden_input else None

#############################
## Q. 7                       #####
def count_wednesdays(start_date = None, end_date = None) -> int:
    """
    Counts the number of Wednesdays between two dates (inclusive).
    
    :param start_date: Start date in 'YYYY-MM-DD' format.
    :param end_date: End date in 'YYYY-MM-DD' format.
    :return: Number of Wednesdays in the given range.
    """
    if not start_date:
        start = date(1990, 8, 19)
    else:
        start = date.fromisoformat(start_date)
        
    if not end_date:
        end = date(2016, 12, 8)
    else:
        end = date.fromisoformat(end_date)
    
    count = 0
    current = start
    
    while current <= end:
        if current.weekday() == 2:  # Wednesday
            count += 1
        current += timedelta(days=1)
    
    return count

#############################
## Q. 8                       #####
def get_answer_from_csv_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all contents
        zip_ref.extractall("temp_extracted")
        
        # Read the CSV file
        csv_path = "temp_extracted/extract.csv"
        df = pd.read_csv(csv_path)
        
        # Return the values in the "answer" column
        return df["answer"].values[0]
    
#############################
## Q. 9                       #####
def sort_json_list(first_parameter: str, second_parameter: str, json_list: list) -> str:
    """
    Sorts a list of JSON objects by the specified first and second parameters.

    Args:
        first_parameter (str): The primary key to sort by.
        second_parameter (str): The secondary key to sort by.
        json_list (list): A list of dictionaries representing JSON objects.

    Returns:
        str: A JSON-formatted string of the sorted list.
    """
    sorted_list = sorted(json_list, key=lambda x: (x[first_parameter], x[second_parameter]))
    return json.dumps(sorted_list, separators=(',', ':'))

#############################
## Q. 10

#############################
## Q. 11                       #####
def sum_data_values_of_foo_divs(html: str) -> int:
    """
    Parses the given HTML, finds all <div> elements with class 'foo' inside the hidden element,
    and sums up their 'data-value' attributes.
    
    :param html: HTML content as a string.
    :return: Sum of 'data-value' attributes of matching <div> elements.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # Find the hidden container
    hidden_element = soup.find("div", class_="d-none")
    
    if not hidden_element:
        return 0  # Return 0 if the hidden element is not found
    
    # Find all <div> elements with class 'foo' inside the hidden element
    foo_divs = hidden_element.find_all("div", class_="foo")
    
    # Sum their 'data-value' attributes
    total = sum(int(div.get("data-value", 0)) for div in foo_divs if div.has_attr("data-value"))
    
    return total

#############################
## Q. 12                       ##
def sum_unicode_values_from_zip(zip_file):
    target_symbols = {"„", "“", "–"}  # Set of symbols to match
    total_sum = 0

    # Step 1: Extract ZIP file
    extract_folder = "q_unicode_extracted"
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Step 2: Define file encoding and delimiter settings
    file_configs = [
        ("data1.csv", "cp1252", ","),
        ("data2.csv", "utf-8", ","),
        ("data3.txt", "utf-16", "\t")
    ]

    # Step 3: Process each file
    for file_name, encoding, delimiter in file_configs:
        file_path = os.path.join(extract_folder, file_name)
        df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)

        # Ensure correct column names
        df.columns = ["symbol", "value"]

        # Convert "value" column to numeric (in case of errors, force conversion)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        # Filter rows where the symbol matches target_symbols and sum up the values
        total_sum += df[df["symbol"].isin(target_symbols)]["value"].sum()

    return total_sum

#############################
## Q. 13                       #####
def create_and_push_github_repo():
    repo_name = "my-public-repo"
    github_username = "21f3002277"
    
    # Step 1: Create a new public repository using GitHub API
    create_repo_cmd = f'curl -u "{github_username}:{github_pat_token}" https://api.github.com/user/repos -d \'{{"name": "{repo_name}", "private": false}}\''
    subprocess.run(create_repo_cmd, shell=True, check=True)

    # Step 2: Create a local directory
    if os.path.exists(repo_name):
        os.system(f"rm -rf {repo_name}")  # Remove if exists
    os.makedirs(repo_name)

    # Step 3: Create email.json
    email_data = {"email": "21f3002277@ds.study.iitm.ac.in"}
    json_file_path = os.path.join(repo_name, "email.json")
    with open(json_file_path, "w") as f:
        json.dump(email_data, f, indent=4)

    # Step 4: Initialize Git and push to GitHub
    os.chdir(repo_name)
    subprocess.run("git init", shell=True, check=True)
    subprocess.run(f'git remote add origin https://{github_username}:{github_pat_token}@github.com/{github_username}/{repo_name}.git', shell=True, check=True)
    subprocess.run("git add email.json", shell=True, check=True)
    subprocess.run('git commit -m "Initial commit: Adding email.json"', shell=True, check=True)
    subprocess.run("git branch -M main", shell=True, check=True)
    subprocess.run("git push -u origin main", shell=True, check=True)

    # Step 5: Return the raw GitHub URL for verification
    raw_url = f"https://raw.githubusercontent.com/{github_username}/{repo_name}/main/email.json"
    return raw_url

#############################
## Q. 14                       #####
def replace_text_and_compute_sha256(zip_path):
    # Create a new folder with the same name as the zip file (without extension)
    extract_folder = zip_path.replace('.zip', '')
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)  # Remove if already exists
    os.makedirs(extract_folder)

    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Process all extracted files
    for root, _, files in os.walk(extract_folder):
        for file in files:
            file_path = os.path.join(root, file)

            # Read file content (preserve original line endings)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Replace "IITM" (case-insensitive) with "IIT Madras"
            updated_content = re.sub(r'IITM', 'IIT Madras', content, flags=re.IGNORECASE)

            # Write back to the file
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                f.write(updated_content)

    # Compute SHA-256 hash of concatenated contents
    sha256_hash = hashlib.sha256()
    for root, _, files in sorted(os.walk(extract_folder)):  # Sort to ensure consistent ordering
        for file in sorted(files):  # Sort files alphabetically
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256_hash.update(chunk)

    return sha256_hash.hexdigest()

#############################
## Q. 15                       #####
def extract_and_calculate_filtered_size(zip_path, target_timestamp):
    # Extract folder name
    extract_folder = zip_path.replace('.zip', '')
    if os.path.exists(extract_folder):
        os.system(f"rm -rf {extract_folder}")  # Remove existing folder
    os.makedirs(extract_folder)

    # Use the system's unzip command to preserve timestamps
    subprocess.run(["unzip", "-q", zip_path, "-d", extract_folder], check=True)

    # Target date and time (Sun, 19 Jul, 2020, 6:50 PM IST)
    target_date = datetime.datetime.strptime(target_timestamp, "%a, %d %b, %Y, %I:%M %p IST")

    total_size = 0

    # Iterate over all extracted files
    for root, _, files in os.walk(extract_folder):
        for file in files:
            file_path = os.path.join(root, file)
            stat_info = os.stat(file_path)

            # File size and modification time
            size = stat_info.st_size
            modified_time = datetime.datetime.fromtimestamp(stat_info.st_mtime)

            # Check if file meets criteria
            if size >= 7564 and modified_time >= target_date:
                total_size += size

    return total_size

#############################
## Q. 16                       #####
def move_and_rename_files(zip_path):
    # Extract folder name
    extract_folder = zip_path.replace('.zip', '')
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)  # Remove if exists
    os.makedirs(extract_folder)

    # Use system unzip to extract while preserving timestamps
    subprocess.run(["unzip", "-q", zip_path, "-d", extract_folder], check=True)

    # Create a new empty folder to move all files into
    new_folder = os.path.join(extract_folder, "all_files")
    os.makedirs(new_folder)

    # Move all files from subdirectories into new_folder
    for root, _, files in os.walk(extract_folder):
        if root == new_folder:
            continue  # Skip if already in new_folder
        for file in files:
            old_path = os.path.join(root, file)
            new_path = os.path.join(new_folder, file)
            shutil.move(old_path, new_path)

    # Rename all files in new_folder by replacing digits with the next (9 → 0)
    for filename in os.listdir(new_folder):
        new_filename = re.sub(r'\d', lambda x: str((int(x.group(0)) + 1) % 10), filename)
        os.rename(os.path.join(new_folder, filename), os.path.join(new_folder, new_filename))

    # Run grep, sort, and sha256sum
    result = subprocess.run(
        "grep . * | LC_ALL=C sort | sha256sum",
        shell=True, cwd=new_folder, capture_output=True, text=True
    )

    return result.stdout.strip()

#############################
## Q. 17                       ##
def extract_and_count_different_lines(zip_path):
    # Extract folder name
    extract_folder = zip_path.replace('.zip', '')
    if os.path.exists(extract_folder):
        os.system(f"rm -rf {extract_folder}")  # Remove existing folder
    os.makedirs(extract_folder)

    # Extract using unzip (preserves timestamps)
    subprocess.run(["unzip", "-q", zip_path, "-d", extract_folder], check=True)

    # Define file paths
    file_a = os.path.join(extract_folder, "a.txt")
    file_b = os.path.join(extract_folder, "b.txt")

    # Compare files line by line
    with open(file_a, "r", encoding="utf-8") as f1, open(file_b, "r", encoding="utf-8") as f2:
        diff_count = sum(1 for line1, line2 in zip(f1, f2) if line1 != line2)

    return diff_count

#############################
## Q. 18                       ##
def generate_sql_ticket_sales_query(item_type):
    # Define the SQL query
    query = f'''
SELECT SUM(units * price) AS total_sales
FROM tickets
WHERE TRIM(LOWER(type)) = '{item_type.lower()}';
    '''

    return query

##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
# GA 2
#############################
## Q. 1
def generate_markdown_documentation():
    markdown = f'''
# Weekly Step Analysis

An **imaginary analysis** of the number of steps walked each day for a week, comparing trends over time and with friends.

---

## Methodology

To perform this analysis, we followed these steps:

1. *Collect data* for daily steps over a week.
2. Store data in a structured format (e.g., a CSV file).
3. Compare individual steps with the average of friends.
4. Visualize trends using charts.

Below is a snippet of the Python code used to process the data:

Store data in a structured format (e.g., `steps_data.csv`).

```python
import pandas as pd

data = pd.read_csv("steps_data.csv")
average_steps = data["steps"].mean()
print(f"Average steps: {{average_steps}}")
```

## **Result**:

- **Daily Steps Comparison**:

> The data for daily steps over a week is summarized in the table below

| Day	    | Your Steps	| Average Steps (Friends)  |
|-----------|---------------|--------------------------|
| Monday	| 7,000	        | 8,500                    |
| Tuesday	| 8,200	        | 9,000                    |
| Wednesday	| 9,500	        | 8,700                    |
| Thursday	| 10,000	    | 9,300                    |
| Friday	| 6,800	        | 7,500                    |
| Saturday	| 12,000	    | 10,000                   |
| Sunday	| 11,500	    | 9,800                    |


## **Conclusion**

Regular tracking of steps helps identify trends and areas for improvement. For future analysis:
- Increase weekday activity.
- Compare data for multiple weeks.
(![not found](https://images.squarespace-cdn.com/content/v1/58501b0cf5e23149e5589e12/1680846606959-LLN74OY9Q3IVMUERW3GB/unsplash-image-Kx385zuJai4.jpg?format=1500w)]
For more information, check out this ([guide to increasing daily steps.](https://www.mayoclinic.org/healthy-lifestyle/fitness/in-depth/10000-steps/art-20317391))
    '''
    return markdown

#############################
## Q. 2
def compress_png_losslessly(input_path):
    output_path = "compressed_shapes.png"
    
    # Step 1: Reduce PNG size using pngquant (Lossless 8-bit conversion)
    subprocess.run(["pngquant", "--quality", "100", "--speed", "1", "--force", "--output", output_path, input_path], check=True)
    
    # Step 2: Optimize PNG using optipng
    subprocess.run(["optipng", "-o7", output_path], check=True)
    
    # Step 3: Strip metadata using pngcrush (optional, if needed)
    subprocess.run(["pngcrush", "-rem", "alla", "-reduce", "-brute", output_path, "final_shapes.png"], check=True)
    
    # Check final file size
    if os.path.getsize("final_shapes.png") <= 1500:
        return "final_shapes.png"
    else:
        return "Compression failed to reach 1,500 bytes."
    
#############################
## Q. 3
def publish_github_pages():
    """Creates a GitHub repo, pushes an HTML file, enables GitHub Pages, and returns the URL."""
    
    username="21f3002277"
    repo_name="my-github-pages"
    
    GITHUB_API = "https://api.github.com/user/repos"
    PAGES_API = f"https://api.github.com/repos/{username}/{repo_name}/pages"
    LOCAL_PATH = f"./{repo_name}"
    GIT_URL = f"https://{username}:{github_pat_token}@github.com/{username}/{repo_name}.git"  # Use token for authentication

    # Step 1: Create GitHub repository (if not exists)
    response = requests.post(
        GITHUB_API,
        json={"name": repo_name, "private": False},
        headers={"Authorization": f"token {github_pat_token}"},  # Authenticate using PAT
    )
    if response.status_code not in [201, 422]:  # 422 means repo already exists
        return f"❌ Failed to create repo: {response.text}"

    # Step 2: Initialize local repo and add index.html
    os.makedirs(LOCAL_PATH, exist_ok=True)
    os.chdir(LOCAL_PATH)

    with open("index.html", "w") as f:
        f.write(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Showcase</title>
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const email = "21f3002277@ds.study.iitm.ac.in";
            document.getElementById('email').innerHTML = `<a href="mailto:${{email}}">${{email}}</a>`;
        }});
    </script>
</head>
<body>
    <h1>Welcome to My Showcase</h1>
    <p>This is where I showcase my work!</p>
    <p>For inquiries, you can reach me at: <span id="email"></span></p>
</body>
</html>
''')

    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "branch", "-m", "main"], check=True)

    # Step 3: Set up remote (remove if already exists)
    subprocess.run(["git", "remote", "remove", "origin"], check=False)
    subprocess.run(["git", "remote", "add", "origin", GIT_URL], check=True)

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

    # Step 4: Wait for GitHub to recognize the branch
    time.sleep(10)

    # Step 5: Enable GitHub Pages
    response = requests.post(
        PAGES_API,
        json={"source": {"branch": "main", "path": "/"}},
        headers={"Authorization": f"token {github_pat_token}"},  # Authenticate using PAT
    )
    if response.status_code not in [200, 201]:
        return f"❌ Failed to enable GitHub Pages: {response.text}"

    # Step 6: Get GitHub Pages URL
    time.sleep(5)
    response = requests.get(PAGES_API, headers={"Authorization": f"token {github_pat_token}"})
    if response.status_code == 200:
        return f"🌐 GitHub Pages live at: https://{username}.github.io/{repo_name}/"

    return "❌ Could not retrieve GitHub Pages URL."

#############################
## Q. 4


#############################
## Q. 5


#############################
## Q. 6
def deploy_to_vercel(config_file="q-vercel-python.json"):
    vercel_token="aJlVJtuFTuqGT7w0I0TuHPQv"
    project_path="vercel-python-app"
    # Read the JSON config
    with open(config_file, "r") as file:
        student_data = json.load(file)
        
    project_path="vercel-python-app"
    
    # Create the project directory
    os.makedirs(project_path, exist_ok=True)
    
    # Write student data to a JSON file
    with open(os.path.join(project_path, "data.json"), "w") as f:
        json.dump(student_data, f)

    # Create main.py (FastAPI app)
    app_code = '''\
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            with open('data.json', "r") as file:
                student_data = json.load(file)

            query_params = parse_qs(urlparse(self.path).query)
            names = query_params.get('name', [])

            name_to_marks = {entry.get("name"): entry.get("marks", 0) for entry in student_data}
            marks = [name_to_marks.get(name, 0) for name in names]
            response = {"marks": marks}

            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    '''

    with open(os.path.join(project_path, "main.py"), "w") as f:
        f.write(app_code)

    # Create requirements.txt
    with open(os.path.join(project_path, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\n")

    # Create vercel.json
    vercel_config = {
        "version": 2,
        "builds": [{"src": "main.py", "use": "@vercel/python"}],
        "routes": [{"src": "/api", "dest": "main.py"}]
    }
    
    with open(os.path.join(project_path, "vercel.json"), "w") as f:
        json.dump(vercel_config, f, indent=4)

    # Change directory and deploy
    os.chdir(project_path)
    
    try:
        result = subprocess.run(
            ["vercel", "--prod", "--yes"],
            env={**os.environ, "VERCEL_AUTH_TOKEN": vercel_token},
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Vercel deployment failed: {result.stderr}")
        
        return f"{result.stdout.strip()}/api"

    except subprocess.CalledProcessError as e:
        return f"Error: Vercel deployment failed: {e}"

#############################
## Q. 7
def setup_github_workflow(EMAIL):
    GITHUB_USERNAME = "21f3002277"
    REPO_NAME = "your-repo-name-actions"
    WORKFLOW_FILE = "workflow.yml"
    """Creates a GitHub repository and adds a workflow file."""
    github_api = "https://api.github.com"
    headers = {"Authorization": f"token {github_pat_token}"}
    
    # Create repository
    create_repo_url = f"{github_api}/user/repos"
    repo_data = {"name": REPO_NAME, "private": False}
    repo_response = requests.post(create_repo_url, json=repo_data, headers=headers)
    
    if repo_response.status_code == 201:
        print(f"Repository created successfully: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
    else:
        print("Error creating repository:", repo_response.json())
        return False
    
    # Wait for GitHub to set up the repo
    time.sleep(5)
    
    # Create workflow file
    workflow_url = f"{github_api}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/.github/workflows/{WORKFLOW_FILE}"
    workflow_content = f'''
# This is a basic workflow to help you get started with Actions

name: CI

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events but only for the "main" branch
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v4

      # Runs a single command using the runners shell
      - name: {EMAIL}
        run: echo Hello, world!

      # Runs a set of commands using the runners shell
      - name: Run a multi-line script
        run: |
          echo Add other actions to build,
          echo test, and deploy your project.
'''
    encoded_content = base64.b64encode(workflow_content.encode()).decode()
    workflow_data = {"message": "Adding GitHub Action", "content": encoded_content, "branch": "main"}
    workflow_response = requests.put(workflow_url, json=workflow_data, headers=headers)
    
    if workflow_response.status_code in [200, 201]:
        print(f"Workflow created: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
        return f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}"
    else:
        print("Error creating workflow:", workflow_response.json())
        return False
    
#############################
## Q. 8

##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
# GA 3
#############################
## Q. 1
def generate_python_code_for_Analyze_the_sentiment(str_text):
    code =f'''
    
import httpx

def analyze_sentiment():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {{
        "Authorization": "Dummy_api_key",
        "Content-Type": "application/json"
    }}
    payload = {{
        "model": "gpt-4o-mini",
        "messages": [
            {{"role": "system", "content": "Analyze the sentiment of the following text. Classify it strictly as GOOD, BAD, or NEUTRAL."}},
            {{"role": "user", "content": "{str_text}"}}
        ]
    }}
    
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    print(result)

if __name__ == "__main__":
    try:
        analyze_sentiment()
    except httpx.HTTPStatusError as e:
        print(f"Error: {{e.response.json()}}")
    
    '''
    
    return code

#############################
## Q. 2
def get_token_count(str_content):
    url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIyNzdAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.K7NIPo5oVym7DFKdql2gXwAgdajEwnzHhEcSFCjc7gw"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
        }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": str_content}
        ],
        "temperature": 0,
        "max_tokens": 1,
        "logprobs": False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("usage", {}).get("prompt_tokens", "Token count not found")
    else:
        return f"Error: {response.status_code}, {response.text}"
    
#############################
## Q. 3
def LLM_Text_Extraction():
    
    code ='''
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "Respond in JSON"
    },
    {
      "role": "user",
      "content": "Generate 10 random addresses in the US"
    }
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "address_response",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "addresses": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "city": { "type": "string" },
                "country": { "type": "string" },
                "zip": { "type": "number" }
              },
              "required": ["city", "country", "zip"],
              "additionalProperties": false
            }
          }
        },
        "required": ["addresses"],
        "additionalProperties": false
      }
    }
  }
}
    '''
    return code

#############################
## Q. 4
def base_64_encoding(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        
    code = f'''
{{
  "model": "gpt-4o-mini",
  "messages": [
    {{
      "role": "user",
      "content": [
        {{"type": "text", "text": "Extract text from this image"}},
        {{
          "type": "image_url",
          "image_url": {{ "url": "data:image/png;base64,{base64_encoded_image}" }}
        }}
      ]
    }}
  ]
}}
    '''
    
    return code

#############################
## Q. 5
def embeddings_openai_and_local_models(first_message, second_message):
    code = f'''
{{
  "model": "text-embedding-3-small",
  "input": [
    "{first_message}",
    "{second_message}"
  ]
}}
    '''
    return code

#############################
## Q. 6
def embedding_similarity_topic_modeling(Embeddings):
    code = f'''
from itertools import combinations
import numpy as np

def cosine_similarity(vec1, vec2):
    """
    Calculate the cosine similarity between two vectors.
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

def most_similar(embeddings):
    """
    Find the pair of phrases with the highest cosine similarity.

    Args:
        embeddings (dict): A dictionary where keys are phrases and values are embedding vectors.

    Returns:
        tuple: A tuple containing the two most similar phrases.
    """
    max_similarity = -1
    most_similar_pair = None

    # Generate all pairs of phrases
    for phrase1, phrase2 in combinations(embeddings.keys(), 2):
        vec1 = embeddings[phrase1]
        vec2 = embeddings[phrase2]

        # Compute cosine similarity
        similarity = cosine_similarity(vec1, vec2)

        # Update the most similar pair if a higher similarity is found
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_pair = (phrase1, phrase2)

    return most_similar_pair

# Example usage
Embeddings = {Embeddings}
print(most_similar(embeddings))
'''
    
    return code

#############################
## Q. 7
def semantic_document_similarity_ranking():
    code = '''
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import httpx

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow only OPTIONS and POST
    allow_headers=["*"],  # Allow all headers
)

# OpenAI API details
OPENAI_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIyNzdAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.K7NIPo5oVym7DFKdql2gXwAgdajEwnzHhEcSFCjc7gw"
OPENAI_API_URL = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"

async def get_embedding(text: str) -> list:
    """Generate text embedding using OpenAI's API via httpx."""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "model": "text-embedding-3-small",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENAI_API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to generate embedding.")
        return response.json()["data"][0]["embedding"]

@app.post("/similarity")
async def similarity_endpoint(request: dict):
    try:
        docs = request.get("docs", [])
        query = request.get("query", "")

        if not docs or not query:
            raise HTTPException(status_code=400, detail="Both 'docs' and 'query' must be provided.")

        # Generate embeddings for the query and documents
        query_embedding = np.array(await get_embedding(query)).reshape(1, -1)
        doc_embeddings = [np.array(await get_embedding(doc)).reshape(1, -1) for doc in docs]

        # Compute cosine similarity between the query and each document
        similarities = [cosine_similarity(query_embedding, doc_embedding)[0][0] for doc_embedding in doc_embeddings]

        # Rank documents by similarity scores
        ranked_indices = np.argsort(similarities)[::-1]  # Sort in descending order
        top_3_matches = [docs[i] for i in ranked_indices[:3]]

        return {"matches": top_3_matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  
    '''

    # Write the FastAPI code to server.py
    with open("server.py", "w", encoding="utf-8") as file:
        file.write(code)

    # Start the FastAPI server
    url = run_server() + "/similarity"

    return url  # Return the API URL

#############################
## Q. 8
def query_to_function_mapping():
    code = '''
from fastapi import FastAPI, Query, HTTPException
import json
import requests

app = FastAPI()

# Enable CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


tools= [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_status",
            "description": "Get the status of a specific IT support ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "integer"
                    }
                },
                "required": [
                    "ticket_id"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_meeting",
            "description": "Schedule a meeting with a given date, time, and room.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string"
                    },
                    "time": {
                        "type": "string"
                    },
                    "meeting_room": {
                        "type": "string"
                    }
                },
                "required": [
                    "date",
                    "time",
                    "meeting_room"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_expense_balance",
            "description": "Retrieve the current expense reimbursement balance for an employee.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer"
                    }
                },
                "required": [
                    "employee_id"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_performance_bonus",
            "description": "Calculate the performance bonus for an employee in a specific year.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer"
                    },
                    "current_year": {
                        "type": "integer"
                    }
                },
                "required": [
                    "employee_id",
                    "current_year"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "report_office_issue",
            "description": "Report an office issue by specifying its code and department.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_code": {
                        "type": "integer"
                    },
                    "department": {
                        "type": "string"
                    }
                },
                "required": [
                    "issue_code",
                    "department"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# Endpoint to handle the query
@app.get("/execute")
async def execute(q: str = Query(..., description="The query to be executed")):
    url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIyNzdAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.K7NIPo5oVym7DFKdql2gXwAgdajEwnzHhEcSFCjc7gw'
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a function-calling assistant that maps queries to function calls."},
                {"role": "user", "content": q}
            ],
            "tools": tools,
            "tool_choice": "auto"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the function call from the LLM response
        if not response_data.get("choices"):
            raise HTTPException(status_code=400, detail="No choices in the LLM response.")
        
        message = response_data["choices"][0].get("message")
        if not message or not message.get("tool_calls"):
            raise HTTPException(status_code=400, detail="No tool calls in the LLM response.")
        
        function_call = response_data.get("choices", [{}])[0].get("message", {}).get("tool_calls")
        
        if function_call:  # Ensure the list is not empty
            first_call = function_call[0]  # Extract the first dictionary in the list
            function_name = first_call.get("function", {}).get("name", "")
            arguments = first_call.get("function", {}).get("arguments", "{}")

            return {"name": function_name, "arguments": json.dumps(json.loads(arguments))}
        
        return {"error": "Invalid query format"}
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
    '''

    # Write the FastAPI code to server.py
    with open("server.py", "w", encoding="utf-8") as file:
        file.write(code)

    # Start the FastAPI server
    url = run_server() + "/execute"

    return url  # Return the API URL

##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
# GA 4
#############################
## Q. 1                       ##
def count_ducks_on_page(page_number):
    base_url = 'https://stats.espncricinfo.com/ci/engine/stats/index.html'
    params = {
        'class': 2,
        'template': 'results',
        'type': 'batting',
        'page': page_number
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code == 403:
        raise Exception("Access denied. Try using a different approach.")

    tables = pd.read_html(response.text)
    
    if not tables:
        raise ValueError("No tables found on the page.")
    
    df = tables[2]

    if '0' not in df.columns:
        raise ValueError("The '0' column (ducks) is not present in the table.")

    df['0'] = pd.to_numeric(df['0'], errors='coerce')
    total_ducks = df['0'].sum()

    return total_ducks

#############################
## Q. 2                       ##
def fetch_rated_movies(filter_start, filter_end):
    url = f"https://www.imdb.com/search/title/?user_rating={filter_start},{filter_end}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = []
    for item in soup.select(".ipc-metadata-list-summary-item")[:25]:  # Select first 25 movies
        # Extract movie title
        title_elem = item.select_one(".ipc-title__text")
        if ":" in title_elem.text:
            title_1, title_2 =title_elem.text.split(":")
            title = title_1.strip() +' '+ title_2.strip()[0].lower() + title_2.strip()[1:]
        else:
            title = title_elem.text.strip() if title_elem else "N/A"
            
        

        # Extract year
        year_elem = item.select_one(".dli-title-metadata-item:nth-child(1)")
        year = year_elem.text if year_elem else "N/A"

        # Extract rating
        rating_elem = item.select_one(".ipc-rating-star--rating")
        rating = rating_elem.text.strip() if rating_elem else "N/A"

        # Extract IMDb ID
        link_elem = item.select_one(".ipc-title-link-wrapper")
        link = link_elem["href"] if link_elem else "N/A"
        movie_id = re.search(r"/title/(tt\d+)/", link)
        movie_id = movie_id.group(1) if movie_id else "N/A"

        movies.append({
            "id": movie_id,
            "title": title,
            "year": year,
            "rating": rating,
        })

    return json.dumps(movies, indent=2, ensure_ascii=False)

#############################
## Q. 3                       ##
def fetch_country_outline():
    code = '''
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from fastapi.responses import PlainTextResponse

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
async def get_country_outline(country: str = Query(..., title="Country Name")):
    wiki_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(wiki_url)

    if response.status_code != 200:
        return "Error: Country not found or Wikipedia page unavailable"

    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    markdown_outline = []
    for tag in headings:
        level = int(tag.name[1])  # Extracts the heading level from h1, h2, etc.
        markdown_outline.append(f"{'#' * level} {tag.text.strip()}")

    return "\\n".join(markdown_outline)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    '''

    # Write the FastAPI code to server.py
    with open("server.py", "w", encoding="utf-8") as file:
        file.write(code)

    # Start the FastAPI server
    url = run_server() + "/api/outline"

    return url  # Return the API URL

#############################
## Q. 4                       ##
def fetch_bbc_weather_forecast(location):
    
    from datetime import datetime, timedelta
    
    # Get location ID
    location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
        'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
        's': location,
        'stack': 'aws',
        'locale': 'en',
        'filter': 'international',
        'place-types': 'settlement,airport,district',
        'order': 'importance',
        'a': 'true',
        'format': 'json'
    })
    
    location_result = requests.get(location_url).json()
    location_id = location_result['response']['results']['results'][0]['id']
    
    # Fetch BBC Weather page
    weather_url = f'https://www.bbc.com/weather/{location_id}'
    response = requests.get(weather_url)
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract weather forecast
    forecast_data = {}
    forecast_elements = soup.select('.wr-day')  # Adjust the selector based on BBC's HTML structure
    
    today = datetime.today()
    
    for i, day in enumerate(forecast_elements):
        raw_date_text = day.select_one('.wr-date').text.strip()
        weather_desc = day.select_one('.wr-day__weather-type-description').text.strip()
        
        # Clean up unwanted text (remove weekday names, extra spaces)
        clean_date_text = re.sub(r'[^A-Za-z0-9 ]', '', raw_date_text)  # Remove special characters
        clean_date_text = re.sub(r'(\d+)\s*([A-Za-z]+).*', r'\1 \2', clean_date_text)  # Extract "23 March"

        # Extract day and month
        match = re.match(r'(\d+)\s+([A-Za-z]+)', clean_date_text)
        if match:
            day_number, month_name = match.groups()
            parsed_date = datetime.strptime(f"{day_number} {month_name} {today.year}", "%d %B %Y")

            # Handle year transition (December to January)
            if parsed_date.month < today.month:
                parsed_date = parsed_date.replace(year=today.year + 1)

            formatted_date = parsed_date.strftime("%Y-%m-%d")
        else:
            # If parsing fails, assume it's today + i days
            formatted_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        
        forecast_data[formatted_date] = weather_desc
    
    return json.dumps(forecast_data, indent=4)

#############################
## Q. 5                       ##
def get_max_latitude(city, country):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "city": city,
        "country": country,
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params, headers={"User-Agent": "UrbanRide/1.0"})
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['boundingbox'][1])  # Maximum latitude is the second value in boundingbox
    
    return None  # Return None if data is not found

#############################
## Q. 6                       ##
def fetch_latest_hn_post(topic, min_points):
    # Construct the HNRSS feed URL
    base_url = 'https://hnrss.org/newest'
    query = f'q={topic.replace(" ", "+")}&points={min_points}'
    feed_url = f'{base_url}?{query}'

    # Parse the RSS feed
    feed = feedparser.parse(feed_url)

    # Check if there are any entries in the feed
    if feed.entries:
        # Get the most recent entry
        latest_entry = feed.entries[0]
        return latest_entry.link
    else:
        return None

#############################
## Q. 7                       ##
def get_newest_github_user(location, min_followers, time_threshold):
    url = "https://api.github.com/search/users"
    params = {
        "q": f"location:{location} followers:>{min_followers}",
        "sort": "joined",
        "order": "desc",
        "per_page": 1
    }
    headers = {"Accept": "application/vnd.github+json"}
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        users = response.json().get("items", [])
        if users:
            user_url = users[0]["url"]  # Fetch full user profile
            user_response = requests.get(user_url, headers=headers)
            if user_response.status_code == 200:
                created_at = user_response.json().get("created_at")
                # Ignore ultra-new users (joined after 2025-03-22T10:09:06Z)
                if created_at <= time_threshold:
                    return created_at
    return None  # If no valid user found

#############################
## Q. 8                       ##
def setup_github_action(email):
  repo_name = "demo-github-action-schedule"
  github_username = "21f3002277"

  headers = {
    "Authorization": f"Bearer {github_pat_token}",
    "Accept": "application/vnd.github.v3+json"
  }
  

  # Step 2: Create Workflow File
  workflow_content = f'''
name: Daily Commit

on:
  schedule:
    - cron: '30 2 * * *'  # Runs daily at 02:30 UTC
  workflow_dispatch:  # Allows manual triggering

jobs:
  commit:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Git user ({email})
        run: |
          git config --global user.name "GitHub Actions Bot"
          git config --global user.email "{email}"

      - name: Make changes
        run: |
          echo "Last run: $(date)" > last_run.txt

      - name: Commit and push changes
        env:
          GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
        run: |
          git add last_run.txt
          git commit -m "Automated commit: $(date)" || echo "No changes to commit"
          git push origin main
    
  '''

  workflow_path = ".github/workflows/main.yaml"
  encoded_content = base64.b64encode(workflow_content.encode()).decode()

  # Check if the file already exists
  file_url = f"https://api.github.com/repos/{github_username}/{repo_name}/contents/{workflow_path}"
  get_response = requests.get(file_url, headers=headers)

  sha = None
  if get_response.status_code == 200:
    sha = get_response.json().get("sha")

  file_data = {
    "message": "Add GitHub Actions workflow for daily commits",
    "content": encoded_content,
    "branch": "main"
  }
  if sha:
    file_data["sha"] = sha  # Include sha if file exists

  response = requests.put(file_url, json=file_data, headers=headers)

  if response.status_code in [200, 201]:
    print(f"Workflow added successfully: {repo_name}")
  else:
    print("Error adding workflow:", response.json())

  repo_link = f"https://github.com/{github_username}/{repo_name}"
  print(f"Repository URL: {repo_link}")
  return repo_link

#############################
## Q. 9                       ##
def extract_total_marks(pdf_path, subject, threshold_marks, groups_range):
    total_marks = 0
    current_group = None
    start, end = map(int, groups_range.split("-"))
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split("\n")
            for line in lines:
                group_match = re.match(r"Student marks - Group (\d+)", line)
                if group_match:
                    current_group = int(group_match.group(1))
                
                if current_group and start <= current_group <= end:
                    values = list(map(int, re.findall(r'\d+', line)))
                    if len(values) == 5:  # Ensure we have exactly 5 subject marks
                        
                        if subject.lower() == "maths":
                            maths, _, _, _, _ = values
                            if maths >= threshold_marks:
                                total_marks += maths
                        elif subject.lower() == "physics":
                            _, physics, _, _, _ = values
                            if physics >= threshold_marks:
                                total_marks += physics
                            _, _, english, _, _ = values
                        elif subject.lower() == "english":
                            _, _, english, _, _ = values
                            if english >= threshold_marks:
                                total_marks += english
                        elif subject.lower() == "economics":
                            _, _, _, economics, _ = values
                            if economics >= threshold_marks:
                                total_marks += economics
                        elif subject.lower() == "biology":
                            _, _, _, _, biology = values
                            if biology >= threshold_marks:
                                total_marks += biology
                        else:
                            raise ValueError(f"Invalid subject: {subject}")
                        
    return total_marks

#############################
## Q. 10


##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
# GA 5
#############################
## Q. 1
def clean_and_calculate_margin(file_path, timestamp, product_name, country_code):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name='RawData')
    
    # Trim Customer Name
    df['Customer Name'] = df['Customer Name'].str.strip()
    
    # Standardize Country
    def standardize_country(country_str):
        if pd.isna(country_str):
            return None
        country_str = str(country_str).strip()
        try:
            # Try to find by alpha_2 code
            country = pycountry.countries.get(alpha_2=country_str.upper())
            if country:
                return country.alpha_2
        except:
            pass
        try:
            # Try to find by name
            country = pycountry.countries.get(name=country_str)
            if country:
                return country.alpha_2
        except:
            pass
        try:
            # Fuzzy search
            countries = pycountry.countries.search_fuzzy(country_str)
            if countries:
                return countries[0].alpha_2
        except:
            pass
        return None
    
    df['Country'] = df['Country'].apply(standardize_country)
    
    # Parse Date
    def parse_date(date_str):
        if pd.isna(date_str):
            return pd.NaT
        date_str = str(date_str).strip()
        try:
            return datetime.strptime(date_str, '%Y/%m/%d')
        except ValueError:
            try:
                return datetime.strptime(date_str, '%m-%d-%Y')
            except ValueError:
                return pd.NaT
    df['Date'] = df['Date'].apply(parse_date)
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['Date'])
    
    # Extract Product Name
    df['Product'] = df['Product/Code'].str.split('/').str[0]
    
    # Clean Sales and Cost
    df['Sales'] = df['Sales'].str.replace(' USD', '').str.strip().astype(float)
    # Handle Cost: remove 'USD', convert to float, fill missing with 0.5*Sales
    df['Cost'] = df['Cost'].str.replace(' USD', '').str.strip()
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['Cost'] = df['Cost'].fillna(df['Sales'] * 0.5)
    
    # Parse the cutoff timestamp (handle timezone format)
    cleaned_timestamp = timestamp.split(" (")[0]  # Remove timezone abbreviation
    cutoff_with_tz = parser.parse(cleaned_timestamp)
    cutoff_naive = cutoff_with_tz.astimezone(tz=None).replace(tzinfo=None)
    
    # Filter rows
    filtered = df[
        (df['Date'] <= cutoff_naive) &
        (df['Product'] == product_name) &
        (df['Country'] == country_code)
    ]
    
    if filtered.empty:
        return 0.0
    
    total_sales = filtered['Sales'].sum()
    total_cost = filtered['Cost'].sum()
    
    if total_sales == 0:
        return 0.0
    
    total_margin = (total_sales - total_cost) / total_sales
    return total_margin

#############################
## Q. 2                       ##
def count_unique_students(filename):
    unique_ids = set()
    
    # This regex looks for a dash, optional spaces, then the student ID (alphanumeric),
    # and uses a lookahead to ensure it is immediately followed by optional colons/spaces and the word "Marks".
    pattern = re.compile(r'-\s*([A-Z0-9]+)(?=\s*[:]*\s*Marks)', re.IGNORECASE)
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                student_id = match.group(1).strip()
                unique_ids.add(student_id)
    
    return len(unique_ids)

#############################
## Q. 3                       ##
def count_peak_requests(file_path, page, start_time_str, end_time_str, target_day):
    """
    Counts the number of successful GET requests for a specific page 
    within a given time window on a specific day.

    :param file_path: Path to the Apache log file (GZipped).
    :param page: The target page URL prefix (e.g., "/kannadamp3/").
    :param start_time_str: Start time as a string in "HH:MM" format.
    :param end_time_str: End time as a string in "HH:MM" format.
    :param target_day: The target day of the week (e.g., "Tuesday").
    :return: The count of matching requests.
    """
    request_count = 0
    day_map = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
        'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }

    # Convert time strings to integer hours
    start_hour = int(start_time_str.split(":")[0])
    end_hour = int(end_time_str.split(":")[0])

    # Regular expression to parse log entries
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) \S+'
    )

    # Read and process the log file
    with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = log_pattern.search(line)
            if match:
                log_time = match.group("datetime")
                method = match.group("method")
                url = match.group("url")
                status = int(match.group("status"))

                # Convert time to datetime object
                log_dt = datetime.strptime(log_time, "%d/%b/%Y:%H:%M:%S %z")

                # Check if it's the target day in GMT-0500
                if log_dt.weekday() == day_map[target_day]:
                    # Check if the time falls within the range
                    if start_hour <= log_dt.hour < end_hour:
                        # Check if it's a GET request and matches the page prefix
                        if method == "GET" and url.startswith(page):
                            # Check if the status code is in the 200-299 range
                            if 200 <= status < 300:
                                request_count += 1

    return request_count

#############################
## Q. 4                       ##
def process_apache_log(file_path, date, url_prefix):
    ip_bandwidth = defaultdict(int)
    
    # Regular expression to parse log entries
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<size>\S+)'
    )

    with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = log_pattern.search(line)
            if match:
                log_time = match.group("datetime")
                method = match.group("method")
                url = match.group("url")
                status = int(match.group("status"))
                size = match.group("size")
                ip = match.group("ip")

                # Handle cases where size is '-'
                size = int(size) if size.isdigit() else 0

                # Convert time to datetime object
                log_dt = datetime.strptime(log_time, "%d/%b/%Y:%H:%M:%S %z")

                # Filter by date and URL prefix
                if log_dt.strftime("%Y-%m-%d") == date and url.startswith(url_prefix):
                    # Only consider successful responses (200-299)
                    if 200 <= status < 300:
                        ip_bandwidth[ip] += size

    # Identify the top IP by bandwidth usage
    top_ip, top_bytes = max(ip_bandwidth.items(), key=lambda x: x[1], default=("N/A", 0))
    
    return top_bytes

#############################
## Q. 5                       ##
def analyze_product_sales_by_city(filename, product_name, city_name, unit_sales):
    # Calculate the target phonetic code for the given city name using Soundex
    target_code = jellyfish.soundex(city_name)
    
    total_sales = 0
    
    with open(filename, 'r') as file:
        data = json.load(file)
        for entry in data:
            # Check if the product matches and sales meet the minimum requirement
            if entry['product'] == product_name and entry['sales'] >= unit_sales:
                # Calculate the phonetic code for the current entry's city
                entry_code = jellyfish.soundex(entry['city'])
                if entry_code == target_code:
                    total_sales += entry['sales']
    
    return total_sales

#############################
## Q. 6                       ##
def calculate_total_sales(file_path):
    total_sales = 0
    sales_pattern = re.compile(r'"sales":(\d+)')
    
    with open(file_path, 'r') as file:
        for line in file:
            match = sales_pattern.search(line)
            if match:
                total_sales += int(match.group(1))
    
    return total_sales

#############################
## Q. 7                       ##
def count_key_occurrences(json_file_path, target_key):
    """Load JSON from a file and recursively count occurrences of a specific key."""
    with open(json_file_path, "r", encoding="utf-8") as file:
        json_obj = json.load(file)
    
    def recursive_count(obj):
        count = 0
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == target_key:
                    count += 1
                count += recursive_count(value)
        elif isinstance(obj, list):
            for item in obj:
                count += recursive_count(item)
        return count
    
    return recursive_count(json_obj)

#############################
## Q. 8                       ##
def get_high_engagement_posts(timestamp, useful_stars):
    query = f'''
SELECT DISTINCT post_id 
FROM (
    SELECT 
        timestamp, 
        post_id, 
        UNNEST(comments->'$[*].stars.useful') AS useful
    FROM social_media
) AS temp
WHERE useful >= {useful_stars} 
AND timestamp > '{timestamp}';

    '''
    
    return query

#############################
## Q. 9                       ##
def extract_and_transcribe(youtube_url, start_time, end_time, model_size="base"):
    """
    Downloads a YouTube video's audio, extracts the specified segment, and transcribes it.
    
    Args:
    youtube_url (str): The URL of the YouTube video.
    start_time (float): Start time in seconds.
    end_time (float): End time in seconds.
    model_size (str): Whisper model size (default: "base").

    Returns:
    str: Transcribed text.
    """
    # Step 1: Download audio using yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        audio_filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.mp4', '.mp3')

    # Step 2: Load and trim the audio
    audio = AudioSegment.from_file(audio_filename)
    trimmed_audio = audio[start_time * 1000:end_time * 1000]  # Convert to milliseconds
    trimmed_filename = "trimmed_audio.mp3"
    trimmed_audio.export(trimmed_filename, format="mp3")

    # Step 3: Transcribe using Whisper
    model = whisper.load_model(model_size)
    result = model.transcribe(trimmed_filename)

    return result["text"]

#############################
## Q. 10
def reconstruct_image(image_path, mapping, grid_size=(5, 5), output_path="reconstructed.png"):
    """
    Reconstructs a scrambled image based on the provided mapping.
    
    :param image_path: Path to the scrambled image.
    :param mapping: List of tuples (original_row, original_col, scrambled_row, scrambled_col).
    :param grid_size: Tuple representing the number of rows and columns (default: 5x5).
    :param output_path: Path to save the reconstructed image.
    """
    # Load the scrambled image
    image = Image.open(image_path)
    width, height = image.size
    piece_width = width // grid_size[1]
    piece_height = height // grid_size[0]
    
    # Create a blank canvas for the reconstructed image
    reconstructed = Image.new("RGB", (width, height))
    
    # Create a dictionary for easy lookup of where each piece belongs
    position_map = {(s_row, s_col): (o_row, o_col) for o_row, o_col, s_row, s_col in mapping}
    
    # Iterate over scrambled positions and place them in correct order
    for (s_row, s_col), (o_row, o_col) in position_map.items():
        # Extract the scrambled piece
        box = (s_col * piece_width, s_row * piece_height, (s_col + 1) * piece_width, (s_row + 1) * piece_height)
        piece = image.crop(box)
        
        # Place it in the correct position
        target_box = (o_col * piece_width, o_row * piece_height)
        reconstructed.paste(piece, target_box)
    
    # Save the reconstructed image
    reconstructed.save(output_path)
    print(f"Reconstructed image saved as {output_path}")

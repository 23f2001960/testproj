from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
import os
from dotenv import load_dotenv
from llm_tools_functions_calls import *
from llm_functions import *


app = FastAPI()
load_dotenv()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# required environment variables:
github_pat_token = os.getenv("GITHUB_PAT_TOKEN")
aiproxy_key = os.getenv("AIPROXY_KEY")



aiproxy_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"


def save_file(file: UploadFile) -> str:
    os.makedirs("Data", exist_ok=True)  # Ensure directory exists
    print(file.filename)
    file_path = os.path.join("Data", file.filename.split("/")[-1])
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)

@app.get("/")
async def home():
    return {"message": "AI Assignment Assistant is running >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"}


@app.post("/api/")
async def handle_request(question: str = Form(...), file: UploadFile = File(None)):
    if not question:
        return {"error": "Question is required"}
    
    answer = "I don't know the answer."
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {aiproxy_key}"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a Assignment assistant, designed to solve data science assignment problems. You should use the provided functions when appropriate to solve the problem."},
            {"role": "user", "content": question}
        ],
        "tools": tools,
        "tool_choice": "required"
    }
    
    
    response = requests.post(aiproxy_url, headers=headers, json=payload)
    print(response.text)
    response.raise_for_status()
    response_data = response.json()
        
        
    if not response_data.get("choices"):
        raise Exception("No response from AI")
        
    message = response_data["choices"][0]["message"]
    print(message)
    
    if not message or not message.get("tool_calls"):
        raise HTTPException(status_code=400, detail="No tool calls in the LLM response.")
        
    tool_call = message["tool_calls"][0]
    print(tool_call)
    function_name = tool_call["function"]["name"]
    print('#########################################')
    print(function_name)
    
    function_args = json.loads(tool_call["function"]["arguments"])
    
    answer = False
    if function_name == "get_vscode_status":  #####
        command = function_args["command"]
        answer = get_vscode_status(command)
    elif function_name == "send_https_request":  #####
        url = function_args["url"]
        email = function_args["email"]
        answer = send_https_request(url, email)
    elif function_name == "evaluate_google_sheets_expression":  #####
        expression = function_args["expression"]
        answer = evaluate_google_sheets_expression(expression)  
    elif function_name == "evaluate_excel_sheets_expression":  #####
        expression = function_args["expression"]
        answer = evaluate_excel_sheets_expression(expression)
    elif function_name == "get_hidden_input_value":  #####
        html = function_args["html"]
        answer = get_hidden_input_value(html)
    elif function_name == "count_wednesdays":  #####
        start_date = function_args["start_date"]
        end_date = function_args["end_date"]
        answer = count_wednesdays(start_date, end_date)
    elif function_name == "get_answer_from_csv_zip":  #####
        if file:
            file_path = save_file(file)
            answer = get_answer_from_csv_zip(file_path)
            delete_file(file_path)
        else:
            raise HTTPException(status_code=400, detail="File is required for this function.")
    elif function_name == "sort_json_list":
        json_array = function_args['json_array']
        first_parameter = function_args['first_parameter']
        second_parameter = function_args['second_parameter']
        answer = sort_json_list(first_parameter=first_parameter,second_parameter=second_parameter,json_list=json_array)
    elif function_name == "sum_data_values_of_foo_divs":
        html = function_args["html"]
        answer = sum_data_values_of_foo_divs(html)
    elif function_name == "sum_unicode_values_from_zip":
        if file:
            file_path = save_file(file)
            answer = sum_unicode_values_from_zip(file_path)
            delete_file(file_path)
        else:
            raise HTTPException(status_code=400, detail="File is required for this function.")
    elif function_name == "create_and_push_github_repo":  #####
        answer = create_and_push_github_repo()
    elif function_name == "replace_text_and_compute_sha256":  #####
        if file:
            file_path = save_file(file)
            answer = replace_text_and_compute_sha256(file_path)
            delete_file(file_path)
        else:
            raise HTTPException(status_code=400, detail="File is required for this function.")
    elif function_name == "extract_and_calculate_filtered_size":  #####
        if file:
            file_path = save_file(file)
            target_timestamp = function_args['target_timestamp']
            answer = extract_and_calculate_filtered_size(file_path, target_timestamp)
            delete_file(file_path)
        else:
            raise HTTPException(status_code=400, detail="File is required for this function.")
    elif function_name == "move_and_rename_files":  #####
        if file:
            file_path = save_file(file)
            answer = move_and_rename_files(file_path)
            delete_file(file_path)
        else:
            raise HTTPException(status_code=400, detail="File is required for this function.")
    elif function_name == "extract_and_count_different_lines":  #####
        if file:
            file_path = save_file(file)
            answer = extract_and_count_different_lines(file_path)
            delete_file(file_path)
        else:
            raise HTTPException(status_code=400, detail="File is required for this function.")
    elif function_name == "calculate_total_ticket_sales":
        item_type = function_args['item_type']
        answer = generate_sql_ticket_sales_query(item_type)
    elif function_name == "generate_markdown_documentation":
        answer = generate_markdown_documentation()
    elif function_name == "generate_python_code_for_Analyze_the_sentiment":
        string_text = function_args['string_text']
        answer = generate_python_code_for_Analyze_the_sentiment(string_text)
    elif function_name == "get_token_count":
        str_content = function_args['str_content']
        answer = get_token_count(str_content)
    elif function_name == "base_64_encoding":
        if file:
            file_path = save_file(file)
            answer = base_64_encoding(file_path)
            delete_file(file_path)
        else:
            raise HTTPException(status_code=400, detail="File is required for this function.")
    elif function_name == "embeddings_openai_and_local_models":
        first_message = function_args['first_message']
        second_message = function_args['second_message']
        answer = embeddings_openai_and_local_models(first_message, second_message)
    elif function_name == "embedding_similarity_topic_modeling":
        embeddings = function_args['embeddings']
        answer = embedding_similarity_topic_modeling(embeddings)
    elif function_name == "document_similarity_ranking":
        answer = semantic_document_similarity_ranking()
    elif function_name == "query_to_function_mapping":
        answer = semantic_document_similarity_ranking()
    elif function_name == "count_ducks_on_page":
        page_number = function_args['page_number']
        answer = count_ducks_on_page(page_number)
    elif function_name == "fetch_rated_movies":
        filter_start = function_args['filter_start']
        filter_end = function_args['filter_end']
        answer = fetch_rated_movies(filter_start,filter_end)
    elif function_name == "fetch_country_outline":
        answer = fetch_country_outline()
    elif function_name == "fetch_bbc_weather_forecast":
        location = function_args['location']
        answer = fetch_bbc_weather_forecast(location)
    elif function_name == "get_max_latitude":
        city = function_args['city']
        country = function_args['country']
        answer = get_max_latitude(city, country)
    elif function_name == "fetch_latest_hn_post":
        topic = function_args['topic']
        min_points = function_args['min_points']
        answer = fetch_latest_hn_post(topic, min_points)
    elif function_name == "get_newest_github_user":
        location = function_args['location']
        min_followers = function_args['min_followers']
        time_threshold = function_args['time_threshold']
        answer = get_newest_github_user(location, min_followers,time_threshold)
    elif function_name == "setup_github_action":
        email = function_args['email']
        answer = setup_github_action(email)
    elif function_name == "extract_total_marks":
        if file:
            pdf_path = save_file(file)
            subject= function_args['subject']
            threshold_marks = function_args['threshold_marks']
            groups_range = function_args['groups_range']
            answer = extract_total_marks(pdf_path,subject,threshold_marks, groups_range)
            delete_file(file_path)
        else:
            raise HTTPException(status_code=400, detail="File is required for this function.")
        
    elif function_name == "":
        pass
        
    if answer:
        return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)

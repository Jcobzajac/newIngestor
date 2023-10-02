import datetime
import os
import openai

GPT_MODEL = "gpt-3.5-turbo"
openai.api_key = os.getenv("OPENAI_API_KEY") #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


def generate_response(text):
    combined_query = f"Please make a summary from this text : {text}"

    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": combined_query},
        ],
        temperature=0.3,
    )
    generated_response = response['choices'][0]['message']['content']

    return generated_response

def write_summary(date, summary, summary_file_name):
    with open(summary_file_name, "a") as file:
        if file.tell() != 0:  # Check if the file is not empty
            file.write("\n")
        file.write(str(date) + "\n")
        file.write(str(summary))


def process_file(primary_file_name, most_recent_date, summary_file_name, state_file_name): 

    date = None # Date assigned to the text
    text = "" #Content of each paragraph
    with open(primary_file_name, 'r') as file:
        lines = file.readlines()
        total_lines = len(lines)
        start_line = most_recent_date - 1 if most_recent_date is not None else 0 #If state is provided then it's a starting point
        total_lines -= start_line
        for i, line in enumerate(lines[start_line:]):
            try:
                validate_date = line.replace('\n', '')
                check_date = datetime.datetime.strptime(f"{validate_date}","%m/%d/%y") #Check whether particular line is the date
                if date is None:
                    date = validate_date
                else:
                    summary = generate_response(text)
                    write_summary(date=date,summary=summary,summary_file_name=summary_file_name)
                    date = validate_date
                    text = ""
            except ValueError:
                text += line
            if i + 1 == total_lines:
                summary = generate_response(text)
                write_summary(date=date,summary=summary,summary_file_name=summary_file_name)
        
        print(date)
        write_state(state_file_name=state_file_name,state=date)


def get_state(state_file_name):

    with open(state_file_name, 'r') as file:
       state = file.readline()
    
    return state

            
def write_state(state_file_name, state):

    with open(state_file_name, "w") as file:
        file.write(state)

def define_starting_point(primary_file_name, most_recent_date):
    
    existence = False
    with open(primary_file_name, 'r') as file:
        for line_number, line in enumerate(file, start=1):

            if existence == True:
                try:
                    validate_date = line.replace('\n', '')
                    check_date = datetime.datetime.strptime(f"{validate_date}","%m/%d/%y")
                    starting_point = line_number
                    return starting_point
                except ValueError:
                    pass

            elif most_recent_date in line:
                existence = True




#def process_file(primary_file_name, most_recent_date, summary_file_name, state_file_name): 

#process_file(primary_file_name="primary.txt", most_recent_date=None, summary_file_name="summaries.txt", state_file_name="state.txt")
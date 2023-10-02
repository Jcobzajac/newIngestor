from operations_google import authentication, modify_file, get_file
from processing import generate_response, write_summary, process_file, get_state, write_state, define_starting_point


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
# IDs of the files from Google Drive
primary_file_id = "1o9pehABzLjkWy3ZLRALdjgGFIGPLIz7uS16toTUJRxo"
summary_file_id = "1LDWxIcNH9M5t21sdEpqyU3bQfXLp4ry_6AAhpQtBOfI"
state_file_id = "1MmRORzi6uGslMlBrHgx2rK36HZOX7KsE-a5LXL5hqV4"
# Names of the files from localhost
primary_file_name = "primary.txt"
summary_file_name = "summaries.txt"
state_file_name = "state.txt"

#Google Authentication
creds = authentication(SCOPES)

#Fetch files
get_file(file_id= primary_file_id, file_name_local=primary_file_name)
get_file(file_id= summary_file_id, file_name_local=summary_file_name)
get_file(file_id= state_file_id, file_name_local=state_file_name)

#Get state of the last run
state = get_state(state_file_name)

if state == "":
    state = None
else:
  state = define_starting_point(primary_file_name=primary_file_name, most_recent_date=state)

#Process primary file
process_file(primary_file_name=primary_file_name, most_recent_date=state, state_file_name=state_file_name, summary_file_name=summary_file_name)

#Modify files
modify_file(file_id_to_modify=primary_file_id, file_name_with_new_content=primary_file_name, creds=creds)
modify_file(file_id_to_modify=summary_file_id, file_name_with_new_content=summary_file_name, creds=creds)
modify_file(file_id_to_modify=state_file_id, file_name_with_new_content=state_file_name, creds=creds)
function SendRequest(method, data, query_params, url){
    var url = new URL(url);
    for (key in Object.keys(query_params)){
        url.searchParams.append(key, query_params[key]);
    }
    var request = new XMLHttpRequest();
    request.open('POST', url, false);
    request.send(data);
}

function CreateResumeView(customer_id, topics_data_query, resume_data){
    // Creates new Resume.
    var unified_http_request_payload = {'topics': topics_data_query, 'resume_data': resume_data}
    SendRequest('POST', unified_http_request_payload,
    {'customer_id': customer_id}, 'http://localhost:8000/create/resume/');
}

function UpdateResumeView(updated_resume_data, topics_data_query, resume_id){
    // Updates Existing Resume.
    var unified_http_request_payload = {'topics': topics_data_query, 'updated_data': updated_resume_data};
    SendRequest('PUT', unified_http_request_payload, {'resume_id': resume_id}, 'http://localhost:8000/update/resume/');
}

function DeleteResumeView(resume_id){
    // Deletes Resume.
    SendRequest('DELETE', null, {'resume_id': resume_id},
    'http://localhost:8000/delete/resume/');
}
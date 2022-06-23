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


function getFormattedResumeView(request_url, resume_content){
       var url = new URL("http://localhost:8000/get/pdf/resume/");
   $.ajax({
        url: url,
        data: resume_content,
        headers: {'Content-Type': 'application/json'},
        type: "POST",
        success: function(response){
            console.log('responded with success, ', response);
            return response
        },
        error: function(error){
            console.log('responded with exception: ' + error);
        }
   });
}
function getPDFResumeView(resume_content){
   var request_url = new URL("http://localhost:8000/get/pdf/resume/");
   var pdf_file = getFormattedResumeView(request_url, resume_content);
   return pdf_file;
}

function GetWordResumeView(resume_content){
   var request_url = new URL("http://localhost:8000/get/pdf/resume/");
   var word_file = getFormattedResumeView(request_url, resume_content);
   return word_file;
}
import * as api from "./api.js"

$("#CreateResumeBtn").addEventListener('submit', function(){
    var files = {};
    var resume_content = $(this).value;
    var customer_id = document.getElementById('customer_id').value;
    var response = api.CreateResumeView(customer_id);
    if (!response.status_code in (200, 201)){
            console.log('Exception. Form has not been proceeded.');
        }
    }
});

$('#UpdateBtn.addEventListener').addEventListener('submit', function(){
    var files = {}
    var resume_updated_content = $(this).value;
    var customer_id = document.getElementById('customer_id').value;
    var response = api.UpdateResumeView(customer_id, resume_updated_content);
    if (!response.status_code in (200, 201)){
        console.log('Exception. Form has not been proceeded.');
    }
});

$('#DeleteBtn.addEventListener').addEventListener('submit', function(){
    var response = api.DeleteResumeView(customer_id);
    if (!response.status_code in (200, 201)){
        console.log('Exception. Form has not been proceeded.');
    }
});

$("#resume_pdf_preview").addEventListener('click', function(){

    var resume_content = document.getElementById('resume_content').value;
    var resume_byte_array = api.getPDFResumeView(resume_content);
    console.log('resume byte array has been obtained...');

});

$("#resume_word_preview").addEventListener('click', function(){
    var resume_content = document.getElementById('resume_content').value;
    var resume_file = api.getWordResumeView('resume_content');
    console.log('resume edit file obtained..');
});
